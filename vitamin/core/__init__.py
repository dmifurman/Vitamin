from vitamin.config import Tweak, Parameter
from helpers.dictmapper import MappedDict
import inspect

class RequestContext():
    
    __slots__ = ["handler",
                 "block",
                 "arguments"]
    
    def __init__(self, ihandler):
        self.handler = ihandler
        self.block = None
        self.arguments = None

class VtCore(Tweak("Main")):
    
    def __init__(self):
        
        self.REGISTERED_MODULES = Parameter()
        self.REGISTERED_INTERFACES = Parameter()
        self.MODULE_IFACE_PREFFIX = Parameter("IModule")
        self.PRODUCTION_CHAIN = Parameter()
        self.tweak()
        
        self.modules = self.initModules()
        
    def initModules(self):        
        
        modules = {}
        for module in self.REGISTERED_MODULES: #lazy import
            ifaces = [x for x in inspect.getmro(module) 
                      if x.__name__.startswith(self.MODULE_IFACE_PREFFIX) 
                      and x.__name__ != self.MODULE_IFACE_PREFFIX]
            if len(ifaces) > 1: raise Exception("More then one IModule")
            iface = ifaces[0]
            if not iface in self.REGISTERED_INTERFACES:
                raise Exception("Interface {0} not registered".format(iface.__name__))
            modules[iface.__name__] = module()
                              
        notimpl = set([x.__name__ for x in self.REGISTERED_INTERFACES]).difference(
                                                                set(modules.keys()))
        if len(notimpl): 
            raise Exception("These interfaces not implemented: \n" + str(notimpl))
    
        chainfail = set(self.PRODUCTION_CHAIN).difference(set(modules.keys()))
        if len(chainfail):
            raise Exception("These interfaces not implemented: \n" + str(chainfail))
              
        return modules
    
    def createContext(self, ihandler):
        return RequestContext(ihandler)
    
    def chain(self, context):
        for node in self.PRODUCTION_CHAIN:
            self.modules[node].go(context)
        
    def go(self, ihandler):
        print("Ядру пришел запрос!")
        context = self.createContext(ihandler)
        self.chain(context)

