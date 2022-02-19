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

"""PyAMS_content.component.extfile.zmi module

This module provides management components for external files.
"""

from zope.interface import Interface, implementer

from pyams_content.component.association import IAssociationContainerTarget
from pyams_content.component.association.zmi import AssociationItemAddFormMixin, \
    AssociationItemAddMenuMixin, IAssociationsTable
from pyams_content.component.extfile import IBaseExtFile, IExtAudio, IExtFile, IExtImage, \
    IExtVideo
from pyams_content.component.extfile.interfaces import IExtFileContainerTarget
from pyams_content.component.extfile.zmi.interfaces import IExtFileAddForm, IExtFileEditForm
from pyams_content.component.extfile.zmi.widget import I18nExtFileTitleFieldWidget
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectIcon
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.utils import get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IAssociationContainerTarget, IAdminLayer, IExtFileAddForm),
                provides=IFormTitle)
def base_extfile_add_form_title(context, request, view):
    """Base external file add form title getter"""
    translate = request.localizer.translate
    parent = get_parent(context, IAssociationContainerTarget)
    label = translate(_("Add new external file"))
    return f'<small>{get_object_label(parent, request, view)}</small><br />{label}'


@implementer(IExtFileAddForm)
class ExtFileAddFormMixin(AssociationItemAddFormMixin):
    """External file add form mixin class"""

    legend = _("New file properties")


@adapter_config(required=(IBaseExtFile, IAdminLayer, Interface),
                provides=IObjectIcon)
def external_file_icon(context, request, view):  # pylint: disable=unused-argument
    """External file hint getter"""
    return context.icon_class


@adapter_config(required=(IExtFile, IAdminLayer, Interface),
                provides=IObjectHint)
def external_file_hint(context, request, view):  # pylint: disable=unused-argument
    """External file hint getter"""
    return request.localizer.translate(context.icon_hint)


@implementer(IExtFileEditForm)
class ExtFileEditFormMixin:
    """External file edit form mixin class"""

    legend = _("External file properties")


#
# External files forms
#

@viewlet_config(name='add-extfile.divider',
                context=IExtFileContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=69)
class ExtFileAddMenuDivider(ProtectedViewObjectMixin, MenuDivider):
    """External file add menu divider"""


@viewlet_config(name='add-extfile.menu',
                context=IExtFileContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=70)
class ExtFileAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """External file add menu"""

    label = _("External file...")
    icon_class = 'far fa-file-alt'

    href = 'add-extfile.html'


@ajax_form_config(name='add-extfile.html',
                  context=IExtFileContainerTarget, layer=IPyAMSLayer)
