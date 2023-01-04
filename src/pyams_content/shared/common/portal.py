#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.portal module

"""

from pyams_content.shared.common import IBaseSharedTool
from pyams_content.shared.common.interfaces import IBaseContentPortalContext, \
    ISharedContentPortalPage
from pyams_portal.interfaces import IPortalPage, PORTAL_PAGE_KEY
from pyams_portal.page import PortalPage
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'


class SharedContentPortalPageMixin:
    """Shared content portal page mixin class"""

    @volatile_property
    def can_inherit(self):
        return IPortalPage(self.parent).template is not None

    @property
    def parent(self):
        return get_parent(self, IBaseSharedTool, allow_context=False)


#
# SHared content portal page
#

@factory_config(ISharedContentPortalPage)
class SharedContentPortalPage(SharedContentPortalPageMixin, PortalPage):
    """Shared content portal page"""


@adapter_config(required=IBaseContentPortalContext,
                provides=IPortalPage)
def shared_content_portal_page_adapter(context):
    """Shared content portal page adapter"""
    return get_annotation_adapter(context, PORTAL_PAGE_KEY, ISharedContentPortalPage)
