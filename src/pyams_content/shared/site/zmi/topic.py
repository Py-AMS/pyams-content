#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.site.zmi.topic module

This module defines sites topics management components.
"""

from pyams_content.shared.site.interfaces import ISiteManager
from pyams_utils.adapter import NullAdapter
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager


__docformat__ = 'restructuredtext'


@viewlet_config(name='add-content.action',
                context=ISiteManager, layer=IAdminLayer,
                manager=IToolbarViewletManager, weight=10)
class SiteManagerContentAddAction(NullAdapter):
    """Site manager add action"""
