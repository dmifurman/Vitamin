from vitamin.modules.database.sqlbuilder.definitions import Names

class Feature(object):

    def __new__(cls, field):
        field.features.append(cls)        
        return field      
    
    @classmethod
    def createHook(cls, query, field, c):
        pass
    
    @classmethod
    def insertHook(cls, query, instance, field, c):
        pass
    
    @classmethod
    def _get_name(cls):
        return cls.__name__
    
    @classmethod
    def check(cls, field):
        return cls in field.features
    
    name = property(_get_name)

def set(context, name, value):
    context[name] = value

class primary(Feature):  
      
    @classmethod
    def createHook(cls, query, field, c):
        c.flagPrimary = True
        
class autoinc(Feature):
        
    @classmethod
    def createHook(cls, query, field, c):
        c.flagAutoinc = True
        
    @classmethod
    def insertHook(cls, query, instance, field, c):
        c.varValue = "NULL"
        
class notnull(Feature):    
    @classmethod
    def createHook(cls, query, field, c):
        c.flagNotNull = True
        
    @classmethod
    def insertHook(cls, query, instance, field, c):
        if instance.value(field) == field.default:
            raise Exception("NOT NULL value must be assigned!")
   
class unique(Feature):    
    @classmethod
    def createHook(cls, query, field, c):
        c.flagUnique = True

def length(length):
    class Length(Feature):        
        @classmethod
        def createHook(cls, query, field, c):
            c.varColumnSize = str(length)
    return Length

def default(value):
    class Default(Feature):  
        
        @classmethod
        def createHook(cls, query, field, c):
            c.varColumnDefaultValue = field.NativeType(value)
              
        @classmethod
        def insertHook(cls, query, instance, field, c):
            if (c.varValue == field.NativeToStorage(field.default)):
                c.varValue = field.NativeToStorage(value)
                
    return Default

class null(Feature):        
    @classmethod
    def insertHook(cls, query, instance, field, c):
        if instance.value(field) == field.default:
            c.varValue = "NULL"
