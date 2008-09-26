import unittest

from zope.component import getMultiAdapter

from Products.Archetypes.tests.utils import makeContent

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

    def test_variables(self):
        fieldname = 'multiRef2'
        request = self.app.REQUEST
        request.set('at_url', '/plone/Members/test_user_1_/')
        request.set('fieldName', fieldname)
        request.set('fieldRealName', fieldname)
        makeContent(self.folder, portal_type='RefBrowserDemo', id='ref')
        obj = self.folder.ref
        obj.reindexObject()
        popup = getMultiAdapter((obj, request), name='refbrowser_popup')
        popup.update()
        relfield = obj.getField(fieldname)

        assert popup.at_url == '/plone/Members/test_user_1_/'
        assert popup.fieldName == fieldname
        assert popup.fieldRealName == fieldname
        assert popup.search_text == ''
        assert popup.field == relfield
        assert popup.multiValued == 1
        assert popup.search_index == relfield.widget.default_search_index
        assert popup.allowed_types == ()
        assert popup.at_obj == obj
        assert popup.close_window == 1


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(ProductsTestCase),
        unittest.makeSuite(PopupTestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
