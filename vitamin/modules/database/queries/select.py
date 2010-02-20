from .query import Query
from vitamin.modules.database.expression import Expression
from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder.definitions import Names
      
class QuerySelect(Query):
    
    def __init__(self, model):
        Query.__init__(self, model)
        self._fields = None
        self._where = None
        self.single_element = False
        
    @Query.chain
    def fields(self, *fields):
        self._fields = fields
    
    @Query.chain
    def where(self, expr):
        assert isinstance(expr, Expression)
        self._where = expr
    
    @Query.chain
    def single(self):
        self.single_element = True
        
    def go(self):
        cursor = Query.go(self)
        cursor_adapt = CursorAdaptor(self.model, self._fields)
        result = cursor_adapt(cursor)
        if not self.single_element:
            return result
        else:
            lst = list(result)
            return lst[0] if len(lst) else None
        
    def sql(self):
        table = self.model.Name
        context = Context(namespace=Names.Select)
        context.varSelectTable = table
        if self._where:
            context.varWhereExpr = str(self._where)

        if self._fields:
            names = [f.name for f in self._fields]
            for name in names:
                c = Context(namespace=Names.Select.ColumnsLevel)
                c.varTableName = table
                c.varColumnName = name
                context.level(c)

        return self.builder.build(context)
    
class CursorAdaptor():
    
    def __init__(self, model, *fields):
        self.model = model
        self.fields = fields
        
    def __call__(self, cursor):
        assert cursor
        assert cursor.description, "No querry"
        names = list(x[0] for x in cursor.description)
        for row in cursor:
            print("feched row: ", row)
            instance = self.model()
            for name, value in dict(zip(names, row)).items():
                setattr(instance, name, value)
            yield instance
                
