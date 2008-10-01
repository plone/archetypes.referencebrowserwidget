import unittest, doctest

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.setup import default_user
from Products.PloneTestCase.setup import default_password

from archetypes.referencebrowserwidget.tests.base import FunctionalTestCase

def setUp(test):
    test.basic_auth = '%s:%s' % (default_user, default_password)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ztc.FunctionalDocFileSuite(
            'browser.txt',
            package='archetypes.referencebrowserwidget',
            setUp=setUp,
            test_class=FunctionalTestCase,
            ))

    suite.addTest(doctest.DocTestSuite(
            'archetypes.referencebrowserwidget.utils',
            ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
