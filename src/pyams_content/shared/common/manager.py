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

"""PyAMS_content.shared.common.manager module

"""

from zope.annotation import IAttributeAnnotatable
from zope.container.folder import Folder
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.shared.common.interfaces import IBaseSharedTool, ISharedContentFactory, \
    ISharedTool, ISharedToolContainer
from pyams_i18n.content import I18nManagerMixin
from pyams_security.interfaces import IDefaultProtectionPolicy
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import get_object_factory
from pyams_utils.registry import query_utility
from pyams_workflow.interfaces import IWorkflow


__docformat__ = 'restructuredtext'


@implementer(ISharedToolContainer, IAttributeAnnotatable)
class SharedToolContainer(Folder):
    """Shared tools container"""

    title = FieldProperty(ISharedToolContainer['title'])
    short_name = FieldProperty(ISharedToolContainer['short_name'])


@implementer(IDefaultProtectionPolicy, IBaseSharedTool)
class BaseSharedTool(I18nManagerMixin):
    """Base shared tool class"""

    title = FieldProperty(IBaseSharedTool['title'])
    short_name = FieldProperty(IBaseSharedTool['short_name'])

    shared_content_menu = True
    shared_content_workflow = FieldProperty(IBaseSharedTool['shared_content_workflow'])


@implementer(ISharedTool)
class SharedTool(Folder, BaseSharedTool):
    """Shared tool class"""

    shared_content_interface = None
    '''Shared content interface must be defined by subclasses'''

    @property
    def shared_content_factory(self):
        return get_object_factory(self.shared_content_interface)

    @property
    def shared_content_type(self):
        factory = self.shared_content_factory
        if factory is not None:
            return factory.content_class.content_type
        return None


@adapter_config(required=IBaseSharedTool,
                provides=IWorkflow)
def shared_tool_workflow_adapter(context):
    """Shared tool workflow adapter"""
    return query_utility(IWorkflow, name=context.shared_content_workflow)
