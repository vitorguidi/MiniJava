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
  
