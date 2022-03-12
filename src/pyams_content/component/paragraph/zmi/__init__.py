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

"""PyAMS_content.component.paragraph.zmi module

This module provides base paragraphs management components.
"""
from zope.interface import implementer

from pyams_content.component.association import IAssociationContainer
from pyams_content.component.association.zmi import IAssociationsTable
from pyams_content.component.paragraph import IBaseParagraph, IParagraphContainer, \
    IParagraphContainerTarget
from pyams_content.component.paragraph.interfaces import IParagraphFactorySettings, \
    IParagraphFactorySettingsTarget, PARAGRAPH_HIDDEN_FIELDS
from pyams_content.component.paragraph.zmi.helper import get_json_paragraph_toolbar_refresh_event
from pyams_content.component.paragraph.zmi.interfaces import IInnerParagraphEditForm, \
    IParagraphAddForm, IParagraphContainerBaseTable, IParagraphContainerFullTable, \
    IParagraphContainerView, IParagraphRendererSettingsEditForm
from pyams_content.feature.renderer import IRendererSettings
from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.shared.common import IWfSharedContent
from pyams_content.zmi.interfaces import IPropertiesEditForm
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.interfaces import PREVIEW_MODE
from pyams_portal.skin.page import PortalContextPreviewPage
from pyams_portal.zmi.portlet import PortletRendererSettingsEditForm
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.schema.button import ActionButton
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_utils.adapter import ContextRequestViewAdapter, NullAdapter, adapter_config
from pyams_utils.factory import get_object_factory
from pyams_utils.request import get_annotations
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.manager import get_label, viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_refresh_callback, \
    get_json_table_row_add_callback, \
    get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IEditFormButtons, IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IPropertiesMenu, \
    IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_hint, get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem
from pyams_zmi.zmi.viewlet.toolbar import AddingsViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='paragraph-types.menu',
                context=IParagraphFactorySettingsTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=610,
                permission=MANAGE_TOOL_PERMISSION)
class ParagraphFactorySettingsMenu(NavigationMenuItem):
    """Paragraph factory settings menu"""

    label = _("Paragraphs types")
    href = '#paragraph-types.html'


