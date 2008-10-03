import unittest

from zope.component import getMultiAdapter
from zope.component import provideAdapter
from zope.formlib.namedtemplate import INamedTemplate

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView

from plone.app.form._named import named_template_adapter

from Products.Archetypes.tests.utils import makeContent
from Products.CMFPlone import Batch

from archetypes.referencebrowserwidget.tests.base import TestCase
from archetypes.referencebrowserwidget.tests.base import PopupBaseTestCase
from archetypes.referencebrowserwidget.interfaces import IFieldRelation

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


class PopupTestCase(PopupBaseTestCase):

    def test_variables(self):
        fieldname = 'multiRef2'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        relfield = self.obj.getField(fieldname)

        assert popup.at_url == '/plone/Members/test_user_1_/'
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
        self.request.set('at_url', '/plone/Members/test_user_1_/')
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
        self.request.set('at_url', '/plone/Members/test_user_1_/')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 1

        # don't close popup after inserting a multivalued reference
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 0

        # close popup after inserting a  multivalued reference, if forced
        fieldname = 'multiRef2'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 1

    def test_query(self):
        # normal query
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
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
        self.request.set('at_url', '/plone/Members/test_user_1_/')
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
           'fieldRealName=%s&at_url=/plone/Members/test_user_1_/')

    def test_breadcrumbs(self):
        """ Standard breadcrumbs """
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
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
        self.request.set('at_url', '/plone/Members/test_user_1_/')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        bc = popup.breadcrumbs('news')
        assert len(bc) == 1
        assert bc[0]['Title'] == 'Home'

    def test_restrictedbrowsing(self):
        """ Only browse startup-dir and below """
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
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

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(ProductsTestCase),
        unittest.makeSuite(PopupTestCase),
        unittest.makeSuite(PopupBreadcrumbTestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
