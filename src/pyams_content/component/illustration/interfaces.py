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

"""PyAMS_content.component.illustration.interfaces module

This module defines interfaces related to illustrations management.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope.schema import Choice, TextLine

from pyams_content.feature.renderer import IRenderedContent
from pyams_file.schema import I18nThumbnailMediaField
from pyams_i18n.schema import I18nTextField, I18nTextLineField

from pyams_content import _


BASIC_ILLUSTRATION_KEY = 'pyams_content.illustration.base'

ILLUSTRATION_KEY = 'pyams_content.illustration'
ILLUSTRATION_RENDERERS = 'pyams.illustration.renderers'

LINK_ILLUSTRATION_KEY = '{0}::link'.format(ILLUSTRATION_KEY)


class IBasicIllustration(Interface):
    """Basic illustration interface"""

    data = I18nThumbnailMediaField(title=_("Image or video data"),
                                   description=_("Image or video content"),
                                   required=False)

    def has_data(self):
        """Check if data is provided in any language"""

    title = I18nTextLineField(title=_("Legend"),
                              required=False)

    alt_title = I18nTextLineField(title=_("Accessibility title"),
                                  description=_("Alternate title used to describe image content"),
                                  required=False)

    author = TextLine(title=_("Author"),
                      description=_("Name of picture's author"),
                      required=False)


class IIllustration(IBasicIllustration, IRenderedContent):
    """Illustration paragraph"""

    description = I18nTextField(title=_("Associated text"),
                                description=_("Illustration description displayed in "
                                              "front-office templates"),
                                required=False)

    renderer = Choice(title=_("Illustration renderer"),
                      description=_("Renderer used to display illustration; please note that "
                                    "this renderer is not always used, but only in some specific "
                                    "contexts"),
                      vocabulary=ILLUSTRATION_RENDERERS,
                      default='default')


class ILinkIllustration(IBasicIllustration):
    """Navigation link illustration interface"""


class IIllustrationTargetBase(Interface):
    """Illustration base target interface"""


class IBasicIllustrationTarget(IIllustrationTargetBase):
    """Basic illustration target marker interface

    This interface is used to identify contexts which should handle only
    *basic* illustrations.
    """


class IIllustrationTarget(IBasicIllustrationTarget):
    """Base illustration target marker interface"""


class ILinkIllustrationTarget(IIllustrationTargetBase):
    """Link illustration target interface"""
