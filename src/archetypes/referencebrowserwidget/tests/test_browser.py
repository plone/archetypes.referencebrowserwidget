import unittest
import doctest

from plone.testing import layered

from archetypes.referencebrowserwidget.testing import (
    ATRB_WITH_DATA_FUNCTIONAL,
)


optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    return unittest.TestSuite([
        layered(
            doctest.DocFileSuite(
                'reference_access.txt',
                'reference_order.txt',
                optionflags=optionflags,
            ),
            layer=ATRB_WITH_DATA_FUNCTIONAL,
        ),
    ])
