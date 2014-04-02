#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Easypay API
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import appier

import mb

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

    def request(self, method, *args, **kwargs):
        return method(*args, **kwargs)

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
