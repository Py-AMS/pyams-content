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

"""PyAMS_content.component.paragraph.skin module

This module defines generic components used to handle paragraphs renderers settings.
"""

from zope.traversing.interfaces import ITraversable

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.feature.renderer import IRendererSettings
from pyams_content.feature.renderer.interfaces import RENDERER_SETTINGS_KEY
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter


__docformat__ = 'restructuredtext'


@adapter_config(required=IBaseParagraph,
                provides=IRendererSettings)
def paragraph_renderer_settings(context):
    """Paragraph renderer settings adapter"""
    renderer = context.get_renderer()
    if renderer is None:
        return None
    return get_annotation_adapter(context,
                                  f'{RENDERER_SETTINGS_KEY}::{context.renderer}',
                                  renderer.settings_interface, name='++renderer++')


@adapter_config(name='renderer',
                required=IBaseParagraph,
                provides=ITraversable)
class ParagraphRendererSettingsTraverser(ContextAdapter):
    """Paragraph renderer settings traverser"""

    def traverse(self, name, furtherpath=None):
        """Traverse paragraph to renderer settings"""
        return IRendererSettings(self.context)
