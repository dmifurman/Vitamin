from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder.definitions import Names

#|Базовые выражения, на основе 
#|котоых будут строиться все остальные

def isfield(obj):
    return hasattr(obj, "NativeToStorage")

def convert(expr1, expr2):
    res1, res2 = None, None
    if isinstance(expr1, Expression) and isinstance(expr2, Expression):
        res1 = str(expr1)
        res2 = str(expr1)
    else:
        if isfield(expr1) and not isfield(expr2):
            res1 = str(expr1)
            res2 = expr1.NativeToStorage(expr2)
        elif isfield(expr2) and not isfield(expr1):
            res2 = str(expr2)
            res1 = expr2.NativeToStorage(expr1)
    if res1 != None and res2 != None:
        return res1, res2
    else:
        raise ValueError("Can not convert binary expressions!")

class Expression():

    def __init__(self, function):
        self.function = function
        
    def __call__(self, *args, **kwargs):
        e = Expression(self.function)
        e._args = args
        e._kwargs = kwargs
        return e
    
    def __str__(self):
        context = self.function(*self._args, **self._kwargs)
        return self.builder.build(context)
    
    def __and__(self, right):
        if right:
            return __and__(self, right)
        else:
            return self
    
    def __or__(self, right):
        if right:
            return __or__(self, right)
        else:
            return self
    
    def _get_builder(self):
        return self._constructor    
    def _set_builder(self, constr):
        self._construction = constr        
    builder = property(_get_builder, _set_builder)

@Expression
def un(unaryOp, expr):
    c = Context()
    c[Names.Expression.UnaryOperator.varUnaryOperator] = unaryOp
    c[Names.Expression.UnaryOperator.varUnaryExpression] = expr
    return c

@Expression
def bin(leftExpr, binaryOp, rightExpr):
    c = Context(namespace=Names.Expression.BinaryOperator)
    res1, res2 = convert(leftExpr, rightExpr)
    c.varBinaryLeft = str(res1)
    c.varBinaryRight = str(res2)
    c.varBinaryOperator = binaryOp
    return c

@Expression
def like(leftExpr, rightExpr, reverse=False, match=False):
    c = Context(namespace=Names.Expression.Like)
    c.varLikeLeft = str(leftExpr)
    c.varLikeRight = str(rightExpr)
    if reverse:
        c.flagReverse = True
    if not match:
        c.flagLike = True
    else:
        c.flagMatch = True
    return c

@Expression
def isnull(expr, reverse=False):
    c = Context()
    c[Names.Null.varNullValue] = str(expr)
    if not reverse:
        c[Names.Null.flagIsNull] = True
    else:
        c[Names.Null.flagNotNull] = False
        
def notnull(expr):
    return isnull(expr, reverse=True)

@Expression
def isop(leftExpr, rightExpr, reverse=False):
    c = Context()
    c[Names.Is.varIsLeft] = str(leftExpr)
    c[Names.Is.varIsRight] = str(rightExpr)
    if reverse:
        c[Names.Is.flagReverse] = True

def isnot(leftExpr, rightExpr):
    return isop(leftExpr, rightExpr, reverse=True)

@Expression
def between(btwVal, btwLeft, btwRight, reversed=False):
    c = Context()
    c[Names.Between.varBetweenValue] = str(btwVal)
    c[Names.Between.varBetweenLeft] = str(btwLeft)
    c[Names.Between.varBetweenRight] = str(btwRight)
    if reversed:
        c[Names.Between.varBetweenReversed] = True
    return c

def betweenr(btwVal, btwLeft, btwRight):
    return between(btwVal, btwLeft, btwRight, reversed=True)

def __eq__(left, right): 
    return bin(left, "=", right)
def __ne__(left, right):
    return bin(left, "!=", right)
def __lt__(left, right):
    return bin(left, "<", right)
def __le__(left, right):
    return bin(left, "<=", right)
def __gt__(left, right):
    return bin(left, ">", right)
def __ge__(left, right):
    return bin(left, ">=", right)
def __and__(left, right):
    return bin(left, "AND", right)
def __or__(left, right):
    return bin(left, "OR", right)
def __pos__(expr):
    return un("+", expr)  
def __neg__(expr):
    return un("-", expr)
def __in__(left, right):
    return bin(left, "IN", right)
        
