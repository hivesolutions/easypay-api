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

import appier

import easypay


def get_api(api_class=easypay.ShelveAPI):
    return api_class(
        username=appier.conf("EASYPAY_USERNAME"),
        password=appier.conf("EASYPAY_PASSWORD"),
        cin=appier.conf("EASYPAY_CIN"),
        entity=appier.conf("EASYPAY_ENTITY"),
    )


def get_api_v2(api_class=easypay.ShelveAPIv2):
    return api_class(
        account_id=appier.conf("EASYPAY_ACCOUNT_ID"),
        key=appier.conf("EASYPAY_KEY"),
    )
