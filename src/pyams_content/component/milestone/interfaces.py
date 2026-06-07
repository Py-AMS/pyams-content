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

"""PyAMS_content.component.milestone.interfaces module

This module defines interfaces for milestone components.
Each milestone represents a step in a chronological list, characterised by a title,
a label, a pictogram, a navigation anchor, and a visibility flag.
"""

from zope.container.constraints import contains
from zope.container.interfaces import IOrderedContainer
from zope.interface import Attribute
from zope.location.interfaces import IContained
from zope.schema import Bool, Choice, TextLine

from pyams_content.component.paragraph import CONTENT_PARAGRAPHS_VOCABULARY
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_content.reference.pictogram.interfaces import SELECTED_PICTOGRAM_VOCABULARY
from pyams_i18n.schema import I18nHTMLField, I18nTextField, I18nTextLineField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IMilestoneInfo(IContained):
    """Milestone info interface"""

    visible = Bool(title=_("Visible?"),
                   description=_("Is this milestone visible in front-office?"),
                   required=True,
                   default=True)

    title = I18nTextLineField(title=_("Title"),
                              description=_("Main label of this milestone step"),
                              required=True)

    header = I18nTextField(title=_('milestone-header', default="Header"),
                           description=_("Short text displayed alongside the milestone "
                                         "(e.g. a date or a short qualifier)"),
                           required=False)

    body = I18nHTMLField(title=_('milestone-body', default="Body"),
                         description=_("Longer text displayed alongside the milestone"),
                         required=False)

    pictogram_name = Choice(title=_("Pictogram"),
                            description=_("Name of the pictogram associated with this milestone"),
                            required=False,
                            vocabulary=SELECTED_PICTOGRAM_VOCABULARY)

    pictogram = Attribute("Selected pictogram object associated with this milestone")

    anchor = Choice(title=_("Navigation anchor"),
                    description=_("Paragraph to which this milestone should lead"),
                    vocabulary=CONTENT_PARAGRAPHS_VOCABULARY,
                    required=False)

    target = Attribute("Anchor target")


class IMilestonesContainer(IOrderedContainer):
    """Milestones container interface"""

    contains(IMilestoneInfo)

    def get_visible_items(self):
        """Get iterator over visible milestones"""


MILESTONES_PARAGRAPH_TYPE = 'milestones'
MILESTONES_PARAGRAPH_NAME = _("Milestones")
MILESTONES_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.milestones.renderers'
MILESTONES_PARAGRAPH_ICON_CLASS = 'fas fa-road'


class IMilestonesParagraph(IMilestonesContainer, IBaseParagraph):
    """Milestones paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for milestones"),
                                       renderers=MILESTONES_PARAGRAPH_RENDERERS)

