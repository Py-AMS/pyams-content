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

"""PyAMS_content.shared.common.interfaces.types module

This module defines interfaces related to content data types.
"""

from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.interface import Attribute
from zope.location import ILocation
from zope.schema import Bool, Choice, List

from pyams_content.reference.pictogram import PICTOGRAM_VOCABULARY
from pyams_content.shared.common.interfaces import IBaseContentPortalContext, ISharedTool, \
    IWfSharedContent
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortalContext
from pyams_sequence.schema import InternalReferenceField


__docformat__ = 'restructuredtext'

from pyams_content import _


DATA_TYPES_VOCABULARY = 'pyams_content.datatypes'
"""Vocabulary of shared content data types"""

VISIBLE_DATA_TYPES_VOCABULARY = 'pyams_content.datatypes.visible'
"""Vocabulary of shared content visible data types"""

ALL_DATA_TYPES_VOCABULARY = 'pyams_content.datatypes.all'
"""Vocabulary of all shared content tools data types"""

DATA_TYPE_FIELDS_VOCABULARY = 'pyams_content.datatype.fields'
"""Vocabulary of data type fields"""


class IDataType(ILocation):
    """Data interface for data-types"""

    visible = Bool(title=_("Visible?"),
                   description=_("An hidden data type can't be assigned to new contents"),
                   required=True,
                   default=True)

    label = I18nTextLineField(title=_("Label"),
                              required=True)

    source_folder = InternalReferenceField(title=_("Source folder"),
                                           description=_("Source folder (or search engine) to "
                                                         "which content is attached; if this "
                                                         "reference is set, canonical URL will "
                                                         "be based on this object's URL"),
                                           required=False)

    def get_source_folder(self):
        """Return source folder as object"""

    navigation_label = I18nTextLineField(title=_("Navigation label"),
                                         description=_("Label used for navigation entries"),
                                         required=False)

    backoffice_label = I18nTextLineField(title=_("Back-office label"),
                                         description=_("Optional label used in management pages "
                                                       "instead of default label"),
                                         required=False)

    pictogram = Choice(title=_("Pictogram"),
                       description=_("Pictogram associated with this data type"),
                       vocabulary=PICTOGRAM_VOCABULARY,
                       required=False)

    display_as_tag = Bool(title=_("Display as tag?"),
                          description=_("Some portlets renderers can display a small tag above "
                                        "each content to show their content type; if this option "
                                        "is checked, data type label will be displayed instead "
                                        "of content type"),
                          required=True,
                          default=False)

    field_names = List(title=_("Field names"),
                       description=_("List of fields associated with this data type"),
                       value_type=Choice(vocabulary=DATA_TYPE_FIELDS_VOCABULARY))


#
# Types data manager interfaces
#

DATA_MANAGER_ANNOTATION_KEY = 'pyams_content.types.manager'


class ITypedDataManager(IContainer):
    """Typed shared data manager interface"""

    contains(IDataType)

    def get_visible_items(self):
        """Iterator on visible data types"""


class ITypedSharedTool(ISharedTool):
    """Shared tool containing typed data"""

    shared_content_types_fields = Attribute("Content fields interface")


class ITypedSharedToolPortalContext(ITypedSharedTool, IPortalContext):
    """Typed shared tool with portal context"""


#
# Typed content interfaces
#

class IWfTypedSharedContent(IWfSharedContent):
    """Typed shared content"""

    data_type = Choice(title=_("Data type"),
                       description=_("Type of content data"),
                       required=True,
                       vocabulary=VISIBLE_DATA_TYPES_VOCABULARY)

    def get_data_type(self):
        """Get associated data type"""

    field_names = Attribute("Selected data type field names")


class IWfTypedSharedContentPortalContext(IWfTypedSharedContent, IBaseContentPortalContext):
    """Shared content with portal support"""
