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

"""PyAMS_content.component.milestone.zmi module

This module provides back-office management views for milestones.
"""

from pyramid.view import view_config
from zope.interface import Interface, implementer

from pyams_content.component.milestone.interfaces import IMilestoneInfo, IMilestonesContainer, \
    IMilestonesParagraph, MILESTONES_PARAGRAPH_ICON_CLASS, MILESTONES_PARAGRAPH_NAME, \
    MILESTONES_PARAGRAPH_TYPE
from pyams_content.component.paragraph.interfaces import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu
from pyams_content.component.paragraph.zmi.interfaces import IParagraphContainerBaseTable
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.interfaces.view import IModalPage
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config, query_adapter
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.text import get_text_start
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.helper.event import get_json_table_row_add_callback, get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IToolbarViewletManager
from pyams_zmi.table import I18nColumnMixin, InnerTableAdminView, NameColumn, ReorderColumn, SortableTable, \
    TableElementEditor, TrashColumn, VisibilityColumn
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


class MilestonesTable(SortableTable):
    """Milestones table"""

    container_class = IMilestonesContainer

    display_if_empty = True


@adapter_config(required=(IMilestonesContainer, IAdminLayer, MilestonesTable),
                provides=IValues)
class MilestonesTableValues(ContextRequestViewAdapter):
    """Milestones table values adapter"""

    @property
    def values(self):
        """Milestones table values getter"""
        yield from self.context.values()


@adapter_config(name='reorder',
                required=(IMilestonesContainer, IAdminLayer, MilestonesTable),
                provides=IColumn)
class MilestonesTableReorderColumn(ReorderColumn):
    """Milestones table reorder column"""


@view_config(name='reorder.json',
             context=IMilestonesContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
@view_config(name='reorder.json',
             context=IMilestonesParagraph, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_CONTENT_PERMISSION)
def reorder_milestones_table(request):
    """Reorder milestones table"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IMilestonesContainer, IAdminLayer, MilestonesTable),
                provides=IColumn)
class MilestonesTableVisibleColumn(VisibilityColumn):
    """Milestones table visible column"""

    hint = _("Click icon to show or hide milestone")


@view_config(name='switch-visible-item.json',
             context=IMilestonesContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_milestone(request):
    """Switch visible milestone"""
    return switch_element_attribute(request)


@adapter_config(name='title',
                required=(IMilestonesContainer, IAdminLayer, MilestonesTable),
                provides=IColumn)
class MilestonesTableTitleColumn(NameColumn):
    """Milestones table title column"""

    i18n_header = _("Title")


@adapter_config(name='header',
                required=(IMilestonesContainer, IAdminLayer, MilestonesTable),
                provides=IColumn)
class MilestonesTableHeaderColumn(I18nColumnMixin, GetAttrColumn):
    """Milestones table header column"""

    i18n_header = _('milestone-header', default="Header")
    attr_name = 'header'

    weight = 20

    def get_value(self, obj):
        return get_text_start(II18n(obj).query_attribute(self.attr_name, request=self.request), 30, 10) or MISSING_INFO


@adapter_config(name='trash',
                required=(IMilestonesContainer, IAdminLayer, MilestonesTable),
                provides=IColumn)
class MilestonesTableTrashColumn(TrashColumn):
    """Milestones table trash column"""


@view_config(name='delete-element.json',
             context=IMilestonesContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
def delete_milestone(request):
    """Delete milestone"""
    return delete_container_element(request)


@viewlet_config(name='milestones-content-table',
                context=IMilestonesContainer, layer=IAdminLayer,
                view=IPropertiesEditForm,
                manager=IContentSuffixViewletManager, weight=10)
class MilestonesTableView(InnerTableAdminView):
    """Milestones table view"""

    table_class = MilestonesTable
    table_label = _("List of milestones")


#
# Milestone add/edit forms
#

@viewlet_config(name='add-milestone.menu',
                context=IMilestonesContainer, layer=IAdminLayer, view=MilestonesTable,
                manager=IToolbarViewletManager, weight=10)
class MilestoneAddAction(ProtectedViewObjectMixin, ContextAddAction):
    """Milestone add action"""

    label = _("Add milestone")
    href = 'add-milestone.html'


class IMilestoneForm(Interface):
    """Milestone form marker interface"""


@ajax_form_config(name='add-milestone.html',
                  context=IMilestonesContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
@implementer(IMilestoneForm)
class MilestoneAddForm(AdminModalAddForm):
    """Milestone add form"""

    subtitle = _("New milestone")
    legend = _("New milestone properties")
    modal_class = 'modal-xl'

    fields = Fields(IMilestoneInfo).select('title', 'header', 'body', 'pictogram_name', 'anchor')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IMilestoneInfo

    def add(self, obj):
        self.context.append(obj)


@adapter_config(required=(IMilestonesContainer, IAdminLayer, MilestoneAddForm),
                provides=IAJAXFormRenderer)
class MilestoneAddFormRenderer(ContextRequestViewAdapter):
    """Milestone add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                MilestonesTable, changes)
            ]
        }


@adapter_config(required=(IMilestoneInfo, IAdminLayer, Interface),
                provides=ITableElementEditor)
class MilestoneElementEditor(TableElementEditor):
    """Milestone element editor"""


@ajax_form_config(name='properties.html',
                  context=IMilestoneInfo, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
@implementer(IMilestoneForm)
class MilestoneEditForm(AdminModalEditForm):
    """Milestone properties edit form"""

    @property
    def subtitle(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        return translate(_("Milestone: {}")).format(
            get_object_label(self.context, self.request, self))

    legend = _("Milestone properties")
    modal_class = 'modal-xl'

    fields = Fields(IMilestoneInfo).select('title', 'header', 'body', 'pictogram_name', 'anchor')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget


@adapter_config(required=(IMilestoneInfo, IAdminLayer, IModalPage),
                provides=IFormTitle)
def milestone_edit_form_title(context, request, view):
    """Milestone edit form title"""
    settings = get_parent(context, IMilestonesContainer)
    return query_adapter(IFormTitle, request, settings, view)


@adapter_config(required=(IMilestoneInfo, IAdminLayer, MilestoneEditForm),
                provides=IAJAXFormRenderer)
class MilestoneEditFormRenderer(ContextRequestViewAdapter):
    """Milestone edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(self.context.__parent__, self.request,
                                                    MilestonesTable, self.context)
            ]
        }


#
# Milestones paragraph forms
#

@viewlet_config(name='add-milestones-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=610)
class MilestonesParagraphAddMenu(BaseParagraphAddMenu):
    """Milestones paragraph add menu"""

    label = MILESTONES_PARAGRAPH_NAME
    icon_class = MILESTONES_PARAGRAPH_ICON_CLASS

    factory_name = MILESTONES_PARAGRAPH_TYPE
    href = 'add-milestones-paragraph.html'


@ajax_form_config(name='add-milestones-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class MilestonesParagraphAddForm(BaseParagraphAddForm):
    """Milestones paragraph add form"""

    content_factory = IMilestonesParagraph
