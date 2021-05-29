from .Ast import NodeType
from .Expr import Expr

class BinOP(Expr):
    def __init__(self, left_term, right_term):
        self.left_term = left_term
        self.right_term = right_term

    def get_left_term(self):
        return self.left_term

    def get_right_term(self):
        return self.right_term

    def get_children(self):
        return [ (self.left_term, 'left operand'), (self.right_term, 'right_operand') ]

class OrExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.OR_EXPR
        super().__init__(left_term, right_term)    

    def __str__(self):
        return '||'

class AndExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.AND_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '&&'

class EqualExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.EQUAL_EXPR
        super().__init__(left_term, right_term)
    
    def __str__(self):
        return '=='

class DifferentExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.DIFFERENT_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '!='

class LessExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.LESS_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '<'

class LeqExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.LEQ_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '<='

class GreaterExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.GREATER_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '>'

class GeqExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.GEQ_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '>='

class PlusExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.PLUS_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '+'

class MinusExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.MINUS_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '-'

class MultExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.MULT_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '*'

class DivExpr(BinOP):
    def __init__(self, left_term, right_term):
        self.type = NodeType.DIV_EXPR
        super().__init__(left_term, right_term)

    def __str__(self):
        return '/'

class UnsupportedArgumentException(Exception):
    def __init__(self, arg, expected_list):
        self.message = 'Unexpected argument {}. Expected something from {}'.format(arg, expected_list)

def EqualityExprFactory(left_term, op, right_term):
    if op.value == '!=':
        return DifferentExpr(left_term, right_term)
    elif op.value == '==':
        return EqualExpr(left_term, right_term)
    else:
        raise UnsupportedArgumentException(op.value, ['==','!='])

def CompExprFactory(left_term, op, right_term):
    if op.value == '>=':
        return GeqExpr(left_term, right_term)
    elif op.value == '<=':
        return LeqExpr(left_term, right_term)
    elif op.value == '<':
        return LessExpr(left_term, right_term)
    elif op.value == '>':
        return GreaterExpr(left_term, right_term)
    else:
        raise UnsupportedArgumentException(op.value, ['<=','>=','>','<'])

def AdditiveExprFactory(left_term, op, right_term):
    if op.value == '+':
        return PlusExpr(left_term, right_term)
    elif op.value == '-':
        return MinusExpr(left_term, right_term)
    else:
        raise UnsupportedArgumentException(op.value, ['-','+'])

def TimesExprFactory(left_term, op, right_term):
    if op.value == '*':
        return MultExpr(left_term, right_term)
    elif op.value == '/':
        return DivExpr(left_term, right_term)
    else:
        raise UnsupportedArgumentException(op.value, ['/','*'])