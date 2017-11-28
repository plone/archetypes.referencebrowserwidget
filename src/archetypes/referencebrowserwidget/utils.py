import new
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import BoundPageTemplate
from ZODB.POSException import ConflictError
from plone.registry.interfaces import IRegistry
from zope import interface
from zope.browserpage import namedtemplate
from zope.component import getMultiAdapter
from zope.component import getUtility

try:
    # chameleon-compatible page templates
    from five.pt.pagetemplate import ViewPageTemplateFile as ChameleonPageTemplateFile
    HAS_CHAMELEON = True
except ImportError:
    HAS_CHAMELEON = False


def getStartupDirectory(context, directory=''):
    """ Construct a path from `context` and `directory`

        Mapping works as follows:

        directory == ''                  => Current object
        directory == '/absolute/url'     => Portal root + absolute url
        directory == '../relative/url'   => Current object + relative url

        If the object is in the portal_factory, remove the factory from the
        equation.
        This creates an inconsistency with the case when directory is not set,
        because the current object is in the factory and thus not generally
        useful as a starting point for browsing (it won't contain any sub-
        objects, and the parent object is the factory's temporary folder).
        Hence, in this case, the startup directory is the parent folder.

        Similarly, if directory is a relative path starting with '../' and
        the object is in the factory, let the first '../' part of the relative
        URL refer to the destination parent folder, not the factory.

        Default case - if no directory is given, search for a property
        refwidget_startupdirectories in portal_properties/site_properties
        that is a lines field having the following
        form:
            path1:path2
        path1 is the path where all widgets being under it set
        startup_directory to path2 if no startup_directory is set.
    """

    def filterPortalFactory(url):
        """Return context's url + the relative url given, but remove any
        reference to portal_factory.
        """

        portal_factory = getToolByName(context, 'portal_factory')

        # Prepend / to ensure proper path separation, and ensure url is a string
        if url:
            url = '/' + url
        else:
            url = ''

        basePath = ''
        if portal_factory.isTemporary(context):
            pathParts = context.getPhysicalPath()

            # Remove the factory from the path
            pathParts = pathParts[:-3]

            # If the object is in the portal factory, we'll be relative to the
            # parent folder, not the temporary object which does not yet exist,
            # so remove any explicit ../ from the relative path
            if url.startswith('/..'):
                url = url[3:]

            basePath = '/'.join(pathParts)
        else:
            basePath = context.absolute_url(relative=1)

        # Resolve the URL
        try:
            targetPath = basePath + url
            obj = context.restrictedTraverse(targetPath)
            return obj.absolute_url()
        except ConflictError:
            raise
        except:
            return context.absolute_url()

    def checkPath(path):
        """ checks if path starts with /

            if, then path is relative to portal root
        """
        if path.startswith('/'):
            portal_url = getToolByName(context, 'portal_url')
            return portal_url() + path
        else:
            return path

    if directory.strip() == '':

        props = getToolByName(context, 'portal_properties').site_properties
        startups = getattr(props, 'refwidget_startupdirectories', '')
        ownpath = '/'.join(context.getPhysicalPath())

        # remove portal path - / is always portal_root
        url_tool = getToolByName(context, 'portal_url')
        ownpath = ownpath.replace(url_tool.getPortalPath(), '')

        for pathdef in startups:
            psplit = pathdef.split(':')
            if ownpath[0:len(psplit[0])] == psplit[0]:
                dopath = psplit[1].strip()
                if checkPath(dopath) == dopath:
                    return filterPortalFactory(dopath)
                else:
                    return checkPath(dopath)

        return filterPortalFactory(None)

    # If we have an absolute URL, return it relative to the portal root
    checked = checkPath(directory)
    if checked != directory:
        return checked

    # Else, if we have a relative URL, get it relative to the context.
    return filterPortalFactory(directory)


def quotestring(s):
    """ Return a double-quoted string

        >>> quotestring('hello world!')
        '"hello world!"'
    """
    return '"%s"' % s


def quotequery(s):
    """ Quote a string query

        Quote reserved query words, if they occur on special
        positions:

        >>> quotequery('foo and')
        'foo "and"'
    """
    if not s:
        return s

    try:
        terms = s.split()
    except (ConflictError, KeyboardInterrupt):
        raise
    except:
        return s

    tokens = ('OR', 'AND', 'NOT')
    s_tokens = ('OR', 'AND')
    check = (0, -1)
    for idx in check:
        if terms[idx].upper() in tokens:
            terms[idx] = quotestring(terms[idx])

    for idx in range(1, len(terms)):
        if (terms[idx].upper() in s_tokens and
                terms[idx-1].upper() in tokens):
            terms[idx] = quotestring(terms[idx])

    return ' '.join(terms)


def getSearchCatalog(context, name=''):
    """ Get named catalog in portal of context with fallback
    """
    search_catalog = name or 'portal_catalog'
    portal_catalog = getToolByName(context, 'portal_catalog')
    catalog = getToolByName(context, search_catalog, portal_catalog)
    if not hasattr(catalog, 'searchResults'):
        catalog = portal_catalog

    return catalog


def getTypesUseViewActionInListings(context, request):
    try:
        portal_properties = getMultiAdapter((context, request),
                                            name=u'plone_tools').properties()
        site_properties = portal_properties.site_properties
        return site_properties.typesUseViewActionInListings
    except (AttributeError, KeyError):
        # plone 5
        registry = getUtility(IRegistry)
        return registry.get('plone.types_use_view_action_in_listings', [])


class NamedTemplateAdapter(object):
    """A named template adapter implementation that has the ability
    to lookup the template portion from regular traversal (intended for
    being able to customize the template portion of a view component
    in the traditional portal_skins style).
    """

    interface.implements(namedtemplate.INamedTemplate)

    def __init__(self, context):
        self.context = context

    @property
    def macros(self):
        return self.default_template.macros

    def __call__(self, *args, **kwargs):
        context = aq_inner(self.context)
        context_of_context = aq_inner(context.context)
        view = context.__of__(context_of_context)

        # self.default_template is a ViewPageTemplateFile, which is a property descriptor
        # whose __get__ method returns a BoundPageTemplate.  That expects to be accessed from
        # a view, but we're accessing it from a NamedTemplateAdapter so we have to be sneaky and
        # make our own BoundPageTemplate rather than calling self.default_template directly.
        return BoundPageTemplate(self.__class__.__dict__['default_template'], view)(*args, **kwargs)


def named_template_adapter(template):
    """Return a new named template adapter which defaults the to given
    template.
    """

    new_class = new.classobj('GeneratedClass',
                             (NamedTemplateAdapter,),
                             {})
    if HAS_CHAMELEON:
        template = ChameleonPageTemplateFile(template.filename)
    new_class.default_template = template
    return new_class
