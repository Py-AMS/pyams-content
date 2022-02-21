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

"""PyAMS_content.component.association.zmi.container module

This module provides a few components used for management of associations containers.
"""

from pyramid.view import view_config
from zope.interface import implementer

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.association.interfaces import IAssociationInfo
from pyams_content.component.association.zmi import IAssociationsTable
from pyams_content.component.association.zmi.interfaces import IAssociationsContainerEditForm
from pyams_content.shared.common.interfaces.types import ITypedSharedTool
from pyams_content.shared.common.zmi.types import SharedToolTypesTable
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalDisplayForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.table import ActionColumn, ContentTypeColumn, I18nColumnMixin, InnerTableAdminView, \
    NameColumn, ReorderColumn, Table, TrashColumn, VisibilityColumn, get_ordered_data_attributes
from pyams_zmi.utils import get_object_hint, get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='associations',
                required=(ITypedSharedTool, IAdminLayer, SharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesAssociationsColumn(ActionColumn):
    """Shared tool data types table associations column"""

    hint = _("Default links and external files")
    icon_class = 'fas fa-link'

    href = 'associations-modal.html'
    modal_target = True

    weight = 450


#
# Associations table modal viewer
#

@ajax_form_config(name='associations-modal.html',
                  context=IAssociationContainerTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
@implementer(IAssociationsContainerEditForm)
class AssociationsModalEditForm(AdminModalDisplayForm):
    """Associations modal edit form"""

    @property
    def title(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        hint = get_object_hint(self.context, self.request, self)
        label = get_object_label(self.context, self.request, self)
        return '<small>{}</small><br />{}'.format(
            translate(_("{}: {}")).format(hint, label) if hint else label,
            translate(_("Links and external files")))

    modal_class = 'modal-xl'


@factory_config(IAssociationsTable)
class AssociationsTable(Table):
    """Associations table"""

    @property
    def data_attributes(self):
        """Attributes getter"""
        attributes = super().data_attributes
        container = IAssociationContainer(self.context)
        get_ordered_data_attributes(attributes, container, self.request)
        return attributes

    display_if_empty = True


@adapter_config(required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IValues)
class AssociationsTableValues(ContextRequestViewAdapter):
    """Associations table values"""

    @property
    def values(self):
        """Associations container values getter"""
        yield from IAssociationContainer(self.context).values()


@adapter_config(name='reorder',
                required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsReorderColumn(ReorderColumn):
    """Associations reorder column"""


@view_config(name='reorder.json',
             context=IAssociationContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def reorder_associations_table(request):
    """Reorder associations"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsVisibleColumn(VisibilityColumn):
    """Associations table visible column"""


@view_config(name='switch-visible-item.json',
             context=IAssociationContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    return switch_element_attribute(request)


@adapter_config(name='icon',
                required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsIconColumn(ContentTypeColumn):
    """Associations table icon column"""


@adapter_config(name='label',
                required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsLabelColumn(NameColumn):
    """Associations table label column"""

    i18n_header = _("Public label")


@adapter_config(name='target',
                required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsTargetColumn(I18nColumnMixin, GetAttrColumn):
    """Associations table target column"""

    i18n_header = _("Internal target")
    weight = 50

    def get_value(self, obj):
        """Column value getter"""
        info = IAssociationInfo(obj, None)
        if info is None:
            return '--'
        return info.inner_title


@adapter_config(name='size',
                required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsSizeColumn(I18nColumnMixin, GetAttrColumn):
    """Associations table size column"""

    i18n_header = _("Size")
    weight = 60

    def get_value(self, obj):
        """Column value getter"""
        info = IAssociationInfo(obj, None)
        if info is None:
            return '--'
        return info.human_size


@adapter_config(name='trash',
                required=(IAssociationContainerTarget, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsTrashColumn(TrashColumn):
    """Associations table trash column"""


@view_config(name='delete-element.json',
             context=IAssociationContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def delete_data_type(request):
    """Delete data type"""
    return delete_container_element(request)


#
# Main associations table
#

@viewlet_config(name='associations-table',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IAssociationsContainerEditForm,
                manager=IContentSuffixViewletManager, weight=10)
class AssociationsTableView(InnerTableAdminView):
    """Associations table view"""

    table_class = AssociationsTable
    table_label = _("Links and external files list")