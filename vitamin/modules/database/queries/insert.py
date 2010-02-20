from .query import Query
from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder.definitions import Names
class QueryInsert(Query):
    
    def __init__(self, model):
        Query.__init__(self, model)
        self.models = None
    
    @Query.chain
    def instance(self, *models):
        self.models = models
        
    def sql(self):
        
        context = Context(namespace=Names.Insert)
        context.varTableName = self.model.Name
        
        for instance in self.models:

            for name, value in instance.storage_items():
                c = Context(namespace=Names.Insert.ValuesLevel)
                c.varValue = value
                field = instance[name]                      
                for feature in field.features:
                    feature.insertHook(self, instance, field , c)
                context.level(c)

            yield self.builder.build(context)
