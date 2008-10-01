import unittest

from zope.component import getMultiAdapter

from Products.Archetypes.tests.utils import makeContent
from Products.CMFPlone import Batch

from archetypes.referencebrowserwidget.tests.base import TestCase
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


class PopupTestCase(TestCase):

    def afterSetUp(self):
        makeContent(self.folder, portal_type='RefBrowserDemo', id='ref')
        self.obj = self.folder.ref
        self.obj.reindexObject()
        self.request = self.app.REQUEST

    def _getPopup(self, obj=None, request=None):
        if obj is None:
            obj = self.obj
        if request is None:
            request = self.request
        popup = getMultiAdapter((obj, request), name='refbrowser_popup')
        popup.update()
        return popup

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


    def test_close_window(self):
        # close popup after inserting single reference
        fieldname = 'singleRef'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 1

        # don't close popup after inserting multivalued reference
        fieldname = 'multiRef3'
        self.request.set('at_url', '/plone/Members/test_user_1_/')
        self.request.set('fieldName', fieldname)
        self.request.set('fieldRealName', fieldname)
        popup = self._getPopup()
        assert popup.close_window == 0

        # close popup after inserting multivalued reference, if forced
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
        assert not popup.has_queryresults

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(ProductsTestCase),
        unittest.makeSuite(PopupTestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
