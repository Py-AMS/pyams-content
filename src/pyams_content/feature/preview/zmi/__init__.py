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

"""PyAMS_content.feature.preview.zmi module

Management interface components used by preview feature.
"""

from pyramid.interfaces import IView

from pyams_content.feature.preview.interfaces import IPreviewTarget
from zope.interface import Interface

from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_skin.viewlet.actions import ContextAction, ContextActionsViewletManager
from pyams_template.template import layout_config
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalDisplayForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewletmanager_config(name='pyams_context.preview',
                       context=IPreviewTarget, layer=IAdminLayer, view=IView,
                       manager=IToolbarViewletManager, weight=50)
class PreviewTargetActions(ContextActionsViewletManager):
    """Preview target actions"""


@viewlet_config(name='pyams_content.preview.modal',
                context=IPreviewTarget, layer=IAdminLayer, view=IView,
                manager=PreviewTargetActions, weight=10)
class ModalPreviewAction(ContextAction):
    """Modal preview action"""

    icon_class = 'fas fa-binoculars'
    label = _("Preview")

    href = 'modal-preview.html'
    modal_target = True


@pagelet_config(name='modal-preview.html',
                context=IPreviewTarget, layer=IPyAMSLayer)
@layout_config(template='templates/modal-preview.pt', layer=IPyAMSLayer)
class ModalPreview(AdminModalDisplayForm):
    """Modal preview form"""

    modal_class = 'modal-max'


@viewlet_config(name='pyams_content.preview.blank',
                context=IPreviewTarget, layer=IAdminLayer, view=Interface,
                manager=PreviewTargetActions, weight=20)
class BlankPreviewAction(ContextAction):
    """Blank window preview action"""

    icon_class = 'far fa-window-maximize'
    hint = _("Open preview in new tab")
    hint_placement = 'bottom'

    href = 'preview.html'
    target = '_blank'
