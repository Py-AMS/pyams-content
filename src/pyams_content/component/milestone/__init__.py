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

"""PyAMS_content.component.milestone module

This module provides persistent classes used to handle milestones.
"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.milestone.interfaces import IMilestoneInfo, IMilestonesContainer, \
    IMilestonesParagraph, MILESTONES_PARAGRAPH_ICON_CLASS, MILESTONES_PARAGRAPH_NAME, \
    MILESTONES_PARAGRAPH_RENDERERS, MILESTONES_PARAGRAPH_TYPE
from pyams_content.component.paragraph import BaseParagraph, ParagraphPermissionChecker, IParagraphContainer
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_content.reference.pictogram.interfaces import IPictogramTable
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry, query_utility
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'


@factory_config(provided=IMilestoneInfo)
class Milestone(Persistent, Contained):
    """Milestone persistent class"""

    visible = FieldProperty(IMilestoneInfo['visible'])
    title = FieldProperty(IMilestoneInfo['title'])
    header = FieldProperty(IMilestoneInfo['header'])
    body = FieldProperty(IMilestoneInfo['body'])
    _pictogram_name = FieldProperty(IMilestoneInfo['pictogram_name'])
    anchor = FieldProperty(IMilestoneInfo['anchor'])

    @property
    def pictogram_name(self):
        """Pictogram name getter"""
        return self._pictogram_name

    @pictogram_name.setter
    def pictogram_name(self, value):
        """Pictogram name setter — clears cached pictogram on change"""
        if value != self._pictogram_name:
            self._pictogram_name = value
            del self.pictogram

    @volatile_property
    def pictogram(self):
        """Resolved pictogram object"""
        if not self._pictogram_name:
            return None
        table = query_utility(IPictogramTable)
        if table is None:
            return None
        return table.get(self._pictogram_name)

    @property
    def target(self):
        """Anchor target getter"""
        if not self.anchor:
            return None
        container = get_parent(self, IParagraphContainer)
        if container is None:
            return None
        return container.get(self.anchor)


@subscriber(IObjectAddedEvent, context_selector=IMilestoneInfo)
@subscriber(IObjectModifiedEvent, context_selector=IMilestoneInfo)
@subscriber(IObjectRemovedEvent, context_selector=IMilestoneInfo)
def handle_modified_milestone(event):
    """Notify container on added, modified or removed milestone"""
    container = get_parent(event.object, IMilestonesContainer)
    if container is not None:
        registry = get_pyramid_registry()
        registry.notify(ObjectModifiedEvent(container))


@adapter_config(required=IMilestoneInfo,
                provides=IViewContextPermissionChecker)
class MilestonePermissionChecker(ContextAdapter):
    """Milestone permission checker"""

    @property
    def edit_permission(self):
        container = get_parent(self.context, IMilestonesContainer)
        if container is not None:
            return IViewContextPermissionChecker(container).edit_permission
        return None


@implementer(IMilestonesContainer)
class MilestonesContainer(BTreeOrderedContainer):
    """Milestones container"""

    def get_visible_items(self):
        """Get iterator over visible items"""
        yield from filter(lambda x: x.visible, self.values())


@adapter_config(required=IMilestonesContainer,
                provides=IViewContextPermissionChecker)
class MilestonesContainerPermissionChecker(ContextAdapter):
    """Milestones container permission checker"""

    edit_permission = MANAGE_TEMPLATE_PERMISSION


@factory_config(IMilestonesParagraph)
@factory_config(IBaseParagraph, name=MILESTONES_PARAGRAPH_TYPE)
class MilestonesParagraph(MilestonesContainer, BaseParagraph):
    """Milestones paragraph"""

    factory_name = MILESTONES_PARAGRAPH_TYPE
    factory_label = MILESTONES_PARAGRAPH_NAME
    factory_intf = IMilestonesParagraph

    icon_class = MILESTONES_PARAGRAPH_ICON_CLASS
    secondary = True

    renderer = FieldProperty(IMilestonesParagraph['renderer'])


@adapter_config(required=IMilestonesParagraph,
                provides=IViewContextPermissionChecker)
class MilestonesParagraphPermissionChecker(ParagraphPermissionChecker):
    """Milestones paragraph permission checker"""


@vocabulary_config(name=MILESTONES_PARAGRAPH_RENDERERS)
class MilestonesParagraphRenderersVocabulary(RenderersVocabulary):
    """Milestones paragraph renderers vocabulary"""

    content_interface = IMilestonesParagraph
