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

from zope.interface import Interface, implementer

from pyams_content.component.association import IAssociationContainerTarget
from pyams_content.component.association.zmi import AssociationItemAddFormMixin, \
    AssociationItemAddMenuMixin, IAssociationsTable
from pyams_content.component.association.zmi.interfaces import IAssociationItemAddForm, \
    IAssociationItemEditForm
from pyams_content.component.links import IExternalLink, IInternalLink, IMailtoLink
from pyams_content.component.links.interfaces import ILinkContainerTarget
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
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectIcon
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.utils import get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


class ILinkAddForm(IAssociationItemAddForm):
    """Link add form internal marker interface"""


class ILinkEditForm(IAssociationItemEditForm):
    """Link edit form internal marker interface"""


@adapter_config(required=(IAssociationContainerTarget, IAdminLayer, ILinkAddForm),
                provides=IFormTitle)
def link_add_form_title(context, request, view):
    """Link add form title getter"""
    translate = request.localizer.translate
    parent = get_parent(context, IAssociationContainerTarget)
    label = translate(_("Add new link"))
    return f'<small>{get_object_label(parent, request, view)}</small><br />{label}'


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

    label = _("Internal link...")
    icon_class = 'fas fa-external-link-square-alt fa-rotate-90'

    href = 'add-internal-link.html'


@ajax_form_config(name='add-internal-link.html',
                  context=ILinkContainerTarget, layer=IPyAMSLayer)
class InternalLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """Internal link add form"""

    legend = _("Add internal link")

    fields = Fields(IInternalLink).select('reference', 'force_canonical_url', 'title',
                                          'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IInternalLink


@adapter_config(required=(IInternalLink, IAdminLayer, Interface),
                provides=IObjectIcon)
def internal_link_icon(context, request, view):  # pylint: disable=unused-argument
    """Internal link icon getter"""
    return "fas fa-fw fa-external-link-square-alt fa-rotate-90"


@adapter_config(required=(IInternalLink, IAdminLayer, Interface),
                provides=IObjectHint)
def internal_link_hint(context, request, view):  # pylint: disable=unused-argument
    """internal link hint getter"""
    return request.localizer.translate(_("Internal link"))


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

    label = _("External link...")
    icon_class = 'fas fa-external-link-alt'

    href = 'add-external-link.html'


@ajax_form_config(name='add-external-link.html',
                  context=ILinkContainerTarget, layer=IPyAMSLayer)
class ExternalLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """External link add form"""

    legend = _("Add external link")

    fields = Fields(IExternalLink).select('url', 'title', 'description',
                                          'language', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IExternalLink


@adapter_config(required=(IExternalLink, IAdminLayer, Interface),
                provides=IObjectIcon)
def external_link_icon(context, request, view):  # pylint: disable=unused-argument
    """External link icon getter"""
    return "fas fa-fw fa-external-link-alt"


@adapter_config(required=(IExternalLink, IAdminLayer, Interface),
                provides=IObjectHint)
def external_link_hint(context, request, view):  # pylint: disable=unused-argument
    """external link hint getter"""
    return request.localizer.translate(_("External link"))


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

    label = _("Mailto link...")
    icon_class = 'far fa-envelope'

    href = 'add-mailto-link.html'


@ajax_form_config(name='add-mailto-link.html',
                  context=ILinkContainerTarget, layer=IPyAMSLayer)
class MailtoLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """Mailto link add form"""

    legend = _("Add mailto link")

    fields = Fields(IMailtoLink).select('address', 'address_name', 'title',
                                        'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IMailtoLink


@adapter_config(required=(IMailtoLink, IAdminLayer, Interface),
                provides=IObjectIcon)
def mailto_link_icon(context, request, view):  # pylint: disable=unused-argument
    """Mailto link icon getter"""
    return "far fa-fw fa-envelope"


@adapter_config(required=(IMailtoLink, IAdminLayer, Interface),
                provides=IObjectHint)
def mailto_link_hint(context, request, view):  # pylint: disable=unused-argument
    """mailto link hint getter"""
    return request.localizer.translate(_("Mailto link"))


@ajax_form_config(name='properties.html',
                  context=IMailtoLink, layer=IPyAMSLayer)
class MailtoLinkPropertiesEditForm(LinkEditFormMixin, AdminModalEditForm):
    """mailto link properties edit form"""

    fields = Fields(IMailtoLink).select('address', 'address_name', 'title',
                                        'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
