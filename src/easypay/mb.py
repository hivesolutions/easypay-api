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

class MBApi(object):
    """
    Class that represents the api for the easypay multibanco
    and that contains the entry points for its interaction.

    The current implementation involves three main steps:
    first the generation of the (mb) reference from the
    client to the server, then the notification from the
    server about the payment and then the retrieval of
    the payment details from the client.

    Please note that the retrieval of the payment details
    from the client may fail and so a continuous loop of
    retries must be done to ensure no errors.
    """

    def generate_mb(self, amount, country = "PT", language = "PT"):
        url = self.base_url + "api_easypay_01BG.php"
        result = self.get(
            url,
            ep_ref_type = "auto",
            ep_entity = self.entity,
            t_key = self.generate(),
            t_value = amount,
            ep_country = country,
            ep_language = language,
        )
        self.gen_reference(result)
        return result

    def details_mb(self, doc):
        info = self.get_doc(doc)
        key = info["key"]
        url = self.base_url + "api_easypay_03AG.php"
        return self.get(
            url,
            ep_key = key,
            ep_doc = doc
        )

    def notify_mb(self, cin, username, doc):
        key = self.next()
        self.validate(cin = cin, username = username)
        self.gen_doc(doc, key)
        result = dict(
            ep_status = "ok",
            ep_message = "doc gerado",
            ep_cin = cin,
            ep_user = username,
            ep_doc = doc,
            ep_key = key
        )
        return self.dumps(result)

    def mark_mb(self, details):
        t_key = details["t_key"]
        doc = details["ep_doc"]
        reference = self.get_reference(t_key)
        self.trigger("paid", reference)
        self.trigger("marked", reference)
        self.del_reference(t_key)
        self.del_doc(doc)
