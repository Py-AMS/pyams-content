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

"""PyAMS_content.shared.common.zmi.viewlet module

"""

import locale

from zope.interface import Interface

from pyams_content.shared.common.interfaces import IBaseSharedTool, ISharedSite
from pyams_content.zmi.viewlet.toplinks import TopTabsViewletManager
from pyams_i18n.interfaces import II18n
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.registry import get_all_utilities_registered_for
from pyams_utils.url import absolute_url
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.toplinks import TopMenuViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewletmanager_config(name='shared-contents.menu',
                       context=Interface, layer=IAdminLayer,
                       manager=TopTabsViewletManager, weight=20)
class SharedContentsMenu(TopMenuViewletManager):
    """Shared contents menu"""

    label = _("Shared contents")

    def update(self):
        super().update()
        context = self.context
        request = self.request
        parent = self.__parent__
        for site in sorted(filter(lambda tool: (not ISharedSite.providedBy(tool)) and
                                               tool.shared_content_menu,
                                  get_all_utilities_registered_for(IBaseSharedTool)),
                           key=lambda x: locale.strxfrm(II18n(x).query_attribute('title',
                                                                                 request=request)
                                                        or '')):
            menu = MenuItem(context, request, parent, self)
            menu.label = II18n(site).query_attribute('title', request=request) or site.__name__
            menu.href = absolute_url(site, request, 'admin')
            self.viewlets.append(menu)


@viewletmanager_config(name='shared-tools.menu',
                       context=Interface, layer=IAdminLayer,
                       manager=TopTabsViewletManager, weight=30)
class SharedToolsMenu(TopMenuViewletManager):
    """Shared tools menu"""

    label = _("Shared tools")

    def update(self):
        super().update()
        context = self.context
        request = self.request
        parent = self.__parent__
        for site in sorted(filter(lambda tool: (not ISharedSite.providedBy(tool)) and
                                               (not tool.shared_content_menu),
                                  get_all_utilities_registered_for(IBaseSharedTool)),
                           key=lambda x: locale.strxfrm(II18n(x).query_attribute('title',
                                                                                 request=request)
                                                        or '')):
            menu = MenuItem(context, request, parent, self)
            menu.label = II18n(site).query_attribute('title', request=request) or site.__name__
            menu.href = absolute_url(site, request, 'admin')
            self.viewlets.append(menu)
