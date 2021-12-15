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

from zope.component import getAdapter

from pyams_content.component.illustration import IBasicIllustration, IBasicIllustrationTarget, \
    IIllustration, IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.zmi.interfaces import IPropertiesEditForm
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IInnerSubForm
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='illustration',
                required=(IBasicIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class BasicIllustrationPropertiesEditForm(FormGroupSwitcher):
    """Basic illustration properties edit form"""

    legend = _("Main illustration")
    weight = 10

    fields = Fields(IBasicIllustration)
    prefix = 'illustration.'

    def get_content(self):
        return IIllustration(self.context)

    @property
    def mode(self):
        return self.parent_form.mode

    @property
    def state(self):
        return 'open' if self.get_content().has_data() else 'closed'


@adapter_config(name='illustration',
                required=(IIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class IllustrationPropertiesEditForm(BasicIllustrationPropertiesEditForm):
    """Illustration properties edit form"""

    fields = Fields(IIllustration)
    fields['renderer'].widget_factory = RendererSelectFieldWidget

    @property
    def state(self):
        return super().state if IBaseParagraph.providedBy(self.context) else 'open'


@adapter_config(name='link-illustration',
                required=(ILinkIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class LinkIllustrationPropertiesEditForm(BasicIllustrationPropertiesEditForm):
    """Link illustration properties edit form"""

    legend = _("Navigation link illustration")
    weight = 15

    prefix = 'link_illustration.'

    def get_content(self):
        return getAdapter(self.context, IIllustration, name='link')


@adapter_config(required=(IBasicIllustrationTarget, IAdminLayer,
                          BasicIllustrationPropertiesEditForm),
                provides=IAJAXFormRenderer)
class BasicIllustrationPropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Basic illustration properties AJAX form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        result = {
            'status': 'success',
            'message': self.request.localizer.translate(self.view.parent_form.success_message)
        }
        if 'data' in changes.get(IBasicIllustration, ()):
            result['callbacks'] = [
                get_json_widget_refresh_callback(self.view, 'data', self.request)
            ]
        return result
