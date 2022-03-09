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

from zope.interface import implementer

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.association.zmi import AssociationItemAddFormMixin, \
    AssociationItemAddMenuMixin, IAssociationsTable
from pyams_content.component.association.zmi.interfaces import IAssociationItemAddForm, \
    IAssociationItemEditForm
from pyams_content.component.links import ExternalLink, InternalLink, MailtoLink
from pyams_content.component.links.interfaces import IExternalLink, IInternalLink, \
    ILinkContainerTarget, IMailtoLink
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.utils import get_object_hint, get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


class ILinkAddForm(IAssociationItemAddForm):
    """Link add form internal marker interface"""


class ILinkEditForm(IAssociationItemEditForm):
    """Link edit form internal marker interface"""


@adapter_config(required=(IAssociationContainer, IAdminLayer, ILinkAddForm),
                provides=IFormTitle)
def link_add_form_title(context, request, view):
    """Link add form title getter"""
    translate = request.localizer.translate
    parent = get_parent(context, IAssociationContainerTarget)
    parent_label = translate(_("{}: {}")).format(get_object_hint(parent, request, view),
                                                 get_object_label(parent, request, view))
    label = translate(_("Add new link"))
    return f'<small>{parent_label}</small><br />{label}'


@implementer(ILinkAddForm)
class LinkAddFormMixin(AssociationItemAddFormMixin):
    """Link add form mixin class"""

    legend = _("New link properties")


@implementer(ILinkEditForm)
class LinkEditFormMixin:
    """Link edit form mixin class"""

    legend = _("Link properties")


#
# Internal links management
#

@viewlet_config(name='add-internal-link.menu',
                context=ILinkContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=50)
class InternalLinkAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """Internal link add menu"""

    label = InternalLink.icon_hint
    icon_class = InternalLink.icon_class

    href = 'add-internal-link.html'


@ajax_form_config(name='add-internal-link.html',
                  context=IAssociationContainer, layer=IPyAMSLayer)
class InternalLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """Internal link add form"""

    legend = _("Add internal link")

    fields = Fields(IInternalLink).select('reference', 'force_canonical_url', 'title',
                                          'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IInternalLink


@ajax_form_config(name='properties.html',
                  context=IInternalLink, layer=IPyAMSLayer)
class InternalLinkPropertiesEditForm(LinkEditFormMixin, AdminModalEditForm):
    """internal link properties edit form"""

    fields = Fields(IInternalLink).select('reference', 'force_canonical_url', 'title',
                                          'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget


#
# External links management
#

@viewlet_config(name='add-external-link.menu',
                context=ILinkContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=55)
class ExternalLinkAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """External link add menu"""

    label = ExternalLink.icon_hint
    icon_class = ExternalLink.icon_class

    href = 'add-external-link.html'


@ajax_form_config(name='add-external-link.html',
                  context=IAssociationContainer, layer=IPyAMSLayer)
class ExternalLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """External link add form"""

    legend = _("Add external link")

    fields = Fields(IExternalLink).select('url', 'title', 'description',
                                          'language', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IExternalLink


@ajax_form_config(name='properties.html',
                  context=IExternalLink, layer=IPyAMSLayer)
class ExternalLinkPropertiesEditForm(LinkEditFormMixin, AdminModalEditForm):
    """external link properties edit form"""

    fields = Fields(IExternalLink).select('url', 'title', 'description',
                                          'language', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget


#
# Mailto links management
#

@viewlet_config(name='add-mailto-link.menu',
                context=ILinkContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=60)
class MailtoLinkAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """Mailto link add menu"""

    label = MailtoLink.icon_hint
    icon_class = MailtoLink.icon_class

    href = 'add-mailto-link.html'


@ajax_form_config(name='add-mailto-link.html',
                  context=IAssociationContainer, layer=IPyAMSLayer)
class MailtoLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """Mailto link add form"""

    legend = _("Add mailto link")

    fields = Fields(IMailtoLink).select('address', 'address_name', 'title',
                                        'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IMailtoLink


@ajax_form_config(name='properties.html',
                  context=IMailtoLink, layer=IPyAMSLayer)
class MailtoLinkPropertiesEditForm(LinkEditFormMixin, AdminModalEditForm):
    """mailto link properties edit form"""

    fields = Fields(IMailtoLink).select('address', 'address_name', 'title',
                                        'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
