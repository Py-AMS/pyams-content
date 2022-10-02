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

from pyams_content.component.illustration import IBaseIllustration, IIllustrationTarget
from pyams_content.component.illustration.interfaces import IIllustrationParagraph, \
    ILLUSTRATION_PARAGRAPH_ICON_CLASS, ILLUSTRATION_PARAGRAPH_NAME, ILLUSTRATION_PARAGRAPH_TYPE
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable, IParagraphContainerFullTable
from pyams_content.component.paragraph.zmi.container import ParagraphTitleToolbarItemMixin
from pyams_content.component.paragraph.zmi.interfaces import IParagraphTitleToolbar
from pyams_content.zmi.interfaces import IPropertiesEditForm
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='illustration',
                context=IIllustrationTarget, request=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=10)
@viewlet_config(name='illustration',
                context=IIllustrationParagraph, request=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=10)
class IllustrationTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """Paragraph illustration marker toolbar viewlet"""

    icon_class = 'far fa-image'
    icon_hint = _("Illustration")

    target_intf = IBaseIllustration

    def update(self):
        illustration = self.target_intf(self.context, None)
        if (illustration is not None) and illustration.has_data():
            self.counter = 1


@viewlet_config(name='add-illustration-paragraph.menu',
                context=IParagraphContainerTarget, request=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=60)
class IllustrationParagraphAddMenu(BaseParagraphAddMenu):
    """Illustration paragraph add menu"""

    label = ILLUSTRATION_PARAGRAPH_NAME
    icon_class = ILLUSTRATION_PARAGRAPH_ICON_CLASS

    factory_name = ILLUSTRATION_PARAGRAPH_TYPE
    href = 'add-illustration-paragraph.html'


@ajax_form_config(name='add-illustration-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class IllustrationParagraphAddForm(BaseParagraphAddForm):
    """Illustration paragraph add form"""

    content_factory = IIllustrationParagraph


@adapter_config(required=(IParagraphContainer, IAdminLayer, IllustrationParagraphAddForm),
                provides=IFormFields)
@adapter_config(required=(IIllustrationParagraph, IAdminLayer, IPropertiesEditForm),
                provides=IFormFields)
def illustration_form_fields(context, request, form):
    """Illustration form fields getter"""
    fields = Fields(IIllustrationParagraph).select('data', 'title', 'alt_title',
                                                   'description', 'author', 'renderer')
    if IIllustrationParagraph.providedBy(context):
        fields['renderer'].widget_factory = RendererSelectFieldWidget
    return fields
