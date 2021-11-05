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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from zope.interface import implementer

from pyams_content.reference.pictogram import IPictogramTable
from pyams_content.reference.pictogram.zmi import get_pictogram_header
from pyams_form.browser.select import SelectWidget
from pyams_form.widget import FieldWidget
from pyams_utils.interfaces.data import IObjectData

from pyams_content import _
from pyams_utils.registry import query_utility
from pyams_utils.url import absolute_url


@implementer(IObjectData)
class PictogramSelectWidget(SelectWidget):
    """Pictogram selection widget"""

    no_value_message = _("No selected pictogram")

    pictograms = None
    label_id = None
    suffix = None

    def update(self):
        super().update()
        self.label_id = '{0}_header'.format(self.id)
        self.pictograms = query_utility(IPictogramTable)
        if self.value and (self.pictograms is not None):
            pictogram = self.pictograms.get(self.value[0])
            if pictogram is not None:
                self.suffix = '<span id="{0}" class="text-info">{1}</span>'.format(
                    self.label_id,
                    get_pictogram_header(pictogram, self.request))
                return
        self.suffix = '<span id="{0}" class="text-info">{1}</span>'.format(
            self.label_id,
            self.request.localizer.translate(_("Default header: --")))

    @property
    def object_data(self):
        """Object data getter"""
        return {
            'ams-change-handler': 'MyAMS.helpers.select2ChangeHelper',
            'ams-stop-propagation': 'true',
            'ams-select2-helper-type': 'html',
            'ams-select2-helper-url': absolute_url(self.pictograms, self.request,
                                                   'get-pictogram-header.html'),
            'ams-select2-helper-target': '#{0}'.format(self.label_id)
        }


def PictogramSelectFieldWidget(field, request):  # pylint: disable=invalid-name
    """Pictogram selection field widget factory"""
    return FieldWidget(field, PictogramSelectWidget(request))
