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

import base

import appier

class MBApp(appier.App):

    def __init__(self):
        appier.App.__init__(self, name = "mb")
        self.api = base.get_api()

    @appier.route("/generate", "GET")
    def generate(self):
        amount = self.field("amount", 10)
        return self.api.generate_mb(amount)

    @appier.route("/notification", "GET")
    def notification(self):
        cin = self.field("ep_cin")
        username = self.field("ep_user")
        doc = self.field("ep_doc")
        print "notification"
        print self.request.args
        #api.notify() -> deve devolver o xml correspondente
        #@todo: tenho de retornar xml aki
        return "<xml>"

if __name__ == "__main__":
    app = MBApp()
    app.serve()