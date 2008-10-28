from zope.interface import implements
from zope.interface import Interface
from zope.interface import Attribute
from zope.component import getMultiAdapter
from zope.app.form.browser.widget import SimpleInputWidget
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from widget import ReferenceBrowserWidget

class DummyField(object):
    """An Archetypes Field dummy.
    """
    
    def __init__(self):
        self.multiValued = False

class IReferenceBrowserWidgetProperties(Interface):
    """Propertied for the bridged reference browser widget.
    
    XXX: this is just a stub and shows how the mechanism works. someone should
    complete this interface as well as the default properties.
    """
    
    popup_width = Attribute(u"popup widtg")
    popup_height = Attribute(u"popup height")

class DefaultReferenceBrowserWidgetProperties(object):
    """Default implementation of IReferenceBrowserWidgetProperties.
    
    XXX: See IReferenceBrowserWidgetProperties docstring.
    """
    
    popup_width = 500
    popup_height = 550

class ReferenceBrowserWidgetEdit(SimpleInputWidget, ReferenceBrowserWidget):
    """A bridge of ReferenceBrowserWidget to be used for zope.formlib.
    """
    
    __call__ = ViewPageTemplateFile('browser/edit.pt')
    
    def __getattr__(self, name):
        if self._properties.has_key(name):
            return self._properties[name]
        return super(ReferenceBrowserWidgetEdit, self).__getattr__(name)
    
    @property
    def refs(self):
        return []
    
    @property
    def fieldName(self):
        return 'hallo'
    
    @property
    def multiValued(self):
        return False # test with true either :)
    
    @property
    def value(self):
        return None
    
    def getPhysicalPath(self):
        return ['p1']
    
    def getStartupDirectory(self):
        return 'http://localhost:8080/p1'
    
    def getName(self):
        """Maybe same as fieldName ??
        """
        return 'hallo'
    
    def getBaseQuery(self, instance, field):
        """Return base query to use for content search
        
        """
        return {'portal_type': ''}
#        query = self.base_query
#        if query:
#            if type(query) is StringType and shasattr(instance, query):
#                method = getattr(instance, query)
#                results = method()
#            elif callable(query):
#                results = query()
#            elif isinstance(query,dict):
#                results = query
#        else:
#            results = {}
#
#        # Add portal type restrictions based on settings in field, if not part
#        # of original base_query the template tries to do this, but ignores
#        # allowed_types_method, which should override allowed_types
#        if not results.has_key('portal_type'):
#            allowed_types = getattr(field, 'allowed_types', ())
#            allow_method = getattr(field, 'allowed_types_method', None)
#            if allow_method is not None:
#                meth = getattr(instance, allow_method)
#                allowed_types = meth()
#            results['portal_type']=allowed_types
#
#        return results
    