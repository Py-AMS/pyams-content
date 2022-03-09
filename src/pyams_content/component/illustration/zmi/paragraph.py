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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from pyams_content import _
from pyams_content.component.illustration import IIllustration, IIllustrationTarget
from pyams_content.component.paragraph.zmi import IParagraphContainerFullTable
from pyams_content.component.paragraph.zmi.container import ParagraphTitleToolbarItemMixin
from pyams_content.component.paragraph.zmi.interfaces import IParagraphTitleToolbar
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer


@viewlet_config(name='illustration',
                context=IIllustrationTarget, request=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=10)
class IllustrationTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """Paragraph illustration marker toolbar viewlet"""

    icon_class = 'far fa-image'
    icon_hint = _("Illustration")

    target_intf = IIllustration

    def update(self):
        illustration = self.target_intf(self.context, None)
        if (illustration is not None) and illustration.has_data():
            self.counter = 1
