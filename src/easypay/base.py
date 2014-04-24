#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Easypay API
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Easypay API.
#
# Hive Easypay API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Easypay API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Easypay API. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import uuid
import shelve
import threading

import xml.dom.minidom
import xml.etree.ElementTree

import appier

from easypay import mb
from easypay import errors

BASE_URL = "https://www.easypay.pt/_s/"
""" The default base url to be used for a production
based environment, should be used carefully """

BASE_URL_TEST = "http://test.easypay.pt/_s/"
""" The base url for the sandbox endpoint, this is used
for testing purposes only and the password is sent using
a non encrypted model (no protection provided) """

class Api(mb.MBApi):

    def __init__(self, *args, **kwargs):
        self.production = kwargs.get("production", False)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.cin = kwargs.get("cin", None)
        self.entity = kwargs.get("entity", None)
        self.base_url = BASE_URL if self.production else BASE_URL_TEST
        self.counter = 0
        self.references = list()
        self.docs = dict()
        self.lock = threading.RLock()

    def request(self, method, *args, **kwargs):
        result = method(*args, **kwargs)
        result = self.loads(result)
        status = result.get("ep_status", "err1")
        message = result.get("ep_message", "no message defined")
        if not status == "ok0": raise errors.ApiError(message)
        return result

    def build_kwargs(self, kwargs, auth = True, token = False):
        if self.cin: kwargs["ep_cin"] = self.cin
        if self.username: kwargs["ep_user"] = self.username

    def get(self, _url, auth = True, token = False, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.get,
            _url,
            params = kwargs
        )

    def post(self, _url, auth = True, token = False, data = None, data_j = None, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.post,
            _url,
            params = kwargs,
            data = data,
            data_j = data_j
        )

    def new_reference(self, data):
        cin = data["ep_cin"]
        username = data["ep_user"]
        entity = data["ep_entity"]
        reference = data["ep_reference"]
        value = data["ep_value"]
        identifier = data["t_key"]
        self.references.append(dict(
            cin = cin,
            username = username,
            entity = entity,
            reference = reference,
            value = value,
            identifier = identifier,
            status = "pending"
        ))

    def new_doc(self, doc, key):
        self.docs[doc] = dict(
            cin = self.cin,
            username = self.username,
            doc = doc,
            key = key
        )

    def get_doc(self, doc):
        return self.docs[doc]

    def next(self):
        self.lock.acquire()
        try: self.counter += 1; next = self.counter
        finally: self.lock.release()
        return next

    def generate(self):
        identifier = str(uuid.uuid4())
        return identifier

    def validate(self, cin = None, username = None):
        if cin and not cin == self.cin:
            raise errors.SecurityError("invalid cin")
        if username and not username == self.username:
            raise errors.SecurityError("invalid username")

    def loads(self, data):
        result = dict()
        document = xml.dom.minidom.parseString(data)
        base = document.childNodes[0]
        for node in base.childNodes:
            name = node.nodeName
            value = self._text(node)
            if value == None: continue
            result[name] = value
        return result

    def dumps(self, map, root = "getautoMB_detail", encoding = "utf-8"):
        root = xml.etree.ElementTree.Element(root)
        for name, value in map.iteritems():
            value = value if type(value) in appier.STRINGS else str(value)
            child = xml.etree.ElementTree.SubElement(root, name)
            child.text = value
        result = xml.etree.ElementTree.tostring(
            root,
            encoding = encoding,
            method = "xml"
        )
        result = "<?xml version=\"1.0\" encoding=\"%s\"?>" % encoding + result
        return result

    def _text(self, node):
        if not node.childNodes: return None
        return node.childNodes[0].nodeValue

class ShelveApi(Api):

    def __init__(self, path = "easypay.shelve", *args, **kwargs):
        Api.__init__(self, *args, **kwargs)
        self.shelve = shelve.open(path, writeback = True)

    def new_reference(self, data):
        t_key = data["t_key"]
        data[t_key] = data
        self.shelve.sync()

    def new_doc(self, doc, key):
        pass

    def get_doc(self, doc):
        pass

    def next(self):
        pass

class MongoApi(Api):
    pass
