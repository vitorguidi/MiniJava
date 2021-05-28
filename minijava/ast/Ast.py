from enum import Enum

class Ast:
    def get_type(self):
        return self.var_type


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
    AND_EXPR = 12
    OR_EXPR = 13
    ARRAY_ACCESS_EXPR = 18
    EQUAL_EXPR = 19
    DIFFERENT_EXPR = 20
    LESS_EXPR = 21
    GREATER_EXPR = 22
    LEQ_EXPR = 23
    GEQ_EXPR = 24
    DIV_EXPR = 25
    MULT_EXPR = 26
    PLUS_EXPR = 27
    MINUS_EXPR = 28
    NOT_EXPR = 29
    INTEGER_LITERAL = 30
    INTEGER_ARRAY = 31
    TRUE = 32
    FALSE = 33
    ID = 34
    THIS = 35
    NULL = 36
    ARRAY_LENGTH = 37
    OBJECT_ACCESS = 38
    METHOD_CALL = 39
