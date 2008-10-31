from zope.interface import implements
from zope.interface import Interface
from zope.interface import Attribute
from zope.component import getAdapter
from zope.component.interfaces import ComponentLookupError
from zope.schema._bootstrapinterfaces import IFromUnicode
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner, aq_parent

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.interfaces import IContentish

from Products.CMFPlone.utils import getToolByName

from widget import ReferenceBrowserWidget

class IFieldDummy(Interface):
    """Interface for an Archetypes dummy field.
    """
    
    multiValued = Attribute(u'Flag wether field is multivalued or not')
    
    allowed_types = Attribute(u"Iterable of allowed types")
    
    allowed_types_method = Attribute(u"Method which return iterable of "
                                     "allowed types")

class FieldDummy(object):
    
    implements(IFieldDummy)
    
    def __init__(self, context):
        self.context = context
        self.multiValued = False
        self.allowed_types = ()
        self.allowed_types_method = None

class IReferenceBrowserWidgetProps(Interface):
    """Properties for the bridged reference browser widget.
    """
    
    properties = Attribute(u"Dictionary containing the widget properties")

class DefaultReferenceBrowserWidgetProps(object):
    """Default implementation of IReferenceBrowserWidgetProps.
    """
    
    implements(IReferenceBrowserWidgetProps)
    
    def __init__(self, context):
        self.context = context
    
    properties = {}

class ReferenceBrowserWidgetEdit(SimpleInputWidget, ReferenceBrowserWidget):
    """A bridge of ReferenceBrowserWidget to be used for zope.formlib.
    """
    
    __call__ = ViewPageTemplateFile('browser/edit.pt')
    
    def __init__(self, *args, **kw):
        SimpleInputWidget.__init__(self, *args, **kw)
        ReferenceBrowserWidget.__init__(self)
        bridge = self.bridge
        try:
            props = getAdapter(self.context,
                               IReferenceBrowserWidgetProps,
                               name=bridge)
        except ComponentLookupError, e:
            props = getAdapter(self.context,
                               IReferenceBrowserWidgetProps,
                               name=u'default')
        kw.update(props.properties)
        self._process_args(**kw)
    
    @property
    def comp_context(self):
        """Return the next available compliant context.
        
        first search for the next available acquisition chain, then aquire
        the next IContentish object or the site root.
        """
        if hasattr(self, '_comp_context'):
            return self._comp_context
        context = self.context
        while not hasattr(context, 'getPhysicalPath'):
            context = context.context
        while not IContentish.providedBy(context):
            if ISiteRoot.providedBy(context):
                break
            context = aq_parent(aq_inner(context))
        setattr(self, '_comp_context', context)
        return self._comp_context
    
    @property
    def field(self):
        if hasattr(self, '_fielddummy'):
            return self._fielddummy
        bridge = self.request.form.get('bridge', '')
        try:
            fielddummy = getAdapter(self.context, IFieldDummy, name=bridge)
        except ComponentLookupError, e:
            fielddummy = getAdapter(self.context, IFieldDummy, name=u'default')
        setattr(self, '_fielddummy', fielddummy)
        return self._fielddummy
    
    @property
    def bridge(self):
        bridge = self.request.form.get('bridge')
        if bridge:
            return bridge
        if IFromUnicode.providedBy(self.context):
            return self.context.getName()
        return ''
    
    @property
    def refs(self):
        if not IFromUnicode.providedBy(self.context):
            raise ValueError, u'no suitable context to query referenced objects'
        context = self.comp_context
        catalog = getToolByName(context, 'portal_catalog')
        
        # XXX: do some checks here
        # this implementation currently provides exactly text line field with
        # single value
        # * if value is a list even if stored in text, and so on ...
        brains = catalog(UID=self._getCurrentValue())
        return [brains[0].getObject()]
    
    @property
    def fieldName(self):
        return '%s%s' % (self._prefix, self.context.getName())
    
    @property
    def fieldRealName(self):
        return self.context.getName()
    
    @property
    def value(self):
        if IFromUnicode.providedBy(self.context):
            return self._getCurrentValue()
        return None
    
    def getPhysicalPath(self):
        return self.comp_context.getPhysicalPath()
    
    def getStartupDirectory(self):
        return self.comp_context.absolute_url()
