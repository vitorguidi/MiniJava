from .Ast import *

class Stmt(Ast):
    pass

class StmtBlock(Stmt):
    def __init__(self, stmt_list):
        self.type = NodeType.STATEMENT_BLOCK
        self.stmt_list = stmt_list
    
    def __str__(self):
        return 'stmt block'

    def get_children(self):
        edges = []
        cnt = 0
        for stmt in self.stmt_list:
            edges.append( (stmt, 'statement '.format(cnt)) )
            cnt += 1
        return edges

    def get_stmt_list(self):
        return self.stmt_list

class IfStmt(Stmt):
    def __init__(self, main_stmt, cond_expr, alt_stmt):
        self.main_stmt = main_stmt
        self.cond_expr = cond_expr
        self.alt_stmt = alt_stmt
        self.type = NodeType.IF_STATEMENT

    def __str__(self):
        return 'if'

    def get_children(self):
        return [ (self.main_stmt, 'main statement'), (self.alt_stmt, 'alt statement'), (self.cond_expr, 'conditional expression') ]

    def get_main_stmt(self):
        return self.main_stmt

    def get_alt_stmt(self):
        return self.alt_stmt

    def get_cond_expr(self):
        return self.cond_expr

class WhileStmt(Stmt):
    def __init__(self, cond_expr, stmt):
        self.cond_expr = cond_expr
        self.stmt = stmt
        self.type = NodeType.WHILE_STATEMENT

    def __str__(self):
        return 'while'

    def get_children(self):
        return [ (self.stmt, 'statement'), (self.cond_expr, 'conditional expression') ]

    def get_stmt(self):
        return self.stmt

    def get_cond_expr(self):
        return self.cond_expr

class AssignStmt(Stmt):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        self.type = NodeType.ASSIGN_STATEMENT

    def __str__(self):
        return 'assign to var {}'.format(self.id)

    def get_children(self):
        return [ (self.expr, 'expression') ]

class ArrayAssigntStmt(Stmt):
    def __init__(self, id, pos_expr, value_expr):
        self.id = id
        self.pos_expr = pos_expr
        self.value_expr = value_expr
        self.type = NodeType.ARRAY_ASSIGN_STATEMENT

    def __str__(self):
        return 'assign to array {}'.format(self.id)

    def get_children(self):
        return [ (self.pos_expr, 'position expression'), (self.value_expr, 'value expression') ]

class PrintStmt(Stmt):
    def __init__(self, print_expr):
        self.print_expr = print_expr
        self.type = NodeType.PRINT_STATEMENT

    def __str__(self):
        return 'print'

    def get_children(self):
        return [ (self.print_expr, 'expression to print') ]

class ReturnStmt(Stmt):
    def __init__(self, return_exp):
        self.return_expr = return_exp
        self.type = NodeType.RETURN_STMT

    def __str__(self):
        return 'return'

    def get_children(self):
        return [(self.return_expr, 'return expr')]

class NullStmt(Stmt):
    def __init__(self):
        self.type = NodeType.NULL_STATEMENT

    def __str__(self):
        return 'NULL'

    def get_children(self):
        return []