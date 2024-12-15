#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Easypay API
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import pprint
import appier

import base


class MBAppV2(appier.APIApp):

    def __init__(self, *args, **kwargs):
        appier.APIApp.__init__(self, name="mb_v2", *args, **kwargs)
        self.api = base.get_api_v2()

    @appier.route("/payments", "GET")
    def payments(self):
        return self.api.list_payments()

    @appier.route("/payments/create", "GET")
    def create_payment(self):
        amount = self.field("amount", 10, cast=float)
        method = self.field("method", "mb")
        key = self.field("key", None)
        return self.api.create_payment(amount=amount, method=method, key=key)

    @appier.route("/payments/show/<str:id>", "GET")
    def show_payment(self, id):
        return self.api.get_payment(id=id)

    @appier.route("/payments/delete/<str:id>", "GET")
    def delete_payment(self, id):
        return self.api.delete_payment(id=id)

    @appier.route("/payments/notify", "POST")
    def notify_payment(self):
        data = appier.request_json()
        self.logger.debug("Received payment notification:\n%s" % pprint.pformat(data))

    @appier.route("/generic/notify", "POST")
    def notify_generic(self):
        data = appier.request_json()
        self.logger.debug("Received generic notification:\n%s" % pprint.pformat(data))


if __name__ == "__main__":
    app = MBAppV2()
    app.serve()
else:
    __path__ = []
