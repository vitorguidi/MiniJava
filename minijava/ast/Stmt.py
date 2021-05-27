from minijava.lexer.lexer import TokenTypes
from minijava.ast.Objects import ObjectTypes
from .Ast import *

class Stmt(Ast):
    pass

def StmtBlock(Stmt):
    def __init__(self, stmt_list):
        self.type = NodeType.STATEMENT_BLOCK
        self.stmt_list = stmt_list

class IfStmt(Stmt):
    def __init__(self, main_stmt, cond_expr, alt_stmt):
        self.main_stmt = main_stmt
        self.cond_expr = cond_expr
        self.alt_stmt = alt_stmt
        self.type = NodeType.IF_STATEMENT

class WhileStmt(Stmt):
    def __init__(self, cond_expr, stmt):
        self.cond_expr = cond_expr
        self.stmt = stmt
        self.type = NodeType.WHILE_STATEMENT

class AssignStmt(Stmt):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        self.type = NodeType.ASSIGN_STATEMENT

class ArrayAssigntStmt(Stmt):
    def __init__(self, id, pos_expr, value_expr):
        self.id = id
        self.pos_expr = pos_expr
        self.value_expr = value_expr
        self.type = NodeType.ARRAY_ASSIGN_STATEMENT

class PrintStmt(Stmt):
    def __init__(self, print_expr):
        self.print_expr = print_expr
        self.type = NodeType.PRINT_STATEMENT

class PlusEquals(Stmt):
    pass

class Minusequals(Stmt):
    pass

class NullStmt(Stmt):
    def __init__(self):
        self.type = NodeType.NULL_STATEMENT
