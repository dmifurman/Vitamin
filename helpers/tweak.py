from helpers.lazyimport import smartimport
from helpers.dictmapper import MappedDict
from collections import UserList

class Null:
    pass

config = None
LAZY_IMPORT_PREFIX = "lazy://"

def prepare(module):
    global config
    config = module

#===============================================================================
# Exceptions
#===============================================================================
class ConfigNoSection(Exception):
    
    def __init__(self, section):
        self.msg = "No section '{0}' in config module".format(section)
        
    def __str__(self):
        return self.msg  
        
class ConfigNoParameter(Exception):
    
    def __init__(self, section, parameter):
        self.msg = "Missed required configuration parameter '{1}' in section '{0}'".format(
            section, parameter)
    
    def __str__(self):
        return self.msg
#===============================================================================
#===============================================================================
class LazyList(UserList):
    
    def __init__(self, lst=[]):
        UserList.__init__(self, lst)
        
    def __getitem__(self, index):
        item = self.data[index]
        if isinstance(item, str) and item.startswith(LAZY_IMPORT_PREFIX):
            self.data[index] = smartimport(item[len(LAZY_IMPORT_PREFIX):])
            return self.data[index]
        else: return item
        
    def __contains__(self, obj):
        for x in self: pass #import all
        return obj in self.data

class Section(MappedDict):
    
    def __init__(self, _dict):
        MappedDict.__init__(self)
        self.update(_dict)
            
    def __getitem__(self, key):
        if key in self.keys():
            item = self.data[key]
            if isinstance(item, str) and item.startswith(LAZY_IMPORT_PREFIX):
                self.data[key] = smartimport(item[len(LAZY_IMPORT_PREFIX):])
                return self.data[key]
            else: return item
        else: raise KeyError(key)
        
    def reconfigure(self, name, value):
        for item in self.keys():
            if item.upper() == name.upper(): 
                self[item] = value
                return True
        return False

        
class Parameter():
    
    def __init__(self, default=Null(), section=None):
        self.name = None
        self.default = default
        self.section = section     

def Tweak(strObj):
    return type("TweakClass" + strObj, (_Tweak,), {"section": strObj, "config": config})

class _Tweak():

    def __init__(self):
        
        self.configParams = []
        self.configSection = self.section
        
    def load_section_get_dict(self, config, section):
        
        if not section in self.dirConf: 
            raise ConfigNoSection(self.configSection);   
        sectionDict = getattr(config, section);
        assert type(sectionDict) is Section
        return sectionDict
    
    def tweak(self):
        
        _Tweak.__init__(self)
        self.dirConf = dir(config)
        assert self.configSection     
        
        sectionDict = self.load_section_get_dict(config, self.configSection)
        
        for i in dir(self):
            value = getattr(self, i)
            if isinstance(value, Parameter):
                value.name = i
                section = sectionDict
                if value.section:                    
                    anotherSection = self.load_section_get_dict(config, value.section)
                    section = anotherSection                    
                if value.name in section:
                    setattr(self, value.name, section[value.name])
                else:
                    if isinstance(value.default, Null):
                        raise ConfigNoParameter(section, value.name)
                    else:
                        setattr(self, value.name, value.default)
            




