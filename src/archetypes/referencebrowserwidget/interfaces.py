
from zope.interface import Interface
from Products.Archetypes.interfaces import IObjectField

class IFieldRelation(Interface):
    """ """


class IATReferenceField(IObjectField):
    """ Missing marker for Products.Archetypes.Field.ReferenceField """

class IATBackRefereneceField(IObjectField):
    """ Missing marker for Products.ATBackRef.BackReferenceField """


class IPloneRelationsRefField(IObjectField):
    """ Missing marker for plone.relations.PloneRelationsATField """

class IPloneRelationsRevRefField(IObjectField):
    """ Missing marker for plone.relations.ReversePloneRelationsATField """


