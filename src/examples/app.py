#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Easypay API
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Easypay API.
#
# Hive Easypay API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Easypay API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Easypay API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import base

import appier

class MBApp(appier.APIApp):

    def __init__(self, *args, **kwargs):
        appier.APIApp.__init__(self, name = "mb", *args, **kwargs)
        self.api = base.get_api()
        self.api.bind("paid", self.on_paid)

    def start(self):
        appier.APIApp.start(self)
        self.api.start_scheduler()

    def stop(self):
        appier.APIApp.stop(self)
        self.api.stop_scheduler()

    def on_paid(self, reference, details):
        identifier = reference["identifier"]
        value = reference["value"]
        self.logger.info("Payment notification '%s' for value %s" % (identifier, value))

    @appier.route("/generate", "GET")
    def generate(self):
        amount = self.field("amount", 10)
        return self.api.generate_mb(amount)

    @appier.route("/cancel", "GET")
    def cancel(self):
        key = self.field("key")
        return self.api.cancel_mb(key)

    @appier.route("/details", "GET")
    def details(self):
        doc = self.field("doc")
        return self.api.details_mb(doc)

    @appier.route("/notification", "GET")
    def notification(self):
        cin = self.field("ep_cin")
        username = self.field("ep_user")
        doc = self.field("ep_doc")
        result = self.api.notify_mb(cin, username, doc)
        self.content_type("application/xml")
        return result

    @appier.route("/references", "GET")
    def references(self):
        return self.api.list_references()

    @appier.route("/docs", "GET")
    def docs(self):
        return self.api.list_docs()

if __name__ == "__main__":
    app = MBApp()
    app.serve()
else:
    __path__ = []
