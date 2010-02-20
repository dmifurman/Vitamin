from .query import Query
from vitamin.modules.database.expression import Expression
from vitamin.modules.database.sqlbuilder.definitions import Names
from vitamin.modules.database.sqlbuilder.constructor import Context
class QueryDelete(Query):
    
    def __init__(self, model):
        Query.__init__(self, model)
        self._where = ""

    @Query.chain
    def where(self, expr):
        assert isinstance(expr, Expression)
        self._where = expr
    
    @Query.chain  
    def instance(self, inst):
        self.where(inst.primaryKey() == inst.storage_value(inst.primaryKey()))
        
    def sql(self):
        context = Context(namespace=Names.Delete)
        assert self._where
        context.varTableName = self.model.Name
        context.varWhereExpr = str(self._where)
        return self.builder.build(context)
