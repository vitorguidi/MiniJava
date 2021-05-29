from enum import Enum

class Ast:
    def get_type(self):
        return self.var_type

    def get_children(self):
        pass

class NodeType(Enum):
    PROGRAM = 0
    CLASS = 1
    MAINCLASS = 2
    METHOD = 3
    VARIABLE = 4
    IF_STATEMENT = 5
    WHILE_STATEMENT = 6
    PRINT_STATEMENT = 7
    ASSIGN_STATEMENT = 8
    ARRAY_ASSIGN_STATEMENT = 9
    NULL_STATEMENT = 10
    STATEMENT_BLOCK = 11
    
    ARRAY_ACCESS_EXPR = 12

    AND_EXPR = 13
    OR_EXPR = 14 
    EQUAL_EXPR = 15
    DIFFERENT_EXPR = 16
    LESS_EXPR = 17
    GREATER_EXPR = 18
    LEQ_EXPR = 19
    GEQ_EXPR = 20
    DIV_EXPR = 21
    MULT_EXPR = 22
    PLUS_EXPR = 23
    MINUS_EXPR = 24
    NOT_EXPR = 25
    
    INTEGER_LITERAL = 26
    INTEGER_ARRAY = 27
    TRUE = 28
    FALSE = 29
    ID = 30
    THIS = 31
    NULL = 32

    ARRAY_LENGTH = 33
    OBJECT_ACCESS = 34
    METHOD_CALL = 35