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

class MBApi(object):

    def generate_mb(self, amount, country = "PT", language = "PT"):
        # @todo must keep track of this stuff
        import uuid
        key = str(uuid.uuid4())

        url = self.base_url + "api_easypay_01BG.php"
        return self.get(
            url,
            ep_ref_type = "auto",
            ep_entity = self.entity,
            t_key = key,
            t_value = amount,
            ep_country = country,
            ep_language = language,
        )

    def notify_mb(self, cin, username, doc):
        key = self.next()
        self.validate(cin = cin, username = username)
        result = dict(
            ep_status = "ok",
            ep_message = "doc gerado",
            ep_cin = cin,
            ep_user = username,
            ep_doc = doc,
            ep_key = key
        )
        return self.dumps(result)


#        <?xml version="1.0" encoding="ISO-8859-1"?>
#<getautoMB_detail>
#<ep_status>ok0</ep_status>
#<ep_message>id e cin ok;ip ok;doc EASYTEST92008091256378290408 and key 1
#ok;</ep_message>
#<ep_cin>8889</ep_cin>
#<ep_user>EASYTEST9</ep_user>
#<ep_key>1</ep_key>
#<t_key>{ORDER_ID}</t_key>
#<ep_doc>EASYTEST92008091256378290408</ep_doc>
#<ep_payment_type>MB</ep_payment_type>
#<ep_entity>10611</ep_entity>
#<ep_reference>888900174</ep_reference>
#<ep_value>10.00</ep_value>
#<ep_value_fixed>0.35</ep_value_fixed>
#<ep_value_var>0.18</ep_value_var>
#<ep_value_tax>0.11</ep_value_tax>
#<ep_value_transf>9.36</ep_value_transf>
#<ep_date_transf>2008-01-29</ep_date_transf>
#<ep_date_read>2008-04-11 20:19:42</ep_date_read>
#<ep_status_read>verified</ep_status_read>
#</getautoMB_detail>
