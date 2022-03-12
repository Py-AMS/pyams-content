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

"""PyAMS_*** module

"""

from fanstatic import Library, Resource
from zope.interface import Interface

from pyams_content.skin.interfaces import IPyAMSDefaultLayer
from pyams_layer.interfaces import IResources, ISkin
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_template.template import override_layout
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import utility_config


__docformat__ = 'restructuredtext'

from pyams_content import _


library = Library('pyams', 'resources')

pyams_default_theme = Resource(library, 'js/pyams-dev.js',
                               minified='js/pyams.js',
                               depends=(),
                               bottom=False)


@utility_config(name='PyAMS default skin',
                provides=ISkin)
class PyAMSDefaultSkin:
    """PyAMS default skin"""

    label = _("PyAMS default skin")
    layer = IPyAMSDefaultLayer


@adapter_config(required=(Interface, IPyAMSDefaultLayer, Interface),
                provides=IResources)
class PyAMSDefaultSkinResources(ContextRequestViewAdapter):
    """PyAMS default skin resources"""

    resources = (pyams_default_theme,)


override_layout(PortalContextIndexPage,
                template='templates/layout.pt', layer=IPyAMSDefaultLayer)
