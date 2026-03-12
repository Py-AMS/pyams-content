# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from ZODB.interfaces import IBroken

from pyams_content.component.paragraph.interfaces import IParagraphContainer, IParagraphContainerItems
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import ContextRequestAdapter, adapter_config

__docformat__ = 'restructuredtext'


@adapter_config(required=(IParagraphContainer, IPyAMSLayer),
                provides=IParagraphContainerItems)
class ParagraphContainerItems(ContextRequestAdapter):
    """Paragraph container items adapter"""

    def get_visible_paragraphs(self, names=None, anchors_only=False, exclude_anchors=False,
                               factories=None, excluded_factories=None, limit=None, **kwargs):
        """Visible paragraphs getter"""
        count = 0
        if names:
            for name in names:
                paragraph = self.context.get(name)
                if ((paragraph is None) or
                        IBroken.providedBy(paragraph) or
                        not paragraph.visible):
                    continue
                yield paragraph
                count += 1
                if limit and (count == limit):
                    return
        else:
            for paragraph in self.context.values():
                if (IBroken.providedBy(paragraph) or not paragraph.visible) or \
                        (anchors_only and not paragraph.anchor) or \
                        (exclude_anchors and paragraph.anchor) or \
                        (factories and (paragraph.factory_name not in factories)) or \
                        (excluded_factories and (paragraph.factory_name in excluded_factories)):
                    continue
                yield paragraph
                count += 1
                if limit and (count == limit):
                    return
