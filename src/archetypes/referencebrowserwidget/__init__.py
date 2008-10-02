from Products.CMFCore.utils import ContentInit
from Products.Archetypes.atapi import process_types, listTypes
from Products.CMFCore.permissions import AddPortalContent
from archetypes.referencebrowserwidget.config import PROJECTNAME
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

def initialize(context):
    import demo
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = AddPortalContent,
        extra_constructors = constructors,
        ).initialize(context)
