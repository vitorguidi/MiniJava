from ast import NodeTransformer
from . import ast
from minijava.ast.Ast import *

class expr(ast):
    def __init__(self):
        pass

    def get_type(self):
        return self.type

class UnOp(expr):
    def __init__(self):
        pass

    def get_arg(self):
        return self.arg

def NotExpr(UnOp):
    def __init__(self, arg):
        self.arg = arg
        self.type = NodeType.NOT_EXPR

class ArrayAccessExpr(expr):
    def __init__(self, id, pos_expr):
        self.id = id
        self.pos_expr = pos_expr
        self.type = NodeType.ARRAY_ACCESS_EXPR

    def get_array_id(self):
        return self.id

    def get_pos_expr(self):
        return self.pos_expr

class MethodCallExpr(expr):
    def __init__(self, object_id, method_id, expr_list):
        self.object_id = object_id
        self.method_id = method_id
        self.expr_list = expr_list

class ObjectAccessExpr(expr):
    def __init__(self, object_id, variable_id):
        self.object_id = object_id
        self.variable_id = variable_id
        self.type = NodeType.OBJECT_ACCESS

class ArrayLengthExpr(expr):
    def __init__(self, id):
        self.id = id
        self.type = NodeType.ARRAY_LENGTH

class NewIntArrayExpr(expr):
    def __init__(self, size_expr):
        self.size_expr = size_expr

class NewObjectExpr(expr):
    def __init__(self, id):
        self.id = id