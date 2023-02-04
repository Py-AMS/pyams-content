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

"""PyAMS_content.component.illustration.skin module

This module provides base illustrations adapters.
"""

from zope.interface import Interface

from pyams_content.component.illustration import IBaseIllustrationTarget, IIllustration, \
    ILinkIllustration
from pyams_content.component.links import IInternalLink
from pyams_content.feature.renderer import HIDDEN_RENDERER_NAME
from pyams_content.shared.common import ISharedContent
from pyams_content.skin.interfaces import IContentNavigationIllustration
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension


#
# Illustrations adapters
#

@adapter_config(required=(IInternalLink, IPyAMSLayer),
                provides=IContentNavigationIllustration)
@adapter_config(context=(IBaseIllustrationTarget, IPyAMSLayer),
                provides=IContentNavigationIllustration)
def base_content_navigation_illustration_factory(context, request):
    """Default content navigation illustration adapter"""
    illustration = ILinkIllustration(context, None)
    if not (illustration and illustration.has_data()):
        illustration = IIllustration(context, None)
        if IIllustration.providedBy(illustration) and \
                (illustration.renderer == HIDDEN_RENDERER_NAME):
            illustration = None
    if illustration and illustration.has_data():
        return illustration
    if IInternalLink.providedBy(context):
        target = context.get_target()
        if target is not None:
            illustration = request.registry.queryMultiAdapter((target, request),
                                                              IContentNavigationIllustration)
            if illustration and illustration.has_data():
                return illustration
    return None


@adapter_config(context=(ISharedContent, IPyAMSLayer),
                provides=IContentNavigationIllustration)
def shared_content_illustration_factory(context, request):
    """Shared content illustration factory"""
    version = context.visible_version
    if version is not None:
        return request.registry.queryMultiAdapter((version, request),
                                                  IContentNavigationIllustration)
    return None


@adapter_config(name='pyams_illustration',
                context=(Interface, Interface, Interface),
                provides=ITALESExtension)
class PyAMSIllustrationTALESExtension(ContextRequestViewAdapter):
    """PyAMS navigation illustration TALES extension"""

    def render(self, context=None, name=''):
        if context is None:
            context = self.context
        return self.request.registry.queryMultiAdapter((context, self.request),
                                                       IContentNavigationIllustration,
                                                       name=name)
