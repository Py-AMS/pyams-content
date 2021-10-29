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

"""PyAMS_content.shared.common.interfaces module

"""

__docformat__ = 'restructuredtext'

from pyams_content import _
from pyams_content.interfaces import CONTRIBUTOR_ROLE, GUEST_ROLE, IBaseContent, MANAGER_ROLE, \
    MANAGE_CONTENT_PERMISSION, OWNER_ROLE, \
    PILOT_ROLE, \
    READER_ROLE, WEBMASTER_ROLE
from zope.container.constraints import containers, contains
from zope.container.interfaces import IContainer

from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Text, TextLine

from pyams_i18n.schema import I18nTextField
from pyams_portal.interfaces import DESIGNER_ROLE, IPortalContext
from pyams_security.schema import PrincipalField, PrincipalsSetField
from pyams_site.interfaces import ISiteRoot
from pyams_utils.schema import TextLineListField
from pyams_workflow.interfaces import IWorkflowManagedContent


class IDeletableElement(Interface):
    """Deletable element interface"""

    def is_deletable(self):
        """Check to know if a site element can be deleted"""


CONTENT_MANAGER_ROLES = 'pyams_content.manager.roles'


class IBaseContentManagerRoles(Interface):
    """Shared tool roles interface"""

    webmasters = PrincipalsSetField(title=_("Webmasters"),
                                    description=_("Webmasters can handle all contents, including "
                                                  "published ones"),
                                    role_id=WEBMASTER_ROLE,
                                    required=False)

    pilots = PrincipalsSetField(title=_("Pilots"),
                                description=_("Pilots can handle tool configuration, manage "
                                              "access rules, grant users roles and manage "
                                              "managers restrictions"),
                                role_id=PILOT_ROLE,
                                required=False)

    managers = PrincipalsSetField(title=_("Managers"),
                                  description=_("Managers can handle main operations in tool's "
                                                "workflow, like publish or retire contents"),
                                  role_id=MANAGER_ROLE,
                                  required=False)

    contributors = PrincipalsSetField(title=_("Contributors"),
                                      description=_("Contributors are users which are allowed to "
                                                    "create new contents"),
                                      role_id=CONTRIBUTOR_ROLE,
                                      required=False)

    designers = PrincipalsSetField(title=_("Designers"),
                                   description=_("Designers are users which are allowed to "
                                                 "manage presentation templates"),
                                   role_id=DESIGNER_ROLE,
                                   required=False)


class ISharedSite(IBaseContent, IDeletableElement):
    """Shared site interface"""

    containers(ISiteRoot)


class ISharedToolContainer(IBaseContent, IContainer):
    """Shared tools container"""

    containers(ISiteRoot)
    contains('.ISharedTool')


class IBaseSharedTool(IBaseContent, IContainer):
    """Base shared tool interface"""

    containers(ISharedToolContainer)

    shared_content_menu = Attribute("Boolean flag indicating if tool is displayed into 'Shared "
                                    "contents' or Shared tools' menu")

    shared_content_workflow = Choice(title=_("Workflow name"),
                                     description=_("Name of workflow utility used to manage tool "
                                                   "contents"),
                                     vocabulary="PyAMS workflows",
                                     default="PyAMS default workflow")


SHARED_TOOL_WORKFLOW_STATES_VOCABULARY = 'PyAMS workflow states'


class ISharedTool(IBaseSharedTool):
    """Shared tool interface"""

    contains('.ISharedContent')

    shared_content_type = Attribute("Shared data content type")
    shared_content_factory = Attribute("Shared data factory")


class ISharedToolPortalContext(ISharedTool, IPortalContext):
    """Shared tool with portal context"""


class ISharedToolRoles(IBaseContentManagerRoles):
    """Shared tool roles"""


class IWfSharedContent(IBaseContent):
    """Shared content interface"""

    content_type = Attribute("Content data type")
    content_name = Attribute("Content name")

    content_url = TextLine(title=_("Content URL"),
                           description=_("URL used to access this content; this is important for "
                                         "SEO and should include most important words describing "
                                         "content; spaces and underscores will be automatically "
                                         "replaced by hyphens"),
                           required=True)

    handle_content_url = Attribute("Static boolean value to specify if content URL is "
                                   "supported by this content type")

    creator = PrincipalField(title=_("Version creator"),
                             description=_("Name of content's version creator. "
                                           "The creator of the first version is also it's "
                                           "owner."),
                             required=True)

    first_owner = PrincipalField(title=_("First owner"),
                                 description=_("Name of content's first version owner"),
                                 required=True,
                                 readonly=True)

    creation_label = TextLine(title=_("Version creation"),
                              readonly=True)

    modifiers = PrincipalsSetField(title=_("Version modifiers"),
                                   description=_("List of principals who modified this content"),
                                   required=False)

    last_modifier = PrincipalField(title=_("Last modifier"),
                                   description=_("Last principal who modified this content"),
                                   required=False)

    last_update_label = TextLine(title=_("Last update"),
                                 readonly=True)

    header = I18nTextField(title=_("Header"),
                           description=_("Content's header is generally displayed in page "
                                         "header"),
                           required=False)

    handle_header = Attribute("Static boolean value to specify if header is supported by this "
                              "content type")

    description = I18nTextField(title=_("Meta-description"),
                                description=_("The content's description is 'hidden' into HTML's "
                                              "page headers; but it can be seen, for example, in "
                                              "some search engines results as content's "
                                              "description; if description is empty, content's "
                                              "header will be used."),
                                required=False)

    handle_description = Attribute("Static boolean value to specify if description is "
                                   "supported by this content type")

    keywords = TextLineListField(title=_("Keywords"),
                                 description=_("They will be included into HTML pages metadata"),
                                 required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("Internal information to be known about this content"),
                   required=False)


