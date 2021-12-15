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

"""PyAMS_content.shared.common.zmi module

This module defines base management components for all shared contents.
"""

from uuid import uuid4

from pyramid.events import subscriber
from pyramid.location import lineage
from zope.interface import Interface
from zope.lifecycleevent import ObjectCreatedEvent

from pyams_content.interfaces import CREATE_CONTENT_PERMISSION, IBaseContent, \
    MANAGE_CONTENT_PERMISSION, MANAGE_SITE_ROOT_PERMISSION, PUBLISH_CONTENT_PERMISSION
from pyams_content.shared.common import IWfSharedContent, WfSharedContent
from pyams_content.shared.common.interfaces import IContributorRestrictions, IManagerRestrictions, \
    ISharedTool, IWfSharedContentRoles
from pyams_content.zmi.properties import PropertiesEditForm
from pyams_content.zmi.widget.seo import I18nSEOTextLineFieldWidget
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_i18n.interfaces import II18n, II18nManager, INegotiator
from pyams_i18n_views.zmi.manager import I18nManagerLanguagesEditForm
from pyams_layer.interfaces import IFormLayer, IPyAMSLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.interfaces.base import FORBIDDEN_PERMISSION, VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.viewlet import IBreadcrumbItem
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.request import check_request
from pyams_utils.url import absolute_url, generate_url
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowInfo, IWorkflowState, IWorkflowVersions
from pyams_zmi.form import AdminModalAddForm
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader, \
    INavigationViewletManager, IPropertiesMenu, \
    ISiteManagementMenu, IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.zmi.viewlet.menu import NavigationMenuHeaderDivider, NavigationMenuItem, \
    SiteManagementMenu


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-content.action',
                context=ISharedTool, layer=IAdminLayer,
                manager=IToolbarViewletManager, weight=10,
                permission=CREATE_CONTENT_PERMISSION)
class SharedContentAddAction(ContextAddAction):
    """Shared content add action"""

    @property
    def label(self):
        translate = self.request.localizer.translate
        factory = self.context.shared_content_factory
        return translate(_("Add new: {}")).format(
            translate(factory.factory.content_name).lower())

    href = 'add-shared-content.html'


@ajax_form_config(name='add-shared-content.html',
                  context=ISharedTool, layer=IFormLayer,
                  permission=CREATE_CONTENT_PERMISSION)
class SharedContentAddForm(AdminModalAddForm):
    """Shared content add form"""

    @property
    def title(self):
        translate = self.request.localizer.translate
        factory = self.content_factory
        return '<small>{}</small><br />{}'.format(
            II18n(self.context).query_attribute('title', request=self.request),
            translate(_("Add new content: {}")).format(
                translate(factory.factory.content_name).lower()))

    legend = _("New content properties")

    fields = Fields(IWfSharedContent).select('title', 'notepad')
    fields['title'].widget_factory = I18nSEOTextLineFieldWidget

    _edit_permission = CREATE_CONTENT_PERMISSION

    @property
    def content_factory(self):
        """Shared content factory"""
        return self.context.shared_content_factory.factory.content_factory

    def update_content(self, obj, data):
        super().update_content(obj, data)
        # initialize content fields
        lang = get_utility(INegotiator).server_language
        obj.creator = self.request.principal.id
        IWfSharedContentRoles(obj).owner = self.request.principal.id
        obj.short_name = obj.title.copy()
        obj.content_url = generate_url(obj.title.get(lang, ''))
        # init content languages
        languages = II18nManager(self.context).languages
        if languages:
            II18nManager(obj).languages = languages.copy()

    def add(self, obj):
        factory = self.context.shared_content_factory
        if factory is not None:
            content = factory()
            self.request.registry.notify(ObjectCreatedEvent(content))
            self.__uuid = uuid = str(uuid4())
            self.context[uuid] = content
            IWorkflowVersions(content).add_version(obj, None)
            IWorkflowInfo(obj).fire_transition('init', comment=obj.notepad)

    def next_url(self):
        return absolute_url(self.context, self.request,
                            f'{self.__uuid}/++versions++/1/admin')


@adapter_config(required=(ISharedTool, IAdminLayer, SharedContentAddForm),
                provides=IAJAXFormRenderer)
class SharedToolAddFormRenderer(AJAXFormRenderer):
    """Shared tool add form renderer"""

    def render(self, changes):
        return {
            'status': 'redirect',
            'location': self.form.next_url()
        }


#
# Shared content properties edit form
#

@adapter_config(required=IWfSharedContent,
                provides=IViewContextPermissionChecker)
