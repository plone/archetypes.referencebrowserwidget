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
from plone.app.robotframework.testing import SIMPLE_PUBLICATION_FIXTURE

import archetypes.referencebrowserwidget


ATRB_SAMPLE_TYPES = PloneWithPackageLayer(
    zcml_package=archetypes.referencebrowserwidget,
    zcml_filename='testing.zcml',
    gs_profile_id='archetypes.referencebrowserwidget:testing',
    additional_z2_products=('archetypes.referencebrowserwidget',),
    name='ATRB_SAMPLE_TYPES',
)

ATRB_SAMPLE_TYPES_FUNCTIONAL = FunctionalTesting(
    bases=(
        ATRB_SAMPLE_TYPES,
    ),
    name="ATRB_SAMPLE_TYPES_FUNCTIONAL",
)


class ReferenceBrowserWidgetWithData(Layer):

    def setUp(self):
        self.createMemberArea()
        self.createDefaultStructure()

    def createMemberArea(self):
        with ploneSite() as portal:
            setRoles(portal, TEST_USER_ID, ['Manager'])
            members = makeContent(portal, portal_type='Folder', id='Members')
            portal.portal_membership.memberareaCreationFlag = True
            portal.portal_membership.createMemberArea()
            pw = portal.portal_workflow
            pw.doActionFor(members, 'publish')

    def createDefaultStructure(self):
        with ploneSite() as portal:
            makeContent(portal, portal_type='Folder', id='layer1')
            portal.layer1.setTitle('Layer1')
            portal.layer1.reindexObject()
            makeContent(portal.layer1, portal_type='Folder', id='layer2')
            folder = portal.layer1.layer2
            folder.setTitle('Layer2')
            folder.reindexObject()
            setRoles(portal, TEST_USER_ID, ['Member'])


ATRB_WITH_DATA = ReferenceBrowserWidgetWithData(
    bases=(
        ATRB_SAMPLE_TYPES,
        SIMPLE_PUBLICATION_FIXTURE,
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


class DummySession(dict):

    def set(self, key, value):
        self[key] = value


class DummyObject(object):

    def __init__(self, location):
        self.location = location

    def getPhysicalPath(self):
        return self.location.split('/')
