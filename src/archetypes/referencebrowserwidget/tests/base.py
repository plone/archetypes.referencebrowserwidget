from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

# setup session
app = ztc.app()
ztc.utils.setupCoreSessions(app)
ztc.close(app)

# setup sample types
from Products.GenericSetup import EXTENSION, profile_registry
profile_registry.registerProfile('referncebrowserwidget_sampletypes',
    'RefernceBrowserWidget Sample Content Types',
    'Extension profile including referncebrowserwidget sample content types',
    'profiles/sample_types',
    'archetypes.referencebrowserwidget',
    EXTENSION)

# install site
ptc.setupPloneSite(extension_profiles=[
    'archetypes.referencebrowserwidget:default',
    'archetypes.referencebrowserwidget:referncebrowserwidget_sampletypes'
    ])

import archetypes.referencebrowserwidget

class MixIn(object):
    """ Mixin for setting up the necessary bits for testing the
        archetypes.referencebrowserwidget
    """
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             archetypes.referencebrowserwidget)
            ptc.installPackage('archetypes.referencebrowserwidget')
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

class TestCase(MixIn, ptc.PloneTestCase):
    """ Base TestCase for archetypes.referencebrowserwidget """

class FunctionalTestCase(MixIn, ptc.FunctionalTestCase):
    """ Base FunctionalTestCase for archetypes.referencebrowserwidget """

