import unittest

from zope.component import getMultiAdapter
from zope.component import provideAdapter
from zope.formlib.namedtemplate import INamedTemplate

from Testing import ZopeTestCase as ztc

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView

from plone.app.form._named import named_template_adapter

from Products.Archetypes.tests.utils import makeContent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch

from archetypes.referencebrowserwidget.tests.base import TestCase
from archetypes.referencebrowserwidget.tests.base import FunctionalTestCase
from archetypes.referencebrowserwidget.tests.base import PopupBaseTestCase
from archetypes.referencebrowserwidget.interfaces import IFieldRelation

from archetypes.referencebrowserwidget.browser import view

_marker = []

class ProductsTestCase(TestCase):

    def test_skininstall(self):
        assert 'referencebrowser' in self.portal.portal_skins.objectIds()

    def test_atadapter(self):
        makeContent(self.folder, portal_type='Document', id='doc1')
        makeContent(self.folder, portal_type='Document', id='doc2')
        self.folder.doc1.setRelatedItems(self.folder.doc2)

        field = self.folder.doc1.getField('relatedItems')
        relation = getMultiAdapter((self.folder.doc1, field),
                                   interface=IFieldRelation)
        assert len(relation) == 1
        assert relation[0] == self.folder.doc2

    def test_plonerelationsadapter(self):
        pass
        # XXX test plone.relations implementation

    def test_requiredbehavior_multi(self):
        """ A required field should throw an error, if no value is provided,
            not silently ignore it.
        """

        basic_auth = '%s:%s' % (ztc.user_name, ztc.user_password)

        makeContent(self.folder, portal_type='RefBrowserDemo', id='ref')
        makeContent(self.folder, portal_type='Document', id='doc')

        context = self.folder.ref

        field = context.getField('multiRef')
        field.required = True

        self.folder.doc.reindexObject()
        uid = self.folder.doc.UID()

        # with value
        form = {'singleRef': '',
                'multiRef2': [''],
                'multiRef': [uid]}
        assert field.widget.process_form(context, field, form,
                                         empty_marker=_marker)[0][0] == uid

        # without key
        form = {'singleRef': '',
                'multiRef2': ['']}
        value = field.widget.process_form(context, field, form,
                                           empty_marker=_marker)
        assert len(value) == 2
        assert value[0] == []
        assert value[0] is not _marker

        # without value
        form = {'singleRef': '',
                'multiRef2': [''],
                'multiRef': []}
        value = field.widget.process_form(context, field, form,
                                           empty_marker=_marker)
        assert len(value) == 2
        assert value[0] == []
        assert value[0] is not _marker

        # no value returns empty_marker
        form = {'singleRef': '',
                'multiRef2': ['']}
        value = field.widget.process_form(context, field, form,
                                          emptyReturnsMarker=True,
                                          empty_marker=_marker)
        assert value is _marker

    def test_requiredbehavior_single(self):
        """ A required field should throw an error, if no value is provided,
            not silently ignore it.
        """

        basic_auth = '%s:%s' % (ztc.user_name, ztc.user_password)

        makeContent(self.folder, portal_type='RefBrowserDemo', id='ref')
        makeContent(self.folder, portal_type='Document', id='doc')

        context = self.folder.ref

        field = context.getField('singleRef')
        field.required = True

        self.folder.doc.reindexObject()
        uid = self.folder.doc.UID()

        # with value
        form = {'singleRef': uid,
                'multiRef2': [''],
                'multiRef': []}
        assert field.widget.process_form(context, field, form,
                                         empty_marker=_marker)[0] == uid

        # without key
        form = {'multiRef2': ['']}
        value = field.widget.process_form(context, field, form,
                                           empty_marker=_marker)
        assert value is _marker

        # without value
        form = {'singleRef': '',
                'multiRef2': [''],
                'multiRef': []}
        value = field.widget.process_form(context, field, form,
                                           empty_marker=_marker)
        assert len(value) == 2
        assert value[0] == ''

        # no value returns empty_marker
        form = {}
        value = field.widget.process_form(context, field, form,
                                          emptyReturnsMarker=True,
                                          empty_marker=_marker)
        assert value is _marker


