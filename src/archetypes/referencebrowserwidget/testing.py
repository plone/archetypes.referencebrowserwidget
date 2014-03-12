from Products.Archetypes.tests.utils import makeContent

from plone.testing import z2
from plone.testing import Layer

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import ploneSite
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

import archetypes.referencebrowserwidget


ATRB_SAMPLE_TYPES = PloneWithPackageLayer(
    zcml_package=archetypes.referencebrowserwidget,
    zcml_filename='testing.zcml',
    gs_profile_id='archetypes.referencebrowserwidget:testing',
    additional_z2_products=('archetypes.referencebrowserwidget',),
    name='ATRB_SAMPLE_TYPES',
)


class ReferenceBrowserWidgetWithData(Layer):

    def testSetUp(self):
        self.createDefaultStructure()

    def testTearDown(self):
        self.removeDefaultStructure()

    def createDefaultStructure(self):
        with ploneSite() as portal:
            if 'layer1' not in portal.objectIds():
                setRoles(portal, TEST_USER_ID, ['Manager'])
                makeContent(portal, portal_type='Folder', id='layer1')
                portal.layer1.setTitle('Layer1')
                portal.layer1.reindexObject()
                makeContent(portal.layer1, portal_type='Folder', id='layer2')
                self.folder = portal.layer1.layer2
                self.folder.setTitle('Layer2')
                self.folder.reindexObject()
                setRoles(portal, TEST_USER_ID, ['Member'])
        self['layer2'] = portal.layer1.layer2

    def removeDefaultStructure(self):
        with ploneSite() as portal:
            if 'layer1' in portal.objectIds():
                portal._delObject('layer1')

ATRB_WITH_DATA = ReferenceBrowserWidgetWithData(
    bases=(
        ATRB_SAMPLE_TYPES,
    ),
    name="ATRB_WITH_DATA",
)

ATRB_WITH_DATA_INTEGRATION = IntegrationTesting(
    bases=(
        ATRB_WITH_DATA,
    ),
    name="ATRB_WITH_DATA_INTEGRATION",
)

ATRB_WITH_DATA_FUNCTIONAL = FunctionalTesting(
    bases=(
        ATRB_WITH_DATA,
    ),
    name="ATRB_WITH_DATA_FUNCTIONAL",
)

ATRB_ROBOT_TESTING = FunctionalTesting(
    bases=(
        ATRB_SAMPLE_TYPES,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="ATRB_ROBOT_TESTING",
)
