class Feature():
    
    PREFIX = "pre"
    POSTFIX = "post"
    
    def __init__(self):
        self.prefix_defined = False
        self.postfix_defined = False
    
    def preProcess(self, object, *args, **kwargs):
        return object, args, kwargs
    
    def postProcess(self, object, *args, **kwargs):
        return object, args, kwargs

    @classmethod
    def adapt(cls, name, feature):
        names = dir(feature)
        f = Feature()
        for n in names:
            if not f.prefix_defined and n.startswith(cls.PREFIX + name):
                f.prePocess = getattr(feature, n)
                f.prefix_defined = True
            elif not f.postfix_defined and n.startswith(cls.POSTFIX + name):
                f.postProcess = getattr(feature, n)
                f.postfix_defined = True
            if f.prefix_defined and f.postfix_defined:
                break
        return f                
    
    @classmethod
    def hook(cls, function):
        name = function.__name__     
        def __go(self, *args, **kwargs):            
            feature = self.feature
            adapted = Feature.adapt(name, feature)
            object, args, kwargs = adapted.preProcess(self, *args, **kwargs)
            result = function(object, *args, **kwargs)
            return adapted.postProcess(object, result)            
        return __go
    
class string(Feature):
    
    def preSomeFoo(self, *args, **kwargs):
        return (self, args, kwargs)

    def postSomeFoo(self, result):
        return not result

class T():
    
    feature = string
    
    @Feature.hook
    def SomeFoo(self):
        return True

t = T()
print(t.SomeFoo())
