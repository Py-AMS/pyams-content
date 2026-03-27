# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.feature.script.interfaces import IScriptContainer

__docformat__ = 'restructuredtext'


def evolve(site):
    """Evolve 2: update scripts position"""
    scripts_container = IScriptContainer(site, None)
    if scripts_container is not None:
        for script in scripts_container.values():
            bottom_script = getattr(script, 'bottom_script', False)
            if bottom_script:
                script.position = 'bottom'
            else:
                script.position = 'head'
            if hasattr(script, 'bottom_script'):
                delattr(script, 'bottom_script')
