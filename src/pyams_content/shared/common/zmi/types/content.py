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

from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_content.shared.common.zmi import SharedContentPropertiesEditForm


class TypedSharedContentPropertiesEditForm(SharedContentPropertiesEditForm):
    """Typed shared content properties edit form"""

    interface = IWfTypedSharedContent
    fieldnames = ('title', 'short_name', 'content_url', 'data_type',
                  'header', 'description', 'notepad')
