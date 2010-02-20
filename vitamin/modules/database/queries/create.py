from .query import Query
from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder.definitions import Names

class QueryCreate(Query):
        
    def __init__(self, model):
        Query.__init__(self, model)
        
    def go(self):
        return bool(Query.go(self))
        
    def field(self, model, field):
        
        c = Context(namespace=Names.Create.ColumnsLevel)
        c.varColumnName = field.Name
        c.varColumnType = field.StorageType
        
        for feature in field.features:
            feature.createHook(self, field, c)  
                
        return c   
        
    def sql(self):        
        context = Context(namespace=Names.Create)
        context.varTableName = self.model.Name
        for field in self.model:
            context.level(self.field(self.model, field))            
        return self.builder.build(context)
