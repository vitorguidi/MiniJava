from .Ast import *

class Terminal(Ast):
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

    def get_children(self):
        return []

class IntegerLiteralNode(Terminal):
    def __init__(self, value):
        super().__init__(value)
        self.type = NodeType.INTEGER_LITERAL

    def __str__(self):
        return 'Integer - {}'.format(self.get_value())

class TrueNode(Terminal):
    def __init__(self):
        super().__init__(True)
        self.type = NodeType.TRUE

    def __str__(self):
        return 'True'

class FalseNode(Terminal):
    def __init__(self):
        super().__init__(False)
        self.type = NodeType.FALSE
    
    def __str__(self):
        return 'False'

class IdNode(Terminal):
    def __init__(self, value):
        super().__init__(value)
        self.type = NodeType.ID

    def __str__(self):
        return 'ID - {}'.format(self.get_value())

class ThisNode(Terminal):
    def __init__(self):
        super().__init__('this')
        self.type = NodeType.THIS

    def __str__(self):
        return 'This'

class NullNode(Terminal):
    def __init__(self):
        super().__init__(None)
        self.type = NodeType.NULL

    def __str__(self):
        return 'NULL'