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

"""PyAMS_content.root module

This module defines roles and permissions checker of site root.
"""

__docformat__ = 'restructuredtext'

from persistent import Persistent

from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_content.root.interfaces import ISiteRootInfos, ISiteRootRoles, \
    ISiteRootToolsConfiguration, SITEROOT_ROLES, \
    SITE_ROOT_INFOS_KEY, SITE_ROOT_TOOLS_CONFIGURATION_KEY
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_file.property import FileProperty
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IRolesPolicy, IViewContextPermissionChecker
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_security.security import ProtectedObjectRoles
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config, \
    get_annotation_adapter
from pyams_utils.factory import factory_config


@factory_config(provided=ISiteRootInfos)
class SiteRootInfos(Persistent, Contained):
    """Site root information"""

    title = FieldProperty(ISiteRootInfos['title'])
    short_title = FieldProperty(ISiteRootInfos['short_title'])
    description = FieldProperty(ISiteRootInfos['description'])
    author = FieldProperty(ISiteRootInfos['author'])
    icon = FileProperty(ISiteRootInfos['icon'])
    logo = FileProperty(ISiteRootInfos['logo'])


@adapter_config(required=ISiteRoot, provides=ISiteRootInfos)
def site_root_infos_factory(context):
    """Site root information factory"""
    return get_annotation_adapter(context, SITE_ROOT_INFOS_KEY,
                                  ISiteRootInfos, name='++infos++')


@adapter_config(name='infos',
                required=ISiteRoot, provides=ITraversable)
class SiteRootInfosTraverser(ContextAdapter):
    """Site root infos traverser"""

    def traverse(self, name, furtherPath=None):
        """Namespace traverser"""
        return ISiteRootInfos(self.context)


@implementer(ISiteRootRoles)
class SiteRootRoles(ProtectedObjectRoles):
    """Site root roles"""

    webmasters = RolePrincipalsFieldProperty(ISiteRootRoles['webmasters'])
    designers = RolePrincipalsFieldProperty(ISiteRootRoles['designers'])
    operators = RolePrincipalsFieldProperty(ISiteRootRoles['operators'])


@adapter_config(required=ISiteRoot,
                provides=ISiteRootRoles)
def site_root_roles_adapter(context):
    """Site root roles adapters"""
    return SiteRootRoles(context)


@adapter_config(name=SITEROOT_ROLES,
                required=ISiteRoot,
                provides=IRolesPolicy)
class SiteRootRolesPolicy(ContextAdapter):
    """Site root roles policy"""

    roles_interface = ISiteRootRoles
    weight = 10


@adapter_config(required=(ISiteRoot, IPyAMSLayer, Interface),
                provides=IViewContextPermissionChecker)
class SiteRootPermissionChecker(ContextRequestViewAdapter):
    """Site root permission checker"""

    edit_permission = MANAGE_SITE_ROOT_PERMISSION



