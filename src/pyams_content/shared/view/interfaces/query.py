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

"""PyAMS_content.shared.view.interfaces.query module

This module defines views queries interfaces.
"""

from zope.interface import Attribute, Interface

__docformat__ = 'restructuredtext'


END_PARAMS_MARKER = object()


class IViewQuery(Interface):
    """View query interface"""

    def get_params(self, context, request=None, **kwargs):
        """Get static view query params"""

    def get_results(self, context, sort_index, reverse, limit,
                    request=None, aggregates=None, settings=None, **kwargs):
        """Get tuple of limited results and total results count"""


class IViewUserQuery(Interface):
    """View user search query interface"""

    def get_user_params(self, request=None):
        """Get dynamic user query params"""


class IViewQueryExtension(Interface):
    """Base view query extension"""

    weight = Attribute("Extension weight")


class IViewQueryParamsExtension(IViewQueryExtension):
    """View query extension interface"""

    def get_params(self, context, request=None):
        """Add params to catalog query

        This method may return an iterator.
        If defined settings are such that no result can be found (for example, if the view is
        defined to use context themes but context doesn't have any), method can yield a "None"
        value which will cancel query execution.
        """


class IViewQueryFilterExtension(IViewQueryExtension):
    """View query filter extension

    Query filters are applied after query execution, so they are generally slower than
    normal queries, but can sometimes handle more complex rules.
    """

    def filter(self, context, items, request=None):
        """Filter items after catalog query"""


VIEWS_MERGERS_VOCABULARY = 'pyams_content.views.mergers'

CONCAT_VIEWS_MERGE_MODE = 'concat'
RANDOM_VIEWS_MERGE_MODE = 'random'
ZIP_VIEWS_MERGE_MODE = 'zip'
ZIP_RANDOM_VIEWS_MERGE_MODE = 'zip_random'


class IViewsMerger(Interface):
    """Interface used to define views mergers

    Mergers are used to merge results of several views.
    """

    def get_results(self, views, context, ignore_cache=False, request=None):
        """Merge results of several views together"""
