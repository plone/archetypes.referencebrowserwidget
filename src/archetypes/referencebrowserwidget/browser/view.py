from zope.component import getMultiAdapter
from zope.formlib import namedtemplate

from Acquisition import aq_inner
from Acquisition import aq_base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError

from plone.app.form._named import named_template_adapter
from plone.memoize import view

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch

from archetypes.referencebrowserwidget import utils
from archetypes.referencebrowserwidget.interfaces import IFieldRelation

default_popup_template = named_template_adapter(
    ViewPageTemplateFile('popup.pt'))

class ReferenceBrowserHelperView(BrowserView):

    def getFieldRelations(self, field):
        return getMultiAdapter((self.context, field), interface=IFieldRelation)

    def getStartupDirectory(self, field):
        """ Return the path to the startup directory. """
        widget = field.widget
        directory = widget.startup_directory
        if widget.startup_directory_method:
            if getattr(aq_base(self.context),
                       widget.startup_directory_method, False):
                method = getattr(self.context, widget.startup_directory_method)
                if callable(method):
                    directory = method()
                else:
                    directory = method
                return method
        return utils.getStartupDirectory(self.context, directory)

class QueryCatalogView(BrowserView):

    def __call__(self, show_all=0,
                 quote_logic=0,
                 quote_logic_indexes=['SearchableText'],
                 search_catalog=None):

        results=[]
        catalog = utils.getSearchCatalog(aq_inner(self.context),
                                         search_catalog)
        indexes = catalog.indexes()
        query = {}
        show_query = show_all
        second_pass = {}

        for k, v in self.request.items():
            if v and k in indexes:
                if quote_logic and k in quote_logic_indexes:
                    v = utils.quotequery(v)
                query.update({k:v})
                show_query=1
            elif k.endswith('_usage'):
                key = k[:-6]
                param, value = v.split(':')
                second_pass[key] = {param:value}
            elif k in ('sort_on', 'sort_order', 'sort_limit'):
                query.update({k:v})

        for k, v in second_pass.items():
            qs = query.get(k)
            if qs is None:
                continue
            query[k] = q = {'query':qs}
            q.update(v)

# doesn't normal call catalog unless some field has been queried
# against. if you want to call the catalog _regardless_ of whether
# any items were found, then you can pass show_all=1.

        if show_query:
            try:
                results=catalog(**query)
            except ParseError:
                 pass

        return results


from zope.component import getAdapter

