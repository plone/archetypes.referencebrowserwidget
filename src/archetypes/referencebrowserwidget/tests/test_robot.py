from plone.testing import layered

import robotsuite

from archetypes.referencebrowserwidget.testing import ATRB_ROBOT_TESTING


def test_suite():
    return layered(robotsuite.RobotTestSuite('robot/reference.robot'),
                layer=ATRB_ROBOT_TESTING)