class ExtFileAddForm(ExtFileAddFormMixin, AdminModalAddForm):
    """External file add form"""

    legend = _("Add external file")

    fields = Fields(IExtFile).select('data', 'filename', 'title', 'description',
                                     'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget

    content_factory = IExtFile


@ajax_form_config(name='properties.html',
                  context=IExtFile, layer=IPyAMSLayer)
class ExtFileEditForm(ExtFileEditFormMixin, AdminModalEditForm):
    """External file properties edit form"""

    fields = Fields(IExtFile).select('data', 'filename', 'title', 'description',
                                     'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget


#
# External images forms
#

@viewlet_config(name='add-extimage.menu',
                context=IExtFileContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=75)
class ExtImageAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """External image add menu"""

    label = _("External image...")
    icon_class = 'far fa-image'

    href = 'add-extimage.html'


@ajax_form_config(name='add-extimage.html',
                  context=IExtFileContainerTarget, layer=IPyAMSLayer)
class ExtImageAddForm(ExtFileAddFormMixin, AdminModalAddForm):
    """External image add form"""

    legend = _("Add external image")

    fields = Fields(IExtImage).select('data', 'filename', 'title', 'description',
                                      'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget

    content_factory = IExtImage


@adapter_config(required=(IExtImage, IAdminLayer, Interface),
                provides=IObjectIcon)
def external_image_icon(context, request, view):  # pylint: disable=unused-argument
    """External image hint getter"""
    return 'far fa-image'


@adapter_config(required=(IExtImage, IAdminLayer, Interface),
                provides=IObjectHint)
def external_image_hint(context, request, view):  # pylint: disable=unused-argument
    """External image hint getter"""
    return request.localizer.translate(_("External image"))


@ajax_form_config(name='properties.html',
                  context=IExtImage, layer=IPyAMSLayer)
class ExtImageEditForm(ExtFileEditFormMixin, AdminModalEditForm):
    """External image properties edit form"""

    fields = Fields(IExtImage).select('data', 'filename', 'title', 'description',
                                      'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget


#
# External videos forms
#

@viewlet_config(name='add-extvideo.menu',
                context=IExtFileContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=80)
class ExtVideoAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """External video add menu"""

    label = _("External video...")
    icon_class = 'fas fa-film'

    href = 'add-extvideo.html'


@ajax_form_config(name='add-extvideo.html',
                  context=IExtFileContainerTarget, layer=IPyAMSLayer)
class ExtVideoAddForm(ExtFileAddFormMixin, AdminModalAddForm):
    """External video add form"""

    legend = _("Add external video")

    fields = Fields(IExtVideo).select('data', 'filename', 'title', 'description',
                                      'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget

    content_factory = IExtVideo


@adapter_config(required=(IExtVideo, IAdminLayer, Interface),
                provides=IObjectIcon)
def external_video_icon(context, request, view):  # pylint: disable=unused-argument
    """External video hint getter"""
    return 'fas fa-film'


@adapter_config(required=(IExtVideo, IAdminLayer, Interface),
                provides=IObjectHint)
def external_video_hint(context, request, view):  # pylint: disable=unused-argument
    """External video hint getter"""
    return request.localizer.translate(_("External video"))


@ajax_form_config(name='properties.html',
                  context=IExtVideo, layer=IPyAMSLayer)
class ExtVideoEditForm(ExtFileEditFormMixin, AdminModalEditForm):
    """External video properties edit form"""

    fields = Fields(IExtVideo).select('data', 'filename', 'title', 'description',
                                      'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget


#
# External audios forms
#

@viewlet_config(name='add-extaudio.menu',
                context=IExtFileContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=85)
class ExtAudioAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """External audio add menu"""

    label = _("External audio...")
    icon_class = 'fas fa-headphones'

    href = 'add-extaudio.html'


@ajax_form_config(name='add-extaudio.html',
                  context=IExtFileContainerTarget, layer=IPyAMSLayer)
class ExtAudioAddForm(ExtFileAddFormMixin, AdminModalAddForm):
    """External audio add form"""

    legend = _("Add external audio")

    fields = Fields(IExtAudio).select('data', 'filename', 'title', 'description',
                                      'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget

    content_factory = IExtAudio


@adapter_config(required=(IExtAudio, IAdminLayer, Interface),
                provides=IObjectIcon)
def external_audio_icon(context, request, view):  # pylint: disable=unused-argument
    """External audio hint getter"""
    return 'fas fa-headphones'


@adapter_config(required=(IExtAudio, IAdminLayer, Interface),
                provides=IObjectHint)
def external_audio_hint(context, request, view):  # pylint: disable=unused-argument
    """External audio hint getter"""
    return request.localizer.translate(_("External audio"))


@ajax_form_config(name='properties.html',
                  context=IExtAudio, layer=IPyAMSLayer)
class ExtAudioEditForm(ExtFileEditFormMixin, AdminModalEditForm):
    """External audio properties edit form"""

    fields = Fields(IExtAudio).select('data', 'filename', 'title', 'description',
                                      'author', 'language')
    fields['title'].widget_factory = I18nExtFileTitleFieldWidget
