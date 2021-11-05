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

"""PyAMS_content.shared.common.security module

This module defines common security rules used by all shared tools.
"""

__docformat__ = 'restructuredtext'

from pyams_content.shared.common.interfaces import CONTENT_MANAGER_ROLES, IBaseSharedTool, \
    ISharedToolRoles
from zope.interface import implementer

from pyams_security.interfaces import IRolesPolicy
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_security.security import ProtectedObjectRoles
from pyams_utils.adapter import ContextAdapter, adapter_config


@implementer(ISharedToolRoles)
class SharedToolRoles(ProtectedObjectRoles):
    """Shared tool roles"""

    webmasters = RolePrincipalsFieldProperty(ISharedToolRoles['webmasters'])
    pilots = RolePrincipalsFieldProperty(ISharedToolRoles['pilots'])
    managers = RolePrincipalsFieldProperty(ISharedToolRoles['managers'])
    contributors = RolePrincipalsFieldProperty(ISharedToolRoles['contributors'])
    designers = RolePrincipalsFieldProperty(ISharedToolRoles['designers'])


@adapter_config(required=IBaseSharedTool,
                provides=ISharedToolRoles)
def shared_tool_roles_adapter(context):
    """Shared tool roles adapter"""
    return SharedToolRoles(context)


@adapter_config(name=CONTENT_MANAGER_ROLES,
                required=IBaseSharedTool,
                provides=IRolesPolicy)
class SharedToolRolesPolicy(ContextAdapter):
    """Shared tool roles policy"""

    roles_interface = ISharedToolRoles
    weight = 10
