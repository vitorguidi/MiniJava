from .Ast import *

class Expr(Ast):
    def __init__(self):
        pass

    def get_type(self):
        return self.type

class UnOp(Expr):
    def __init__(self):
        pass

    def get_arg(self):
        return self.arg

    def _get_children(self):
        return [ (self.arg, 'unary operand') ]

class NotExpr(UnOp):
    def __init__(self, arg):
        self.arg = arg
        self.type = NodeType.NOT_EXPR

    def __str__(self):
        return '!'

    def get_children(self):
        return [(self.arg, 'negated argument')]

class ArrayAccessExpr(Expr):
    def __init__(self, id, pos_expr):
        self.id = id
        self.pos_expr = pos_expr
        self.type = NodeType.ARRAY_ACCESS_EXPR

    def get_array_id(self):
        return self.id

    def get_pos_expr(self):
        return self.pos_expr

    def __str__(self):
        return 'ArrayAccess'

    def get_children(self):
        return [ (self.id, 'array id'), (self.pos_expr, 'position expr') ]

class MethodCallExpr(Expr):
    def __init__(self, object_id, method_id, expr_list):
        self.object_id = object_id
        self.method_id = method_id
        self.expr_list = expr_list

    def __str__(self):
        return 'method call'

    def get_children(self):
        edges = [ (self.object_id, 'object id'), (self.method_id, 'method id') ]
        cnt = 0
        for item in self.expr_list:
            edges.push_back( (item, 'argument {}'.format(cnt)) )
            cnt += 1
        return edges
        

class ObjectAccessExpr(Expr):
    def __init__(self, object_id, variable_id):
        self.object_id = object_id
        self.variable_id = variable_id
        self.type = NodeType.OBJECT_ACCESS

    def __str__(self):
        return 'object access'

    def get_children(self):
        return [ (self.object_id, 'object id'), (self.variable_id, 'inner variable id') ]

class ArrayLengthExpr(Expr):
    def __init__(self, id):
        self.id = id
        self.type = NodeType.ARRAY_LENGTH

    def __str__(self):
        return 'array length'

    def get_children(self):
        return [(self.id, 'array id')]

class NewIntArrayExpr(Expr):
    def __init__(self, size_expr):
        self.size_expr = size_expr

    def __str__(self):
        return 'new array'

    def get_children(self):
        return [(self.size_expr, 'size expression')]

class NewObjectExpr(Expr):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'new object'

    def get_children(self):
        return [(self.id, 'object id')]