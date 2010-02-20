from collections import UserDict, OrderedDict

class MappedDict(UserDict):
    
    def __init__(self):
        UserDict.__init__(self)
        
    def __getattribute__(self, name):
        getter = super(MappedDict, self).__getattribute__
        try:
            return getter(name)
        except AttributeError as exp:
            if name in self: return self[name]
            else: raise exp

class MappedDictOrdered(OrderedDict):
    
    def __init__(self):
        OrderedDict.__init__(self)
        
    def __getattribute__(self, name):
        getter = super(MappedDictOrdered, self).__getattribute__
        try:
            return getter(name)
        except AttributeError as exp:
            if name in self: return self[name]
            else: raise exp
