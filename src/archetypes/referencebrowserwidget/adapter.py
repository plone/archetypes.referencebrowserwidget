
def ATReferenceAdapter(context, field):
    relationship = field.relationship
    return [item.getTargetObject()
            for item in context.getReferenceImpl(relationship)]

def ATBackReferenceAdapter(context, field):
    relationship = field.relationship
    return [item.getTargetObject()
            for item in context.getBackReferenceImpl(relationship)]

def PloneRelationsAdapter(context, field):
    relationship = field.relationship
    from plone.app.relations.interfaces import IRelationshipSource
    return IRelationshipSource(context).getTargets(relation=relationship)


def PloneRelationsRevAdapter(context, field):
    relationship = field.relationship
    from plone.app.relations.interfaces import IRelationshipTarget
    return IRelationshipTarget(context).getSources(relation=relationship)

