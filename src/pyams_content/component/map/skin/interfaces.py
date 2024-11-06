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
    
    from zope.interface import Attribute, Interface
    from zope.schema import Bool, Int, Object
    
    from pyams_content.feature.renderer.interfaces import IRendererSettings
    from pyams_gis.interfaces.configuration import IMapConfiguration

    from pyams_content import _
    
    
    class IBaseMapRendererSettings(IMapConfiguration):
        """Map base renderer settings interface"""
        
        no_use_default_map_configuration = Bool(title=_("Don't use default configuration?"),
                                                required=True,
                                                default=False)
        
        use_default_map_configuration = Bool(title=_("Use default configuration?"),
                                             required=True,
                                             default=True)
        
        configuration = Attribute("Map configuration")
        
        map_height = Int(title=_("Map height"),
                         description=_("Map height, in pixels"),
                         required=True,
                         default=400)


    class IMapDefaultRendererSettings(IRendererSettings, IBaseMapRendererSettings):
        """Map default renderer settings"""
