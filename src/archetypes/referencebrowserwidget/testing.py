from plone.testing import z2

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

import archetypes.referencebrowserwidget


ATRB_SAMPLE_TYPES = PloneWithPackageLayer(
    zcml_package=archetypes.referencebrowserwidget,
    zcml_filename='testing.zcml',
    gs_profile_id='archetypes.referencebrowserwidget:testing',
    additional_z2_products=('archetypes.referencebrowserwidget',),
    name='ATRB_SAMPLE_TYPES',
)

ATRB_ROBOT_TESTING = FunctionalTesting(
    bases=(
        ATRB_SAMPLE_TYPES,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="ATRB_ROBOT_TESTING")
