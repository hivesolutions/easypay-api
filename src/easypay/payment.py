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


class PaymentAPI(object):

    def list_payments(self, *args, **kwargs):
        url = self.base_url + "single"
        return self.get(url, *args, **kwargs)

    def create_payment(self, amount, method="mb", key=None):
        url = self.base_url + "single"
        return self.post(url, data_j=dict(value=amount, method=method, key=key))

    def get_payment(self, id):
        url = self.base_url + "single/%s" % id
        return self.get(url)
