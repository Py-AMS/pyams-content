#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.milestone.portlet.skin module

This module provides front-office renderers for the milestones portlet.
"""

from zope.interface import Interface

from pyams_content.component.milestone.portlet.interfaces import IMilestonesPortletSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseMilestoneRenderer(PortletRenderer):
    """Base milestones renderer"""

    def get_paragraph_anchor(self, milestone):
        """Paragraph anchor getter"""
        target = milestone.target
        return target.get_anchor(self.request) if target is not None else None


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IMilestonesPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/milestones-default.pt', layer=IPyAMSLayer)
class MilestonesPortletDefaultRenderer(BaseMilestoneRenderer):
    """Milestones portlet default renderer"""

    label = _("Vertical timeline (default)")
    weight = 1


@adapter_config(name='horizontal',
                required=(IPortalContext, IPyAMSLayer, Interface, IMilestonesPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/milestones-horizontal.pt', layer=IPyAMSLayer)
class MilestonesPortletHorizontalRenderer(BaseMilestoneRenderer):
    """Milestones portlet horizontal renderer"""

    label = _("Horizontal timeline")
    weight = 10

