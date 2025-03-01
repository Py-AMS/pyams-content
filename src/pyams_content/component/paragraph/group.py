# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.component.paragraph.interfaces.group import GROUP_PARAGRAPH_ICON_CLASS, GROUP_PARAGRAPH_NAME, \
    GROUP_PARAGRAPH_RENDERERS, \
    GROUP_PARAGRAPH_TYPE, IParagraphsGroup
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(IParagraphsGroup)
@factory_config(IBaseParagraph, name=GROUP_PARAGRAPH_TYPE)
class ParagraphsGroup(BaseParagraph):
    """Paragraphs group persistent class"""
    
    factory_name = GROUP_PARAGRAPH_TYPE
    factory_label = GROUP_PARAGRAPH_NAME
    factory_intf = IParagraphsGroup
    
    secondary = True
    
    icon_class = GROUP_PARAGRAPH_ICON_CLASS

    renderer = FieldProperty(IParagraphsGroup['renderer'])


@vocabulary_config(name=GROUP_PARAGRAPH_RENDERERS)
class ParagraphsGroupRenderersVocabulary(RenderersVocabulary):
    """Paragraphs group renderers vocabulary"""

    content_interface = IParagraphsGroup