class ReferenceBrowserPopup(BrowserView):
    """ View class of Popup window """

    has_queryresults = True
    has_brain = False
    brainuid = None
    _updated = False

    def __init__(self, context, request):
        super(ReferenceBrowserPopup, self).__init__(context, request)

        portal_props = getToolByName(aq_inner(context), 'portal_properties')
        self.charset = portal_props.site_properties.default_charset
        self.request.response.setHeader('Content-Type',
                                        'text/html;;charset=%s' % self.charset)
        if self.request.get('clearHistory', None):
            self.request.SESSION.set('atrefbrowserwidget_history', [])

        self.at_url = request.get('at_url');
        self.fieldName = request.get('fieldName');
        self.fieldRealName = request.get('fieldRealName');
        self.search_text = request.get('searchValue', '');

    def __call__(self):
        self.update()
        return self.template()

    def update(self):
        context = aq_inner(self.context)

        catalog = getToolByName(context, 'portal_catalog')

        at_result = catalog.searchResults(dict(path=self.at_url));
        at_brain = at_result and at_result[0] or None;
        if at_brain:
            self.at_obj = at_brain.getObject()
            self.has_brain = True
            self.brainuid = at_brain.UID
        else:
            self.at_obj = context.restrictedTraverse(self.at_url);
        self.field = self.at_obj.Schema()[self.fieldRealName];
        self.widget = self.field.widget
        self.multiValued = int(self.field.multiValued)
        self.search_index = self.request.get('search_index',
                                             self.widget.default_search_index)
        self.request.set(self.search_index, self.search_text)

        base_query = self.widget.getBaseQuery(self.at_obj, self.field)
        self.allowed_types = base_query.get('portal_type', '')
        if not self.allowed_types:
            base_query.pop('portal_type')

        if base_query.keys():
            self.request.form.update(base_query)

        # close_window needs to be int, since it is used
        # with javascript
        self.close_window = int(not self.field.multiValued or
                                self.widget.force_close_on_insert)
        if self.widget.history_length > 0:
            self.insertHistory(self.request, self.widget.history_length)
        popup_name = getattr(self.widget, 'popup_name', 'popup')
        self.template = getAdapter(self, namedtemplate.INamedTemplate,
                                   name=popup_name or 'popup')
        self._updated = True

    @property
    def search_catalog(self):
        assert self._updated
        return utils.getSearchCatalog(aq_inner(self.context),
                                      self.widget.search_catalog)

    @property
    def filtered_indexes(self):
        assert self._updated
        indexes = self.search_catalog.indexes()
        avail = self.widget.available_indexes
        return [index for index in indexes if not avail or index in avail]

    @property
    def history_url(self):
        return "%s?%s&clearHistory=1" % (
            self.request.get('ACTUAL_URL', ''),
            self.request.get('QUERY_STRING', ''))

    def insertHistory(self, history_length=20):
        """ Keep url history in session

            Insert 'at_url' into the list of visited path in front.
            The history is stored as list of tuples
            (relative path to Zope root, relative_path to Plone portal root)
        """
        path = self.request.get('PATH_TRANSLATED')
        history = self.request.SESSION.get('atrefbrowserwidget_history', [])
        portal_path = self.context.portal_url.getPortalObject().absolute_url(1)

        # remove existing entries
        for i, tp in enumerate(history):
            if path == tp[0]:
                del history[i]
                break

        # generate a friendly path for UI representation
        visible_path = self.context.absolute_url(1)
        visible_path = visible_path.replace(portal_path, '')

        # insert at the head of the history list
        history.insert(0, (path, visible_path))

        # cut off oversized history
        history = history[:history_length]

        # put it back into the session
        history = self.request.SESSION.set('atrefbrowserwidget_history',
                                           history)

    def getResult(self):
        assert self._updated
        result = []
        if self.widget.show_results_without_query or self.search_text:

            qc = getMultiAdapter((self.context, self.request),
                                 name='refbrowser_querycatalog')

            # XXX do batching with query
            result = (self.widget.show_results_without_query or \
                      self.search_text) and \
                      qc(search_catalog=self.widget.search_catalog)

            self.has_queryresults = bool(result)

        elif self.widget.allow_browse:
            ploneview = getMultiAdapter((self.context, self.request),
                                        name="plone")
            folder = ploneview.getCurrentFolder()
            result = folder.getFolderContents(
                        contentFilter={'sort_on': 'sortable_title'})
        else:
            result = []
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))

        return Batch(result, b_size, b_start, orphan=1)

    def breadcrumbs(self, startup_directory):
        assert self._updated
        context = aq_inner(self.context)

        putils = getToolByName(context, 'plone_utils')
        portal = context.portal_url.getPortalObject()
        crumbs = putils.createBreadCrumbs(context)

        server_url = self.request.SERVER_URL
        if startup_directory.startswith('/'):
            startup_directory = startup_directory[1:]

        startup_folder = portal.restrictedTraverse(startup_directory)
        startup_folder_url = startup_folder.absolute_url()

        newcrumbs = []
        for c in crumbs:
            if c['absolute_url'].startswith(startup_folder_url):
                c['absolute_url'] = self.genRefBrowserUrl(c['absolute_url'])
                newcrumbs.append(c)

        if not self.widget.restrict_browsing_to_startup_directory:
            newcrumbs.insert(0,
                {'Title': 'Home',
                 'absolute_url': self.genRefBrowserUrl(portal.absolute_url())})
        return newcrumbs

    def genRefBrowserUrl(self, urlbase):
        assert self._updated
        return "%s/%s?fieldName=%s&fieldRealName=%s&at_url=%s" % (
       urlbase, self.__name__, self.fieldName, self.fieldRealName, self.at_url)


    def getUid(self, item):
        assert self._updated
        return (self.has_brain and item.UID or item.aq_explicit.UID) or None


    def isNotSelf(self, item):
        assert self._updated
        return self.has_brain and self.getUid(item) != self.brainuid or \
               item.getObject() != self.at_obj

    def isReferencable(self, item):
        assert self._updated
        item_referenceable = not self.allowed_types or \
            item.portal_type in self.allowed_types
        filter_review_states = self.widget.only_for_review_states is not None
        review_state_allows = filter_review_states and \
            item.review_state in (self.widget.only_for_review_states or ()) or \
            True
        return self.getUid(item) and item_referenceable and \
               review_state_allows and self.isNotSelf(item)