class SharedContentPermissionChecker(ContextAdapter):
    """Shared content form permission checker"""

    @property
    def edit_permission(self):
        context = self.context
        workflow = IWorkflow(context)
        state = IWorkflowState(context).state
        # forbidden access to all for archived contents
        if state in workflow.readonly_states:
            return FORBIDDEN_PERMISSION
        # only webmaster can update published contents
        if state in workflow.protected_states:
            return MANAGE_SITE_ROOT_PERMISSION
        # webmaster access
        request = check_request()
        if request.has_permission(MANAGE_SITE_ROOT_PERMISSION, context=context):
            return MANAGE_SITE_ROOT_PERMISSION
        principal_id = request.principal.id
        roles = IWfSharedContentRoles(context)
        # access is granted to content's owner and designated contributors or managers
        if principal_id in roles.owner | roles.contributors | roles.managers:
            return MANAGE_CONTENT_PERMISSION
        # restricted manager access
        if state in workflow.manager_states:
            if principal_id in roles.managers:
                return PUBLISH_CONTENT_PERMISSION
            for parent in lineage(context):
                manager_restrictions = IManagerRestrictions(parent, None)
                if manager_restrictions is not None:
                    if manager_restrictions.can_access(context,
                                                       permission=PUBLISH_CONTENT_PERMISSION,
                                                       request=request):
                        return PUBLISH_CONTENT_PERMISSION
            return FORBIDDEN_PERMISSION
        # check if current principal can manage owner's contents
        for parent in lineage(context):
            contrib_restrictions = IContributorRestrictions(parent, None)
            if contrib_restrictions is not None:
                if contrib_restrictions.can_access(context,
                                                   permission=MANAGE_CONTENT_PERMISSION,
                                                   request=request):
                    return MANAGE_CONTENT_PERMISSION
        restrictions = IContributorRestrictions(context)
        if restrictions and restrictions.can_access(context,
                                                    permission=MANAGE_CONTENT_PERMISSION,
                                                    request=request):
            return MANAGE_CONTENT_PERMISSION
        # check if current principal can manage content's due to manager restrictions
        for parent in lineage(self.context):
            manager_restrictions = IManagerRestrictions(parent, None)
            if manager_restrictions is not None:
                if manager_restrictions.can_access(self.context,
                                                   permission=MANAGE_CONTENT_PERMISSION,
                                                   request=request):
                    return MANAGE_CONTENT_PERMISSION
        restrictions = IManagerRestrictions(self.context)
        if restrictions and restrictions.can_access(self.context,
                                                    permission=MANAGE_CONTENT_PERMISSION,
                                                    request=request):
            return MANAGE_CONTENT_PERMISSION
        return FORBIDDEN_PERMISSION


@adapter_config(required=(IWfSharedContent, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class SharedContentBreadcrumbItem(BreadcrumbItem):
    """Shared content breadcrumb item"""

    @property
    def label(self):
        return II18n(self.context).query_attribute('title', request=self.request)

    view_name = 'admin'


@adapter_config(required=(IWfSharedContent, IAdminLayer, Interface),
                provides=ITableElementEditor)
class SharedContentElementEditor(TableElementEditor):
    """Shared content element editor"""

    view_name = 'admin'
    modal_target = False


@adapter_config(required=(IWfSharedContent, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def shared_content_management_menu_header(context, request, view, manager):
    """Shared content management menu header"""
    return request.localizer.translate(_("Content management"))


@viewletmanager_config(name='content.menu',
                       context=IWfSharedContent, layer=IAdminLayer,
                       manager=IContentManagementMenu, weight=10,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IPropertiesMenu)
class SharedContentCompositionMenu(NavigationMenuItem):
    """Shared content composition menu"""

    label = _("Composition")
    icon_class = 'fab fa-dropbox'
    url = '#'


@viewlet_config(name='properties.menu',
                context=IWfSharedContent, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=10,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedContentPropertiesMenu(NavigationMenuItem):
    """Shared content properties menu"""

    label = _("Properties")
    href = '#properties.html'


@ajax_form_config(name='properties.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SharedContentPropertiesEditForm(PropertiesEditForm):
    """Shared content properties edit form"""

    title = _("Content properties")
    legend = _("Main content properties")

    interface = IWfSharedContent
    fieldnames = ('title', 'short_name', 'content_url', 'header', 'description', 'notepad')

    @property
    def fields(self):
        fields = Fields(self.interface).select(*self.fieldnames)
        if 'title' in fields:
            fields['title'].widget_factory = I18nSEOTextLineFieldWidget
        for name in self.fieldnames:
            if (name in fields) and not getattr(self.context, f'handle_{name}', True):
                fields = fields.omit(name)
        return fields


@subscriber(IDataExtractedEvent, form_selector=SharedContentPropertiesEditForm)
def handle_content_properties_data_extraction(event):
    """Automatically set short_name as title"""
    data = event.data
    if not getattr(event.form.context, 'handle_short_name', True):
        data['short_name'] = data['title'].copy()
    if 'content_url' in data:
        data['content_url'] = generate_url(data['content_url'])


@adapter_config(required=(IWfSharedContent, IAdminLayer, SharedContentPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SharedContentPropertiesEditFormRenderer(AJAXFormRenderer):
    """Shared content properties edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if 'title' in changes.get(IBaseContent, ()):
            return {
                'status': 'redirect'
            }
        return super().render(changes)


@adapter_config(name='main',
                required=(IWfSharedContent, IAdminLayer, SharedContentPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SharedContentPropertiesEditFormRenderer(ContextRequestViewAdapter):

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        result = {}
        if 'content_url' in changes.get(IWfSharedContent, ()):
            result['callbacks'] = [
                get_json_widget_refresh_callback(self.view, 'content_url', self.request)
            ]
        return result


@viewlet_config(name='site-manager.menu.divider',
                context=IWfSharedContent, layer=IAdminLayer,
                manager=INavigationViewletManager, weight=199)
class SharedContentSiteManagementMenuDivider(NavigationMenuHeaderDivider):
    """Shared content site management menu divider"""


@viewletmanager_config(name='site-manager.menu',
                       context=IWfSharedContent, layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=200,
                       provides=ISiteManagementMenu)
class SharedContentSiteManagementMenu(SiteManagementMenu):
    """Shared content site management menu header"""

    header = None


@adapter_config(required=(WfSharedContent, IAdminLayer, I18nManagerLanguagesEditForm),
                provides=IViewContextPermissionChecker)
class SharedContentLanguagesEditFormPermissionChecker(ContextRequestViewAdapter):
    """Shared tool languages edit form permission checker"""

    @property
    def edit_permission(self):
        return SharedContentPermissionChecker(self.context).edit_permission
