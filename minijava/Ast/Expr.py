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

def NotExpr(UnOp):
    def __init__(self, arg):
        self.arg = arg
        self.type = NodeType.NOT_EXPR

class ArrayAccessExpr(Expr):
    def __init__(self, id, pos_expr):
        self.id = id
        self.pos_expr = pos_expr
        self.type = NodeType.ARRAY_ACCESS_EXPR

    def get_array_id(self):
        return self.id

    def get_pos_expr(self):
        return self.pos_expr

class MethodCallExpr(Expr):
    def __init__(self, object_id, method_id, expr_list):
        self.object_id = object_id
        self.method_id = method_id
        self.expr_list = expr_list

class ObjectAccessExpr(Expr):
    def __init__(self, object_id, variable_id):
        self.object_id = object_id
        self.variable_id = variable_id
        self.type = NodeType.OBJECT_ACCESS

class ArrayLengthExpr(Expr):
    def __init__(self, id):
        self.id = id
        self.type = NodeType.ARRAY_LENGTH

class NewIntArrayExpr(Expr):
    def __init__(self, size_expr):
        self.size_expr = size_expr

class NewObjectExpr(Expr):
    def __init__(self, id):
        self.id = id