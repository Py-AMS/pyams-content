# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

try:
    import pyams_gis
except ImportError:
    pyams_gis = None
else:
    
    from pyams_content.component.map.interfaces import IMapInfo
    from pyams_i18n.schema import I18nTextLineField
    from pyams_portal.interfaces import IPortletSettings
    
    from pyams_content import _
    
    
    class IMapPortletSettings(IPortletSettings, IMapInfo):
        """Map portlet settings interface"""
        
        title = I18nTextLineField(title=_("Title"),
                                  required=False)