@ajax_form_config(name='paragraph-types.html',
                  context=IParagraphFactorySettingsTarget, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class ParagraphFactorySettingsEditForm(AdminEditForm):
    """Paragraph factory settings edit form"""

    title = _("Paragraph types")
    legend = _("Shared content paragraph types")

    fields = Fields(IParagraphFactorySettings)

    def get_content(self):
        """Content getter"""
        return IParagraphFactorySettings(self.context)


#
# Paragraph add menu
#

@viewletmanager_config(name='pyams.context_addings',
                       context=IParagraphContainerTarget, layer=IAdminLayer,
                       view=IParagraphContainerBaseTable, manager=IToolbarViewletManager, weight=10,
                       provides=IContextAddingsViewletManager)
class ParagraphContainerAddingsViewletManager(AddingsViewletManager):
    """Paragraph container addings viewlet manager"""

    def sort(self, viewlets):
        """Viewlets sorter"""

        def get_sort_order(viewlet):
            menu = viewlet[1]
            if isinstance(menu, MenuDivider):
                return getattr(menu, 'weight', 500), None
            factory = get_object_factory(IBaseParagraph, name=menu.factory_name)
            if factory.factory.secondary:
                return 900, get_label(viewlet, self.request)
            return getattr(menu, 'weight', 500), get_label(viewlet, self.request)

        return sorted(viewlets, key=get_sort_order)


@viewlet_config(name='paragraphs.divider',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable, manager=IContextAddingsViewletManager, weight=500)
class ParagraphAddMenuDivider(ProtectedViewObjectMixin, MenuDivider):
    """Paragraph add menu divider"""

    def __new__(cls, context, request, view, manager):
        target = get_parent(context, IParagraphFactorySettingsTarget)
        if target is None:
            return MenuDivider.__new__(cls)
        has_primary = False
        has_secondary = False
        settings = IParagraphFactorySettings(target)
        for factory_name in settings.allowed_paragraphs or ():
            factory = get_object_factory(IBaseParagraph, name=factory_name)
            if factory is None:
                continue
            if factory.factory.secondary:
                has_secondary = True
            else:
                has_primary = True
            if has_primary and has_secondary:
                return MenuDivider.__new__(cls)
        return None


class BaseParagraphAddMenu(ProtectedViewObjectMixin, MenuItem):
    """Base paragraph add menu"""

    factory_name = None
    modal_target = True

    def __new__(cls, context, request, view, manager):
        target = get_parent(context, IParagraphFactorySettingsTarget)
        if target is not None:
            settings = IParagraphFactorySettings(target)
            if cls.factory_name not in (settings.allowed_paragraphs or ()):
                return None
        return MenuItem.__new__(cls)

    def get_href(self):
        container = IParagraphContainer(self.context)
        return absolute_url(container, self.request, self.href)


@implementer(IParagraphAddForm)
class BaseParagraphAddForm(AdminModalAddForm):
    """Base paragraph add form"""

    prefix = 'addform.'
    legend = _("New paragraph properties")
    modal_class = 'modal-xl'

    @property
    def fields(self):
        """Form fields getter"""
        return Fields(self.content_factory).omit(*PARAGRAPH_HIDDEN_FIELDS) + \
            Fields(self.content_factory).select('renderer')

    def add(self, obj):
        """Add paragraph to container"""
        IParagraphContainer(self.context).append(obj)


@adapter_config(required=(IParagraphContainer, IAdminLayer, IParagraphAddForm),
                provides=IFormTitle)
def paragraph_add_form_title(context, request, view):
    """Paragraph add form title"""
    translate = request.localizer.translate
    parent = get_parent(context, IParagraphContainerTarget)
    parent_label = translate(_("{}: {}")).format(get_object_hint(parent, request, view),
                                                 get_object_label(parent, request, view))
    factory = get_object_factory(view.content_factory)
    label = translate(_("New paragraph: {}")).format(factory.factory.factory_label)
    return f'<small>{parent_label}</small><br />{label}'


@adapter_config(required=(IParagraphContainer, IAdminLayer, IParagraphAddForm),
                provides=IAJAXFormRenderer)
class ParagraphAddFormRenderer(ContextRequestViewAdapter):
    """Paragraph add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        target = get_parent(self.context, IParagraphContainerTarget)
        table_factory = IParagraphContainerFullTable if IWfSharedContent.providedBy(target) \
            else IParagraphContainerBaseTable
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                table_factory, changes)
            ]
        }


#
# Paragraphs edit forms
#

@implementer(IPropertiesEditForm)
class ParagraphPropertiesEditFormMixin:
    """Paragraph properties edit form mixin"""

    legend = _("Paragraph properties")

    label_css_class = 'col-sm-2 col-md-3'
    input_css_class = 'col-sm-10 col-md-9'

    @property
    def prefix(self):
        """Form prefix getter"""
        return f'form_{self.context.__name__}.'

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(self.context.factory_intf).omit(*PARAGRAPH_HIDDEN_FIELDS) + \
            Fields(self.context.factory_intf).select('renderer')
        fields['renderer'].widget_factory = RendererSelectFieldWidget
        return fields


class IInnerParagraphEditFormButtons(IEditFormButtons):
    """Inner paragraph edit form buttons interface"""

    preview = ActionButton(name='preview',
                           title=_("Preview"))


@adapter_config(required=(IBaseParagraph, IAdminLayer),
                provides=IInnerParagraphEditForm)
class InnerParagraphPropertiesEditForm(ParagraphPropertiesEditFormMixin, AdminEditForm):
    """Default inner paragraph edit form"""

    buttons = Buttons(IInnerParagraphEditFormButtons)
    ajax_form_handler = 'properties.json'

    def update_actions(self):
        """Actions update"""
        super().update_actions()
        preview = self.actions.get('preview')
        if preview is not None:
            preview.icon_class = 'fas fa-binoculars'
            preview.icon_only = True
            preview.href = absolute_url(self.context, self.request, 'modal-preview.html')
            preview.modal_target = True
            preview.hint = self.request.localizer.translate(_("Preview"))

    @handler(IInnerParagraphEditFormButtons['apply'])
    def handle_apply(self, action):
        """Apply button handler"""
        super().handle_apply(self, action)


@adapter_config(required=(IBaseParagraph, IAdminLayer, IParagraphContainerBaseTable),
                provides=ITableElementEditor)
class BaseParagraphTableElementEditor(TableElementEditor):
    """Base paragraph table element editor"""


@adapter_config(required=(IBaseParagraph, IAdminLayer, IParagraphContainerFullTable),
                provides=ITableElementEditor)
class BaseParagraphFullTableElementEditor(NullAdapter):
    """Base paragraph full table element editor"""


@ajax_form_config(name='properties.html',
                  context=IBaseParagraph, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ParagraphPropertiesEditForm(ParagraphPropertiesEditFormMixin, AdminModalEditForm):
    """Paragraph properties edit form"""

    modal_class = 'modal-xl'


@adapter_config(name='main',
                required=(IBaseParagraph, IAdminLayer, ParagraphPropertiesEditFormMixin),
                provides=IAJAXFormRenderer)
class BaseParagraphPropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Base paragraph properties edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        result = {}
        if changes:
            event = get_json_paragraph_toolbar_refresh_event(self.context, self.request)
            if event is not None:
                result.setdefault('callbacks', []).append(event)
        if 'title' in changes.get(IBaseParagraph, ()):
            result.setdefault('callbacks', []).append({
                'callback': 'MyAMS.content.paragraphs.refreshTitle',
                'options': {
                    'element_name': self.context.__name__,
                    'title': get_object_label(self.context, self.request)
                }
            })
        if 'renderer' in changes.get(self.context.factory_intf, ()):
            result.setdefault('callbacks', []).append(
                get_json_widget_refresh_callback(self.view, 'renderer', self.request))
            renderer = self.context.get_renderer(self.request)
            if (renderer is not None) and (renderer.settings_interface is not None):
                translate = self.request.localizer.translate
                result['closeForm'] = False
                result['messagebox'] = {
                    'status': 'info',
                    'title': translate(_("Updated renderer")),
                    'message': translate(_("You changed renderer selection. Don't omit to "
                                           "check renderer properties...")),
                    'timeout': 5000
                }
        container = IAssociationContainer(self.context, None)
        if container is not None:
            result.setdefault('callbacks', []).append(
                get_json_table_refresh_callback(container, self.request, IAssociationsTable))
        return result


#
# Paragraph renderer properties
#

@ajax_form_config(name='renderer-settings.html',
                  context=IBaseParagraph, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
@implementer(IParagraphRendererSettingsEditForm)
class BaseParagraphRendererSettingsEditForm(PortletRendererSettingsEditForm):
    """Base paragraph renderer settings edit form"""

    @property
    def title(self):
        """Title getter"""
        translate = self.request.localizer.translate
        return translate(_("<small>Paragraph: {paragraph}</small><br />"
                           "Renderer: {renderer}")).format(
            paragraph=II18n(self.context).query_attribute('title', request=self.request) or '--',
            renderer=translate(self.renderer.label))

    def get_content(self):
        """Content getter"""
        renderer = self.context.get_renderer(self.request)
        if renderer.settings_interface is None:
            return None
        return IRendererSettings(self.context)


#
# Paragraph preview
#

@pagelet_config(name='preview.html',
                context=IBaseParagraph, request_type=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class ParagraphPreviewPage(PortalContextPreviewPage):
    """Paragraph preview page"""

    def __init__(self, context, request):
        super().__init__(context, request)
        self.renderer = context.get_renderer(request)

    def update(self):
        """Page update"""
        get_annotations(self.request)[PREVIEW_MODE] = True
        if self.renderer is not None:
            self.renderer.update()

    def render(self):
        """Page renderer"""
        if self.renderer is not None:
            return self.renderer.render()
        return ''