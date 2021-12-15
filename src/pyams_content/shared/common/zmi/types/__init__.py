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

"""PyAMS_content.shared.common.zmi.types module

This module provides shared content data types management components.
"""

from pyramid.view import view_config
from zope.interface import Interface

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
from pyams_content.shared.common.interfaces.types import IDataType, ITypedDataManager, \
    ITypedSharedTool
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.data import ObjectDataManagerMixin
from pyams_utils.interfaces.intids import IUniqueID
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.helper.event import get_json_table_row_add_callback, \
    get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, IToolbarViewletManager
from pyams_zmi.table import JsActionColumn, NameColumn, ReorderColumn, Table, \
    TableAdminView, TableElementEditor, TrashColumn, get_ordered_data_attributes
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='data-types.menu',
                context=ITypedSharedTool, request=IAdminLayer,
                manager=IPropertiesMenu, weight=400,
                permission=MANAGE_TOOL_PERMISSION)
class SharedToolTypesMenu(NavigationMenuItem):
    """Shared tool data types menu"""

    label = _("Content types")
    href = '#data-types.html'


class SharedToolTypesTable(Table):
    """Shared tool data types table"""

    @property
    def data_attributes(self):
        attributes = super().data_attributes
        container = ITypedDataManager(self.context)
        get_ordered_data_attributes(attributes, container, self.request)
        return attributes

    display_if_empty = True


@adapter_config(required=(ITypedSharedTool, IAdminLayer, SharedToolTypesTable),
                provides=IValues)
class SharedToolTypesTableValues(ContextRequestViewAdapter):
    """Shared tool data types table values"""

    @property
    def values(self):
        """Data types values getter"""
        yield from ITypedDataManager(self.context).values()


@adapter_config(name='reorder',
                required=(ITypedSharedTool, IAdminLayer, SharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesReorderColumn(ReorderColumn):
    """Shared tool data types table reorder column"""


@view_config(name='reorder.json',
             context=ITypedDataManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TOOL_PERMISSION)
def reorder_types_table(request):
    """Reorder shared tool data types"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success'
    }


@adapter_config(name='visible',
                required=(ITypedSharedTool, IAdminLayer, SharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesVisibleColumn(ObjectDataManagerMixin, JsActionColumn):
    """Shared tool data types table visible column"""

    hint = _("Click icon to enable or disable content type")

    href = 'MyAMS.container.switchElementAttribute'
    modal_target = False

    object_data = {
        'ams-modules': 'container',
        'ams-update-target': 'switch-visible-item.json',
        'ams-attribute-name': 'visible',
        'ams-icon-on': 'far fa-eye',
        'ams-icon-off': 'far fa-eye-slash'
    }

    weight = 1

    def get_icon_class(self, item):
        """Icon class getter"""
        return 'far fa-eye' if item.visible else 'far fa-eye-slash'


@view_config(name='switch-visible-item.json',
             context=ITypedDataManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    return switch_element_attribute(request)


@adapter_config(name='label',
                required=(ITypedSharedTool, IAdminLayer, SharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesLabelColumn(NameColumn):
    """Shared tool data types table label column"""

    i18n_header = _("Label")


@adapter_config(name='trash',
                required=(ITypedSharedTool, IAdminLayer, SharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesTrashColumn(TrashColumn):
    """Shared tool data types table trash column"""


@view_config(name='delete-element.json',
             context=ITypedDataManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TOOL_PERMISSION)
def delete_data_type(request):
    """Delete data type"""
    return delete_container_element(request)


@pagelet_config(name='data-types.html',
                context=ITypedSharedTool, layer=IPyAMSLayer,
                permission=MANAGE_TOOL_PERMISSION)
class SharedToolTypesView(TableAdminView):
    """Shared tool data types view"""

    title = _("Content types")

    table_class = SharedToolTypesTable
    table_label = _("Shared tool content types list")


#
# Shared data types views
#

@adapter_config(required=(IDataType, IAdminLayer, Interface),
                provides=IObjectLabel)
def data_type_label(context, request, view):
    """Data type label"""
    i18n = II18n(context)
    return i18n.query_attribute('backoffice_label', request=request) or \
        i18n.query_attribute('label', request=request)


@adapter_config(required=(IDataType, IAdminLayer, SharedToolTypesTable),
                provides=ITableElementEditor)
class DataTypeEditor(TableElementEditor):
    """data type editor"""


@viewlet_config(name='add-data-type.action',
                context=ITypedSharedTool, layer=IAdminLayer, view=SharedToolTypesTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_TOOL_PERMISSION)
class DataTypesAddAction(ContextAddAction):
    """Data type add action"""

    label = _("Add content type")
    href = 'add-data-type.html'


@ajax_form_config(name='add-data-type.html',
                  context=ITypedSharedTool, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class DataTypeAddForm(AdminModalAddForm):
    """Data type add form"""

    @property
    def title(self):
        translate = self.request.localizer.translate
        return '<small>{}</small><br />{}'.format(
            II18n(self.context).query_attribute('title', request=self.request),
            translate(_("Add new content type")))

    legend = _("New data type properties")

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(IDataType).omit('__name__', '__parent__', 'visible')
        fields['pictogram'].widget_factory = PictogramSelectFieldWidget
        if not self.context.shared_content_types_fields:
            fields = fields.omit('field_names')
        return fields

    content_factory = IDataType

    def add(self, obj):
        oid = IUniqueID(obj).oid
        ITypedDataManager(self.context)[oid] = obj


@adapter_config(required=(ITypedSharedTool, IAdminLayer, DataTypeAddForm),
                provides=IAJAXFormRenderer)
class DataTypeAddFormRenderer(ContextRequestViewAdapter):
    """Data type add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                SharedToolTypesTable, changes)
            ]
        }


@ajax_form_config(name='properties.html',
                  context=IDataType, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class DataTypeEditForm(AdminModalEditForm):
    """Data type properties edit form"""

    @property
    def title(self):
        translate = self.request.localizer.translate
        tool = get_parent(self.context, ITypedSharedTool)
        return '<small>{}</small><br />{}'.format(
            II18n(tool).query_attribute('title', request=self.request),
            translate(_("Content type: {}")).format(get_object_label(self.context, self.request))
        )

    legend = _("Content type properties")

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(IDataType).omit('__name__', '__parent__', 'visible')
        fields['pictogram'].widget_factory = PictogramSelectFieldWidget
        tool = get_parent(self.context, ITypedSharedTool)
        if (tool is not None) and not tool.shared_content_types_fields:
            fields = fields.omit('field_names')
        return fields


@adapter_config(required=(IDataType, IAdminLayer, DataTypeEditForm),
                provides=IAJAXFormRenderer)
class DataTypeEditFormRenderer(ContextRequestViewAdapter):
    """Data type edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        tool = get_parent(self.context, ITypedSharedTool)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(tool, self.request,
                                                    SharedToolTypesTable, self.context)
            ]
        }
