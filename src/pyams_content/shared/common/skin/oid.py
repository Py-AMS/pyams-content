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

__docformat__ = 'restructuredtext'

from pyramid.httpexceptions import HTTPNotFound
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable

from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_sequence.interfaces import ISequentialIntIds
from pyams_sequence.reference import get_reference_target
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.interfaces import DISPLAY_CONTEXT_KEY_NAME
from pyams_utils.registry import get_utility
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowVersions


@adapter_config(name='+',
                required=(Interface, IPyAMSUserLayer),
                provides=ITraversable)
@adapter_config(name='oid',
                required=(Interface, IPyAMSUserLayer),
                provides=ITraversable)
class OIDTraverser(ContextRequestAdapter):
    """++oid++ traverser

    This traverser can be used to get direct access to any content having an OID.
    The general URL syntax is "*/++oid++{oid}::{title}.html", where {oid} is the internal OID
    of the requested content, and "title" it's "content URL" attribute.

    A shorter syntax, is now available: */+/{oid}::{title}.html
    """

    def traverse(self, name, furtherpath=None):
        """++oid++ namespace traverser"""
        if not name:
            raise HTTPNotFound()
        context = self.context
        request = self.request
        if '::' in name:
            oid, _title = name.split('::', 1)
        else:
            oid, _title = name, ''
        sequence = get_utility(ISequentialIntIds)
        reference = sequence.get_full_oid(oid)
        target = get_reference_target(reference)
        if target is not None:
            workflow = IWorkflow(target, None)
            if workflow is not None:
                versions = IWorkflowVersions(target, None)
                if versions is not None:
                    versions = versions.get_versions(workflow.visible_states, sort=True)
                    if versions:
                        target = versions[-1]
        if (target is not None) and not IWorkflowPublicationInfo(target).is_visible(request):
            target = None
        if target is not None:
            request.annotations[DISPLAY_CONTEXT_KEY_NAME] = context
            request.context = target
            return target
        raise HTTPNotFound()
