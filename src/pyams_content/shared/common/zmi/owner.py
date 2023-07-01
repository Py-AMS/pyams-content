#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
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

__docformat__ = 'restructuredtext'

from datetime import datetime

from zope.interface import Interface
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import Bool

from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.shared.common import IWfSharedContent, IWfSharedContentRoles
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.schema import PrincipalField
from pyams_security.utility import get_principal
from pyams_security_views.zmi.interfaces import IObjectSecurityMenu
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.schema.button import ResetButton, SubmitButton
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.timezone import tztime
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowState, IWorkflowVersions
from pyams_workflow.versions import WorkflowHistoryItem
from pyams_zmi.form import AdminAddForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

from pyams_content import _


@viewlet_config(name='change-owner.menu',
                context=IWfSharedContent, layer=IAdminLayer, view=Interface,
                manager=IObjectSecurityMenu, weight=10,
                permission=MANAGE_SITE_PERMISSION)
class WfSharedContentOwnerChangeMenu(NavigationMenuItem):
    """Shared content owner change menu"""

    label = _("Change owner")
    href = '#change-owner.html'


class IWfSharedContentOwnerChangeInfo(Interface):
    """Shared content owner change form fields"""

    new_owner = PrincipalField(title=_("New owner"),
                               description=_("The selected user will become the new content's owner"))

    keep_owner_as_contributor = Bool(title=_("Keep previous owner as contributor"),
                                     description=_("If 'yes', the previous owner will still be "
                                                   "able to modify this content"),
                                     required=False,
                                     default=False)


class IWfSharedContentOwnerChangeButtons(Interface):
    """Shared content owner change form buttons"""

    change = SubmitButton(name='change', title=_("Change owner"))
    reset = ResetButton(name='reset', title=_("Cancel"))


@ajax_form_config(name='change-owner.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_PERMISSION)
class WfSharedContentOwnerChangeForm(AdminAddForm):
    """Shared content owner change form"""

    title = _("Change content owner")
    legend = _("New owner selection")

    fields = Fields(IWfSharedContentOwnerChangeInfo)
    buttons = Buttons(IWfSharedContentOwnerChangeButtons)

    @handler(buttons['change'])
    def handle_change(self, action):
        super().handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        new_owner = data.get('new_owner')
        workflow = IWorkflow(self.context)
        translate = self.request.localizer.translate
        for version in IWorkflowVersions(self.context).get_versions():
            state = IWorkflowState(version)
            if state.state in workflow.readonly_states:
                continue
            roles = IWfSharedContentRoles(version)
            [previous_owner] = roles.owner
            roles.owner = {new_owner}
            contributors = roles.contributors.copy()  # don't modify contributors in place!!
            if data.get('keep_owner_as_contributor'):
                if previous_owner not in contributors:
                    contributors.add(previous_owner)
            else:
                if previous_owner in contributors:
                    contributors.remove(previous_owner)
            roles.contributors = contributors
            state.history.append(
                WorkflowHistoryItem(date=tztime(datetime.utcnow()),
                                    source_state=state.state,
                                    target_state=state.state,
                                    transition_id='--',
                                    principal=self.request.principal.id,
                                    comment=translate(_("Owner changed: {} -> {}")).format(
                                        get_principal(self.request, previous_owner).title,
                                        get_principal(self.request, new_owner).title
                                    )))
            self.request.registry.notify(ObjectModifiedEvent(version))


@viewlet_config(name='help',
                context=IWfSharedContent, layer=IAdminLayer,
                view=WfSharedContentOwnerChangeForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentOwnerChangeFormHelp(AlertMessage):
    """Shared content owner change form help"""

    status = 'info'

    _message = _("All versions of this content which are not archived will be transferred to "
                 "newly selected owner")
    message_renderer = 'markdown'


@adapter_config(required=(IWfSharedContent, IAdminLayer, WfSharedContentOwnerChangeForm),
                provides=IAJAXFormRenderer)
class SharedContentOwnerChangeFormAJAXRenderer(ContextRequestViewAdapter):
    """Shared content owner change form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        return {
            'status': 'reload'
        }
