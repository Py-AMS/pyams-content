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

"""PyAMS_content.shared.common.types module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.container.ordered import OrderedContainer
from zope.interface import implementer
from zope.location.interfaces import ISublocations
from zope.schema import getFieldsInOrder
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.traversing.interfaces import ITraversable

from pyams_content.component.links.interfaces import ILinkContainerTarget
from pyams_content.component.paragraph.interfaces import IParagraphContainerTarget
from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.reference.pictogram import IPictogramTable
from pyams_content.shared.common.interfaces import ISharedTool
from pyams_content.shared.common.interfaces.types import DATA_MANAGER_ANNOTATION_KEY, \
    DATA_TYPES_VOCABULARY, DATA_TYPE_FIELDS_VOCABULARY, IDataType, \
    ITypedDataManager, ITypedSharedTool, IWfTypedSharedContent
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_sequence.reference import get_reference_target
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_local_registry, query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IDataType)
@implementer(IParagraphContainerTarget,
             ILinkContainerTarget)
class DataType(Persistent, Contained):
    """Base data type"""

    label = FieldProperty(IDataType['label'])
    source_folder = FieldProperty(IDataType['source_folder'])
    navigation_label = FieldProperty(IDataType['navigation_label'])
    backoffice_label = FieldProperty(IDataType['backoffice_label'])
    pictogram = FieldProperty(IDataType['pictogram'])
    display_as_tag = FieldProperty(IDataType['display_as_tag'])
    field_names = FieldProperty(IDataType['field_names'])

    def get_source_folder(self):
        """Source folder getter"""
        if self.source_folder is not None:
            return get_reference_target(self.source_folder)

    def get_pictogram(self):
        """Pictogram getter"""
        table = query_utility(IPictogramTable)
        if table is not None:
            return table.get(self.pictogram)


@factory_config(ITypedDataManager)
class TypedDataManager(OrderedContainer):
    """Data types container persistent class"""


@adapter_config(required=IDataType,
                provides=IViewContextPermissionChecker)
class DatatypePermissionChecker(ContextAdapter):
    """Data type permission checker"""

    edit_permission = MANAGE_TOOL_PERMISSION


@implementer(ITypedSharedTool)
class TypedSharedToolMixin:
    """Typed shared tool"""

    shared_content_types_fields = None


@adapter_config(required=ITypedSharedTool,
                provides=ITypedDataManager)
def typed_shared_tool_data_manager_factory(context):
    """Types shared tool data manager factory"""
    return get_annotation_adapter(context, DATA_MANAGER_ANNOTATION_KEY, ITypedDataManager,
                                  name='++types++')


@adapter_config(name='types',
                required=ITypedSharedTool,
                provides=ITraversable)
class TypedSharedToolTypesNamespace(ContextAdapter):
    """Typed shared tool ++types++ namespace"""

    def traverse(self, name, furtherpath=None):
        """Namespace traverser"""
        return ITypedDataManager(self.context)


@adapter_config(name='types',
                required=ITypedSharedTool,
                provides=ISublocations)
class TypedSharedToolSublocations(ContextAdapter):
    """Typed shared tool sub-locations adapter"""

    def sublocations(self):
        return ITypedDataManager(self.context).values()


#
# Typed shared content
#

@implementer(IWfTypedSharedContent)
class WfTypedSharedContentMixin:
    """Typed shared content"""

    data_type = FieldProperty(IWfTypedSharedContent['data_type'])

    def get_data_type(self):
        """Datatype getter"""
        if not self.data_type:
            return None
        tool = get_parent(self, ITypedSharedTool)
        if tool is not None:
            manager = ITypedDataManager(tool)
            return manager.get(self.data_type)
        return None

    @property
    def field_names(self):
        """Field names getter"""
        data_type = self.get_data_type()
        if data_type is not None:
            return data_type.field_names
        return None


# @subscriber(IObjectAddedEvent, context_selector=IWfTypedSharedContent)
# def handle_added_typed_shared_content(event):
#     """Automatically assign themes for newly created contents"""
#     content = event.object
#     if not IThemesTarget.providedBy(content):
#         return
#     themes_info = IThemesInfo(content)
#     if not themes_info.themes:  # don't remove previous themes!
#         data_type = content.get_data_type()
#         if data_type is not None:
#             themes_info.themes = IThemesInfo(data_type).themes


#
# Data types vocabularies
#

# @vocabulary_config(name=ALL_DATA_TYPES_VOCABULARY)
# class AllTypedSharedToolDataTypesVocabulary(SimpleVocabulary):
#     """Vocabulary consolidating all data types"""
#
#     def __init__(self, context):
#         terms = []
#         request = check_request()
#         registry = get_local_registry()
#         for tool in registry.getAllUtilitiesRegisteredFor(ISharedTool):
#             manager = ITypedDataManager(tool, None)
#             if manager is not None:
#                 terms.extend([
#                     SimpleTerm(datatype.__name__,
#                                title=II18n(datatype).query_attribute('backoffice_label',
#                                                                      request=request) or
#                                      II18n(datatype).query_attribute('label',
#                                                                      request=request))
#                     for datatype in manager.values()
#                 ])
#         terms.sort(key=lambda x: x.title)
#         super().__init__(terms)
#
#     def getTermByToken(self, token):
#         try:
#             return super().getTermByToken(token)
#         except LookupError:
#             request = check_request()
#             translate = request.localizer.translate
#             return SimpleTerm(token,
#                               title=translate(_("-- missing value ({}) --")).format(token))


def get_all_data_types(request):
    """Get list of all registered data types as JSON object"""
    results = []
    registry = get_local_registry()
    for tool in sorted(registry.getAllUtilitiesRegisteredFor(ISharedTool),
                       key=lambda x: II18n(x).query_attribute('title', request=request)):
        manager = ITypedDataManager(tool, None)
        if manager is not None:
            terms = [
                {
                    'id': datatype.__name__,
                    'text': II18n(datatype).query_attribute('backoffice_label',
                                                            request=request) or
                            II18n(datatype).query_attribute('label',
                                                            request=request)
                }
                for datatype in manager.values()
            ]
            content_factory = tool.shared_content_factory
            results.append({
                'text': request.localizer.translate(content_factory.content_name),
                'disabled': True,
                'children': terms
            })
    return results


@vocabulary_config(name=DATA_TYPES_VOCABULARY)
class TypedSharedToolDataTypesVocabulary(SimpleVocabulary):
    """Typed shared tool data types vocabulary"""

    def __init__(self, context):
        terms = []
        parent = get_parent(context, ITypedSharedTool)
        if parent is not None:
            request = check_request()
            manager = ITypedDataManager(parent)
            terms = [SimpleTerm(datatype.__name__,
                                title=II18n(datatype).query_attribute('backoffice_label',
                                                                      request=request) or
                                      II18n(datatype).query_attribute('label',
                                                                      request=request))
                     for datatype in manager.values()]
        super(TypedSharedToolDataTypesVocabulary, self).__init__(terms)


@vocabulary_config(name=DATA_TYPE_FIELDS_VOCABULARY)
class TypedSharedToolDataTypesFieldsVocabulary(SimpleVocabulary):
    """Typed shared tool data types fields vocabulary"""

    def __init__(self, context):
        terms = []
        parent = get_parent(context, ITypedSharedTool)
        if (parent is not None) and parent.shared_content_types_fields:
            request = check_request()
            translate = request.localizer.translate
            terms = [SimpleTerm(name, title=translate(field.title))
                     for name, field in getFieldsInOrder(parent.shared_content_types_fields)]
        super(TypedSharedToolDataTypesFieldsVocabulary, self).__init__(terms)
