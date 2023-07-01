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

"""PyAMS_content.shared.common.alert.interfaces module

This module defines interfaces of alerts tool and contents.
"""

from collections import OrderedDict
from enum import Enum

from zope.interface import Invalid, invariant
from zope.schema import Choice, Int, URI
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.shared.common import ISharedContent, IWfSharedContent
from pyams_content.shared.common.interfaces import ISharedTool
from pyams_i18n.schema import I18nTextField
from pyams_sequence.interfaces import IInternalReferencesList
from pyams_sequence.schema import InternalReferenceField, InternalReferencesListField

__docformat__ = 'restructuredtext'

from pyams_content import _


ALERT_CONTENT_TYPE = 'alert'
ALERT_CONTENT_NAME = _("Alert")


class ALERT_GRAVITY(Enum):
    """Alert gravity enumeration"""
    alert = 'alert'
    alert_end = 'alert_end'
    info = 'info'
    warning = 'warning'
    recommend = 'recommend'


ALERT_GRAVITY_NAMES = OrderedDict((
    (ALERT_GRAVITY.alert, _("Alert")),
    (ALERT_GRAVITY.alert_end, _("End of alert")),
    (ALERT_GRAVITY.info, _("Information")),
    (ALERT_GRAVITY.warning, _("Warning")),
    (ALERT_GRAVITY.recommend, _("Recommendation"))
))

ALERT_GRAVITY_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in ALERT_GRAVITY_NAMES.items()
])


class IWfAlert(IWfSharedContent, IInternalReferencesList):
    """Alert interface"""

    gravity = Choice(title=_("Alert gravity"),
                     description=_("Alert gravity can affect renderer alert style"),
                     required=True,
                     vocabulary=ALERT_GRAVITY_VOCABULARY,
                     default='info')

    body = I18nTextField(title=_("Message content"),
                         description=_("Message body"),
                         required=False)

    reference = InternalReferenceField(title=_("Internal reference"),
                                       description=_("Internal link target reference. You can "
                                                     "search a reference using '+' followed by "
                                                     "internal number, or by entering text "
                                                     "matching content title"),
                                       required=False)

    external_url = URI(title=_("External URL"),
                       description=_("Alternate external URL"),
                       required=False)

    @invariant
    def check_url(self):
        if self.reference and self.external_url:
            raise Invalid(_("You can't set internal reference and external URI simultaneously!"))

    references = InternalReferencesListField(title=_("Concerned contents"),
                                             description=_("If any, these contents will "
                                                           "automatically display this alert"),
                                             required=False)

    maximum_interval = Int(title=_("Maximum interval"),
                           description=_("Maximum interval between alert displays on a given "
                                         "device, given in hours; set to 0 to always display "
                                         "the alert"),
                           required=True,
                           min=0,
                           default=48)


class IAlert(ISharedContent):
    """Workflow managed alert interface"""


class IAlertManager(ISharedTool):
    """Alert manager interface"""

    def find_context_alerts(self, context=None, request=None):
        """Find alerts associated with given context"""
