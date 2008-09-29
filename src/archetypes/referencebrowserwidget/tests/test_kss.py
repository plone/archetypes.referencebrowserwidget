import unittest
from pprint import pprint
from kss.core.tests.base import KSSViewTestCaseMixin

from plone.app.kss.tests.kss_and_plone_layer import KSSAndPloneLayer

from Products.Archetypes.tests.utils import makeContent

from archetypes.referencebrowserwidget.tests.base import FunctionalTestCase
from archetypes.referencebrowserwidget.browser import kssview

class KSSTestCase(FunctionalTestCase, KSSViewTestCaseMixin):
    """ Test KSS features """

    layer = KSSAndPloneLayer

    def afterSetUp(self):
        self.setDebugRequest()


    def test_moveup(self):
        view = kssview.KSSMoveReferencesView(self.portal, self.app.REQUEST)
        assert view.moveUp(1, 2, 'foo') == [
            {'name': 'moveNodeBefore',
             'params': {'html_id': u'ref-foo-0'},
             'selector': 'li#ref-foo-1',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'id', 'value': u'ref-foo-1'},
             'selector': 'li#ref-foo-0',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'id', 'value': u'ref-foo-0'},
             'selector': 'li#ref-foo-1',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveUp kssattr-pos-1 kssattr-length-2 kssattr-field-foo'},
             'selector': 'li#ref-foo-1 img.moveUp',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveDown kssattr-pos-1 kssattr-length-2 kssattr-field-foo'},
             'selector': 'li#ref-foo-1 img.moveDown',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveUp kssattr-pos-0 kssattr-length-2 kssattr-field-foo'},
             'selector': 'li#ref-foo-0 img.moveUp',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveDown kssattr-pos-0 kssattr-length-2 kssattr-field-foo'},
             'selector': 'li#ref-foo-0 img.moveDown',
             'selectorType': ''}]

    def test_movedown(self):
        view = kssview.KSSMoveReferencesView(self.portal, self.app.REQUEST)
        #        pprint(view.moveDown(0, 2, 'bar'))
        assert view.moveDown(0, 2, 'bar') == [
            {'name': 'moveNodeAfter',
             'params': {'html_id': u'ref-bar-1'},
             'selector': 'li#ref-bar-0',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'id', 'value': u'ref-bar-1'},
             'selector': 'li#ref-bar-0',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'id', 'value': u'ref-bar-0'},
             'selector': 'li#ref-bar-1',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveUp kssattr-pos-0 kssattr-length-2 kssattr-field-bar'},
             'selector': 'li#ref-bar-0 img.moveUp',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveDown kssattr-pos-0 kssattr-length-2 kssattr-field-bar'},
             'selector': 'li#ref-bar-0 img.moveDown',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveUp kssattr-pos-1 kssattr-length-2 kssattr-field-bar'},
             'selector': 'li#ref-bar-1 img.moveUp',
             'selectorType': ''},
            {'name': 'setAttribute',
             'params': {'name': u'class',
                        'value': u'moveDown kssattr-pos-1 kssattr-length-2 kssattr-field-bar'},
             'selector': 'li#ref-bar-1 img.moveDown',
             'selectorType': ''}]

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(KSSTestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
