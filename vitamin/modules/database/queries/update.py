from .query import Query
from vitamin.modules.database.expression import Expression
from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder.definitions import Names
class QueryUpdate(Query): 
    
    def __init__(self, model):
        Query.__init__(self, model)
        self._fields = []
        self._where = None
        self.only_fields = []
    
    @Query.chain
    def where(self, expr):
        assert isinstance(expr, Expression)
        self._where = expr
    
    @Query.chain
    def field(self, field, expr):
        assert isinstance(expr, str)
        self._fields.append((field, expr))
        
    @Query.chain
    def fields(self, *fields):
        self.only_fields = fields        
    
    @Query.chain
    def instance(self, *model_inst):
        self._instances = model_inst
        
    def sql(self):
        
        context = Context(namespace=Names.Update)
        context.varTableName = self.model.Name
        
        def gene():
            nonlocal context
            assert len(self._fields)
             
            if self._where:
                context.varWhereExpr = str(self._where)

            for field, expr in self._fields:
                c = Context(namespace=Names.Update.ColumnsLevel)
                c.varColumnName = field.Name
                c.varColumnUpdateExpr = expr
                context.level(c)

            return self.builder.build(context)
        
        if self._instances: 
            for model_inst in self._instances:
                if not self.only_fields:
                    self._fields = list(zip(self.model, model_inst.storage_values()))
                else:
                    self._fields = [(x, model_inst.storage_value(x)) for x in self.only_fields]
                value = model_inst.value(self.model.PrimaryKey())
                assert value != None, "Не указано значение первичного ключа для обновления!"
                self._where = self.model.PrimaryKey() == value
                yield gene()
        else:
            yield gene()
