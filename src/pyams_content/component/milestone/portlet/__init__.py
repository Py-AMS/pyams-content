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

"""PyAMS_content.component.milestone.portlet module

This module provides the milestones portlet implementation.
"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.milestone import MilestonesContainer
from pyams_content.component.milestone.interfaces import MILESTONES_PARAGRAPH_ICON_CLASS
from pyams_content.component.milestone.portlet.interfaces import IMilestonesPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


MILESTONES_PORTLET_NAME = 'pyams_content.portlets.milestones'


@factory_config(provided=IMilestonesPortletSettings)
class MilestonesPortletSettings(MilestonesContainer, PortletSettings):
    """Milestones portlet settings"""

    title = FieldProperty(IMilestonesPortletSettings['title'])
    header = FieldProperty(IMilestonesPortletSettings['header'])


@portlet_config(permission=None)
class MilestonesPortlet(Portlet):
    """Milestones portlet"""

    name = MILESTONES_PORTLET_NAME
    label = _("Milestones")

    settings_factory = IMilestonesPortletSettings
    toolbar_css_class = MILESTONES_PARAGRAPH_ICON_CLASS

