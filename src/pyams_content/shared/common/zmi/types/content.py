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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from pyramid.decorator import reify
from zope.interface import Interface

from pyams_content.shared.common.interfaces import ISharedTool
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_content.shared.common.zmi import SharedContentPropertiesEditForm
from pyams_form.field import Fields
from pyams_utils.registry import get_utility
from pyams_zmi.form import AdminEditForm


class TypedSharedContentPropertiesEditForm(SharedContentPropertiesEditForm):
    """Typed shared content properties edit form"""

    interface = IWfTypedSharedContent
    fieldnames = ('title', 'short_name', 'content_url', 'data_type',
                  'header', 'description', 'notepad')


class TypedSharedContentCustomInfoEditForm(AdminEditForm):
    """Typed shared content custom information edit form"""

    @reify
    def datatype(self):
        """Form context datatype getter"""
        context = self.context
        if IWfTypedSharedContent.providedBy(context):
            return context.get_data_type()
        return None

    def get_content(self):
        """Form content getter"""
        manager = get_utility(ISharedTool, name=self.context.content_type)
        return manager.shared_content_info_factory(self.context)

    @property
    def fields(self):
        """Form fields getter"""
        datatype = self.datatype
        if datatype is None:
            return Fields(Interface)
        manager = get_utility(ISharedTool, name=self.context.content_type)
        return Fields(manager.shared_content_info_factory).select(*datatype.field_names)
