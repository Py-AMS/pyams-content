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

"""PyAMS_content.component.milestone.skin module

This module provides front-office renderers for milestones paragraphs.
"""

from pyams_content.component.milestone.interfaces import IMilestonesParagraph
from pyams_content.feature.renderer import BaseContentRenderer
from pyams_content.feature.renderer.interfaces import IContentRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseMilestonesRenderer(BaseContentRenderer):
    """Base milestones renderer"""

    def get_paragraph_anchor(self, milestone):
        """Paragraph anchor getter"""
        target = milestone.target
        return target.get_anchor(self.request) if target is not None else None


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IMilestonesParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/milestones-default.pt',
                 layer=IPyAMSLayer)
class MilestonesParagraphDefaultRenderer(BaseMilestonesRenderer):
    """Milestones paragraph default renderer"""

    label = _("Vertical timeline (default)")
    weight = 10


@adapter_config(name='horizontal',
                required=(IMilestonesParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/milestones-horizontal.pt',
                 layer=IPyAMSLayer)
class MilestonesParagraphHorizontalRenderer(BaseMilestonesRenderer):
    """Milestones paragraph horizontal renderer"""

    label = _("Horizontal timeline")
    weight = 20
