#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.illustration.zmi module

"""

from pyramid.events import subscriber
from zope.component import getAdapter

from pyams_content.component.illustration.interfaces import IBaseIllustration, \
    IBaseIllustrationTarget, IIllustration, IIllustrationTarget, ILinkIllustrationTarget, \
    IParagraphIllustration
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.zmi import BaseParagraphRendererSettingsEditForm
from pyams_content.feature.renderer import IRendererSettings
from pyams_content.zmi.interfaces import IPropertiesEditForm
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent, IFormUpdatedEvent, \
    IInnerSubForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.zmi.portlet import PortletRendererSettingsEditForm
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.traversing import get_parent
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.utils import get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='illustration',
                required=(IBaseIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class BasicIllustrationPropertiesEditForm(FormGroupSwitcher):
    """Basic illustration properties edit form"""

    legend = _("Main illustration")
    weight = 10

    fields = Fields(IBaseIllustration)
    prefix = 'illustration.'

    def get_content(self):
        return IIllustration(self.context)

    @property
    def mode(self):
        return self.parent_form.mode

    @property
    def state(self):
        return 'open' if self.get_content().has_data() else 'closed'


@adapter_config(name='illustration',
                required=(IIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class IllustrationPropertiesEditForm(BasicIllustrationPropertiesEditForm):
    """Illustration properties edit form"""

    fields = Fields(IIllustration)
    fields['renderer'].widget_factory = RendererSelectFieldWidget

    @property
    def state(self):
        return super().state if IBaseParagraph.providedBy(self.context) else 'open'


@adapter_config(name='link-illustration',
                required=(ILinkIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class LinkIllustrationPropertiesEditForm(BasicIllustrationPropertiesEditForm):
    """Link illustration properties edit form"""

    legend = _("Navigation link illustration")
    weight = 15

    prefix = 'link_illustration.'

    def get_content(self):
        return getAdapter(self.context, IIllustration, name='link')


@adapter_config(required=(IBaseIllustrationTarget, IAdminLayer,
                          BasicIllustrationPropertiesEditForm),
                provides=IAJAXFormRenderer)
class BasicIllustrationPropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Basic illustration properties AJAX form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        result = {
            'status': 'success',
            'message': self.request.localizer.translate(self.view.parent_form.success_message)
        }
        if 'data' in changes.get(IBaseIllustration, ()):
            result['callbacks'] = [
                get_json_widget_refresh_callback(self.view, 'data', self.request)
            ]
        return result


@ajax_form_config(name='renderer-settings.html',
                  context=IParagraphIllustration, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ParagraphIllustrationRendererSettingsEditForm(BaseParagraphRendererSettingsEditForm):
    """Paragraph illustration renderer settings edit form"""

    @property
    def title(self):
        """Title getter"""
        translate = self.request.localizer.translate
        paragraph = get_parent(self.context, IBaseParagraph)
        return translate(_("<small>Paragraph: {paragraph}</small><br />"
                           "Renderer: {renderer}")).format(
            paragraph=get_object_label(paragraph, self.request, self),
            renderer=translate(self.renderer.label))


@adapter_config(required=(IParagraphIllustration, IAdminLayer,
                          ParagraphIllustrationRendererSettingsEditForm),
                provides=IFormContent)
def get_paragraph_illustration_renderer_settings_edit_form_content(context, request, form):
    """Paragraph illustration renderer settings edit form content getter"""
    return IRendererSettings(context)


@subscriber(IFormUpdatedEvent,
            context_selector=IBaseIllustration,
            form_selector=PortletRendererSettingsEditForm)
def handle_illustration_renderer_settings_edit_form_update(event):
    """Illustration renderer settings edit form update"""
    widgets = event.form.widgets
    thumb_selection = widgets.get('thumb_selection')
    if thumb_selection is not None:
        thumb_selection.no_value_message = _("Use responsive selection")