class IBaseContentPortalContext(IPortalContext):
    """Content portal context interface"""


class IWfSharedContentPortalContext(IWfSharedContent, IBaseContentPortalContext):
    """Shared content with portal support"""


class IWfSharedContentFactory(Interface):
    """Shared content factory interface"""


class IWfSharedContentRoles(Interface):
    """Shared content roles"""

    owner = PrincipalsSetField(title=_("Content owner"),
                               description=_("The owner is the creator of content's first "
                                             "version, except if it was transferred afterwards "
                                             "to another owner"),
                               role_id=OWNER_ROLE,
                               required=True,
                               max_length=1)

    managers = PrincipalsSetField(title=_("Managers"),
                                  description=_("Managers can handle main operations in tool's "
                                                "workflow, like publish or retire contents"),
                                  role_id=MANAGER_ROLE,
                                  required=False)

    contributors = PrincipalsSetField(title=_("Contributors"),
                                      description=_("Contributors are users which are allowed "
                                                    "to update this content in addition to "
                                                    "it's owner"),
                                      role_id=CONTRIBUTOR_ROLE,
                                      required=False)

    designers = PrincipalsSetField(title=_("Designers"),
                                   description=_("Designers are users which are allowed to "
                                                 "manage presentation templates"),
                                   role_id=DESIGNER_ROLE,
                                   required=False)

    readers = PrincipalsSetField(title=_("Readers"),
                                 description=_("Readers are users which are asked to verify and "
                                               "comment contents before they are published"),
                                 role_id=READER_ROLE,
                                 required=False)

    guests = PrincipalsSetField(title=_("Guests"),
                                description=_("Guests are users which are allowed to view "
                                              "contents with restricted access"),
                                role_id=GUEST_ROLE,
                                required=False)


class ISharedContent(IWorkflowManagedContent):
    """Workflow managed shared content interface"""

    visible_version = Attribute("Link to actually visible version")


class ISharedContentFactory(Interface):
    """Workflow managed shared content factory interface"""


CONTENT_TYPES_VOCABULARY = 'pyams_content.content.types'

SHARED_CONTENT_TYPES_VOCABULARY = 'pyams_content.shared_content.types'


#
# Generic restrictions interfaces
#

class IRestrictionInfo(Interface):
    """User restriction base interface"""

    principal_id = PrincipalField(title=_("Principal ID"),
                                  required=True)

    restriction_interface = Attribute("Restrictions interface")


class IRestrictions(Interface):
    """Restrictions manager interface"""

    restrictions_key = Attribute("Restrictions annotations key")
    restrictions_factory_interface = Attribute("Restrictions factory")

    def get_restrictions(self, principal, create_if_none=False):
        """Get manager restrictions for given principal"""

    def new_restrictions(self, principal):
        """Create new manager restrictions"""

    def set_restrictions(self, principal, restrictions=None):
        """Set manager restrictions for given principal"""

    def drop_restrictions(self, principal):
        """Drop manager restrictions for given principal"""


class IRestrictionsFactory(Interface):
    """Restrictions factory interface"""


#
# Shared tool contributor security restrictions
#

CONTRIBUTOR_RESTRICTIONS_KEY = 'pyams_content.contributor.restrictions'


class IContributorRestrictionInfo(IRestrictionInfo):
    """Shared content contributor restrictions"""

    publication_checks = Bool(title=_("Publication checks"),
                              description=_("If 'yes', this contributor will have to confirm "
                                            "that contents have been previewed and checked "
                                            "before asking for publication"),
                              required=False,
                              default=True)

    owners = PrincipalsSetField(title=_("Substitute for"),
                                description=_("Contributor will have access to contents owned "
                                              "by these principals"),
                                required=False)

    def check_access(self, context, permission=MANAGE_CONTENT_PERMISSION, request=None):
        """Check if principal is granted access to given context"""


class IContributorRestrictions(IRestrictions):
    """Contributor restrictions interface"""


class IContributorRestrictionsFactory(IRestrictionsFactory):
    """Contributor restrictions factory interface"""


#
# Shared tool manager security restrictions
#

MANAGER_RESTRICTIONS_KEY = 'pyams_content.manager.restrictions'


class IManagerRestrictionInfo(IRestrictionInfo):
    """Shared content manager restrictions"""

    publication_checks = Bool(title=_("Publication checks"),
                              description=_("If 'yes', this manager will have to confirm that "
                                            "contents have been previewed and checked before "
                                            "publishing a content"),
                              required=False,
                              default=True)

    restricted_contents = Bool(title=_("Restricted contents"),
                               description=_("If 'yes', this manager will get restricted access "
                                             "to manage contents based on selected settings"),
                               required=False,
                               default=True)

    owners = PrincipalsSetField(title=_("Selected owners"),
                                description=_("Manager will have access to contents owned "
                                              "by these principals"),
                                required=False)

    def check_access(self, context, permission=MANAGE_CONTENT_PERMISSION, request=None):
        """Check if principal is granted access to given content"""


class IManagerRestrictions(IRestrictions):
    """Manager restrictions interface"""


class IManagerRestrictionsFactory(IRestrictionsFactory):
    """Manager restrictions factory interface"""