class PopupTestCase(PopupBaseTestCase):

    def test_variables(self):
        fieldname = 'multiRef2'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        relfield = self.obj.getField(fieldname)

        assert popup.at_url == '/plone/Members/test_user_1_/ref'
        assert popup.fieldName == fieldname
        assert popup.fieldRealName == fieldname
        assert popup.search_text == ''
        assert popup.field == relfield
        assert popup.multiValued == 1
        assert popup.search_index == relfield.widget.default_search_index
        assert popup.allowed_types == ()
        assert popup.at_obj == self.obj
        assert popup.filtered_indexes == ['Description', 'SearchableText']

        assert popup.template.default_template.__name__ == 'popup'

    def test_alternatetemplate(self):
        alternate_template = named_template_adapter(
            ViewPageTemplateFile('sample.pt'))
        provideAdapter(alternate_template, adapts=(BrowserView, ),
                       provides=INamedTemplate, name='alternate')
        fieldname = 'multiRef2'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)

        field = self.obj.getField(fieldname)
        field.widget.popup_name = 'alternate'

        popup = self._getPopup()
        assert popup.template.default_template.__name__ == 'sample'
        delattr(field.widget, 'popup_name')

    def test_close_window(self):
        # close popup after inserting a single reference
        fieldname = 'singleRef'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 1

        # don't close popup after inserting a multivalued reference
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 0

        # close popup after inserting a  multivalued reference, if forced
        fieldname = 'multiRef2'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 1

    def test_query(self):
        # normal query
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        self.request.set('search_index', 'getId')
        self.request.set('searchValue', 'news')
        popup = self._getPopup()
        batch = popup.getResult()
        assert isinstance(batch, Batch)
        assert len(batch) == 1
        assert batch[0].getObject() == self.portal.news
        assert popup.has_queryresults

    def test_noquery(self):
        # no query
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        self.request.set('search_index', 'getId')
        self.request.set('searchValue', '')
        popup = self._getPopup()
        batch = popup.getResult()
        assert isinstance(batch, Batch)
        assert len(batch) == 1
        assert batch[0].getObject() == self.obj
        assert popup.has_queryresults


class PopupBreadcrumbTestCase(PopupBaseTestCase):

    pat = ('http://nohost/plone%%srefbrowser_popup?fieldName=%s&'
           'fieldRealName=%s&at_url=/plone/Members/test_user_1_/ref')

    def test_breadcrumbs(self):
        """ Standard breadcrumbs """
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        bc = popup.breadcrumbs('Members')

        path = ''
        pat = self.pat % (fieldname, fieldname)
        for compare, bc in zip([('', 'Home'),
                                ('Members', 'Users'),
                                ('test_user_1_', 'test_user_1_'),
                                ('ref', 'ref')], bc):
            path += compare[0] + '/'
            assert bc['absolute_url'] == pat % path
            assert bc['Title'] == compare[1]

    def test_startup(self):
        """ The startup dir doesn't match the path we start with.

            -> the crumbs are empty except the home entry
        """
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        bc = popup.breadcrumbs('news')
        assert len(bc) == 1
        assert bc[0]['Title'] == 'Home'

    def test_restrictedbrowsing(self):
        """ Only browse startup-dir and below """
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)

        field = self.obj.getField(fieldname)
        field.widget.restrict_browsing_to_startup_directory = 1

        popup = self._getPopup()
        bc = popup.breadcrumbs('Members/test_user_1_')
        assert len(bc) == 2
        assert bc[0]['Title'] == 'test_user_1_'
        assert bc[1]['Title'] == 'ref'

        field.widget.restrict_browsing_to_startup_directory = 0

    def test_isNotSelf(self):
        catalog = getToolByName(self.portal, 'portal_catalog')

        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/ref')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)

        clip = self.folder.manage_copyObjects('ref')
        self.folder.manage_pasteObjects(clip)

        copy = self.folder['copy_of_ref']
        copy.reindexObject()

        refbrain = catalog(id='ref')[0]
        copybrain = catalog(id='copy_of_ref')[0]

        popup = self._getPopup()
        assert popup.isNotSelf(copybrain) == True
        assert popup.isNotSelf(refbrain) == False


class HelperViewTestCase(TestCase):

    def test_startupdirectory(self):
        makeContent(self.folder, portal_type='RefBrowserDemo', id='ref')
        context = self.folder.ref

        request = self.app.REQUEST

        field = context.getField('multiRef5')
        helper = view.ReferenceBrowserHelperView(context, request)

        # no query
        self.assertEqual(helper.getStartupDirectory(field),
                         'http://nohost/plone/Members/test_user_1_/ref')

        # dynamic query
        field.widget.startup_directory_method = 'dynamicDirectory'
        assert helper.getStartupDirectory(field) == '/bar/dynamic'

        # constant query
        field.widget.startup_directory_method = 'constantDirectory'
        assert helper.getStartupDirectory(field) == '/foo/constant'


class IntegrationTestCase(FunctionalTestCase):

    def test_multivalued(self):
        """ We want to support `multiValued=True/False` on fields,
            but need `1` or `0` for our widget, since we work with
            javascript there.
        """
        basic_auth = '%s:%s' % (ztc.user_name, ztc.user_password)

        makeContent(self.folder, portal_type='RefBrowserDemo', id='ref')
        context = self.folder.ref

        # this is the easy case
        field = context.getField('singleRef')
        field.multiValued = 0

        response = self.publish(context.absolute_url(1) + '/base_edit',
                              basic_auth)
        self.assert_(
            'onclick="javascript:refbrowser_removeReference(\'singleRef\', 0)"'
            in response.getBody())

        # we want to support this as well
        field = context.getField('singleRef')
        field.multiValued = False

        response = self.publish(context.absolute_url(1) + '/base_edit',
                              basic_auth)
        # this should be the same
        self.assert_(
            'onclick="javascript:refbrowser_removeReference(\'singleRef\', 0)"'
            in response.getBody())


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(ProductsTestCase),
        unittest.makeSuite(PopupTestCase),
        unittest.makeSuite(PopupBreadcrumbTestCase),
        unittest.makeSuite(HelperViewTestCase),
        unittest.makeSuite(IntegrationTestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
