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
    
    from zope.interface import Interface
    from zope.schema import Bool
    
    from pyams_content.component.paragraph.interfaces import IBaseParagraph
    from pyams_content.component.paragraph.schema import ParagraphRendererChoice
    from pyams_gis.schema import GeoPointField
    
    from pyams_content import _
    
    
    MAP_PARAGRAPH_TYPE = 'map'
    MAP_PARAGRAPH_NAME = _("Location map")
    MAP_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.map.renderers'
    MAP_PARAGRAPH_ICON_CLASS = 'fas fa-map-marker'
    
    
    class IMapInfo(Interface):
        """Base map settings interface"""
        
        position = GeoPointField(title=_("Map position"),
                                 description=_("GPS coordinates used to locate map"),
                                 required=False)
        
        display_marker = Bool(title=_("Display location mark?"),
                              description=_("If 'yes', a location marker will be displayed on map"),
                              required=True,
                              default=True)

        display_coordinates = Bool(title=_("Display coordinates?"),
                                   description=_("If 'yes', GPS coordinates (if GPS position "
                                                 "is defined) will be displayed below the map"),
                                   required=True,
                                   default=False)
        
        
    class IMapParagraph(IMapInfo, IBaseParagraph):
        """Map paragraph interface"""
        
        renderer = ParagraphRendererChoice(description=_("Presentation template used for this map"),
                                           renderers=MAP_PARAGRAPH_RENDERERS)
