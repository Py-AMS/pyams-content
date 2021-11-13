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

"""PyAMS_content.shared.common.zmi.dashboard module

This module provides dashboard management components which are common to all
shared contents.
"""

from pyramid.events import subscriber
from zope.annotation import IAttributeAnnotatable
from zope.dublincore.interfaces import IZopeDublinCore

from pyams_content.shared.common.interfaces import ISharedContent
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentModifier, \
    IDashboardContentNumber, IDashboardContentOwner, IDashboardContentStatus, \
    IDashboardContentStatusDatetime, IDashboardContentTimestamp, IDashboardContentVersion, \
    IDashboardTable
from pyams_security.interfaces import ISecurityManager
from pyams_sequence.interfaces import ISequentialIdInfo, ISequentialIdTarget, ISequentialIntIds
from pyams_table.interfaces import ITableRowUpdatedEvent
from pyams_utils.adapter import adapter_config
from pyams_utils.date import SH_DATETIME_FORMAT, format_datetime
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, \
    IWorkflowPublicationSupport, IWorkflowState, IWorkflowVersions
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_content import _


@subscriber(ITableRowUpdatedEvent,
            context_selector=IDashboardTable,
            row_context_selector=ISharedContent)
def handle_shared_content_table_row_update(event):
    """Shared content table row update event handler"""
    item_key = ICacheKeyValue(event.item)
    event.object.rows_state[item_key] = IWorkflowVersions(event.context).get_last_versions()[-1]


@adapter_config(required=(ISequentialIdTarget, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentNumber)
def sequence_target_number(context, request, column):
    """Sequence target number getter"""
    target = get_parent(context, ISequentialIdTarget)
    if target is not None:
        sequence_info = ISequentialIdInfo(context, None)
        if sequence_info is not None:
            sequence = get_utility(ISequentialIntIds, name=target.sequence_name)
            return sequence.get_base_oid(sequence_info.oid, target.sequence_prefix)
    return None


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatus)
def content_workflow_status(context, request, column):
    """Content workflow status getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        workflow = IWorkflow(context)
        result = request.localizer.translate(workflow.get_state_label(state.state))
        if state.state_urgency:
            result += ' <i class="fas fa-fw fa-exclamation-triangle text-danger"></i>'
        elif state.state in workflow.published_states:
            pub_info = IWorkflowPublicationInfo(context, None)
            if (pub_info is not None) and not pub_info.is_published():
                translate = request.localizer.translate
                result += ' <i class="fas fa-fw fa-hourglass-half opacity-75 hint align-base" ' \
                          '    data-offset="5" title="{}"></i>'.format(
                    translate(_("Content publication start date is not passed yet")))
        return result
    return None


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatusDatetime)
def content_workflow_status_datetime(context, request, column):
    """Content workflow status datetime getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        return format_datetime(state.state_date, SH_DATETIME_FORMAT,
                               request=request)
    return None


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentVersion)
def content_workflow_version(context, request, column):
    """Content workflow version getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        return str(state.version_id)
    return None


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentModifier)
def content_workflow_status_principal(context, request, column):
    """Content workflow status principal getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        manager = get_utility(ISecurityManager)
        return manager.get_principal(state.state_principal).title
    return None


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentOwner)
def content_workflow_owner(context, request, column):
    """Content workflow owner getter"""
    try:
        owner = context.owner
    except AttributeError:
        return None
    if owner:
        manager = get_utility(ISecurityManager)
        return manager.get_principal(next(iter(owner))).title
    return None


@adapter_config(required=(IAttributeAnnotatable, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentTimestamp)
def content_timestamp(context, request, column):
    """Content timestamp getter"""
    dc = IZopeDublinCore(context, None)
    if dc is not None:
        return format_datetime(tztime(dc.modified), SH_DATETIME_FORMAT,
                               request=request)
    return None
