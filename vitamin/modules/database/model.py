from collections import OrderedDict
from vitamin.modules.database.fields import Field, IntegerField, ForeignField
from vitamin.modules.database.queries import QuerySelect, QueryInsert, \
    QueryCreate, QueryUpdate, QueryDelete
from helpers.property import SingletonProperty
from vitamin.modules.database.features import primary, autoinc
    
class Makeup(type):

    @classmethod
    def __prepare__(metacls, name, bases):
        return OrderedDict()
    
    def __new__(cls, name, bases, classdict):
        
        have_primary = False
        fields = OrderedDict()
        _primary = None
        for n, value in classdict.items():
            if isinstance(value, Field): 
                value.expressionBehaviour()  
                value.Name = n.lower() 
                fields[n] = value
                if primary.check(value):
                    have_primary = True
                    _primary = value
                elif n == "id":
                    raise ValueError("id must be primary!")

        if not have_primary:
            IdField = IntegerField(primary, autoinc)
            IdField.expressionBehaviour()
            classdict["id"] = IdField
            fields = OrderedDict([('id', IdField)] + list(fields.items()))
            _primary = IdField
        result = type.__new__(cls, name, bases, classdict)
        result._primary = _primary
        for f in fields.values():
            f.Model = result  
        
        result._fields = fields 
        result._own_type = result
        result.Name = SingletonProperty(name.lower())
        return result
    
    def __iter__(self):
        return iter(self._fields.values())
    

            
class Model(metaclass=Makeup):
        
    #|var Name
    #|var Fields
    #|    goes from metaclass
    
    #Запросы к базе данных
    
    @classmethod
    def __getitem__(cls, key):
        return cls._fields[key]

    @classmethod
    def Select(cls):
        return QuerySelect(cls)
    
    @classmethod
    def Insert(cls):
        return QueryInsert(cls)
    
    @classmethod
    def Delete(cls): 
        return QueryDelete(cls)
    
    @classmethod
    def Update(cls):
        return QueryUpdate(cls)
    
    @classmethod
    def Create(cls):
        return QueryCreate(cls)
    
    #Производные запросы к базе данных
    
    def Append(self):
        return self.Insert().instance(self).go()
    
    def Save(self):
        return self.Update().instance(self).go()
    
    def Foreign(self, field):
        assert isinstance(field, ForeignField)
        assert field.ForeignModel == self.__class__
        return field.Model.Select().where(field == self.value(self.PrimaryKey())).go()  
    
    #---------------------------
    
    
    @classmethod
    def keys(cls):
        return list(cls._fields.keys())   
        
    @classmethod
    def PrimaryKey(cls):
        return cls._primary
    
    PDO = SingletonProperty(None)
           
    def __iter__(self):
        return self._fields.__iter__()
    
    #Items
    def __items(self, base=False):
        return tuple(zip(self.keys(), self.__values(base)))  
    
    def items(self):
        return self.__items(False)
    
    def storage_items(self):
        return self.__items(True)
    
    def __values(self, base=False):
        if not base:
            return [self.value(x) for x in self._fields.values()]
        else:
            return [x.NativeToStorage(self.value(x)) for x in self._fields.values()]
        
    def values(self):
        return self.__values(False)
    
    def storage_values(self):
        return self.__values(True)
    
    def value(self, field):
        return field.__get__(self, None)  
    
    def storage_value(self, field):
        return field.NativeToStorage(self.value(field))    

    

 
