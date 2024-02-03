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
from pyams_content.component.association.interfaces import IAssociationParagraph
from pyams_content.component.association.skin import AssociationContainerRendererMixin
from pyams_content.feature.renderer import DefaultContentRenderer, \
    IContentRenderer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IAssociationParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/association-default.pt', layer=IPyAMSLayer)
class AssociationParagraphDefaultRenderer(AssociationContainerRendererMixin,
                                          DefaultContentRenderer):
    """Association paragraph default renderer"""

    label = _("Associations list (default)")
