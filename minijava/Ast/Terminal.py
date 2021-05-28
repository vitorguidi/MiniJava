from .Ast import *

class Terminal(Ast):
    def __init__(self, value):
        pass
    
    def get_value(self):
        return self.value

class IntegerLiteralNode(Terminal):
    def __init__(self, value):
        super().__init__(value)
        self.type = NodeType.INTEGER_LITERAL

class TrueNode(Terminal):
    def __init__(self):
        super().__init__(True)
        self.type = NodeType.TRUE

class FalseNode(Terminal):
    def __init__(self):
        super().__init__(False)
        self.type = NodeType.FALSE

class IdNode(Terminal):
    def __init__(self, value):
        super().__init__(value)
        self.type = NodeType.ID

class ThisNode(Terminal):
    def __init__(self):
        super().__init__('this')
        self.type = NodeType.THIS

class NullNode(Terminal):
    def __init__(self):
        super().__init__(None)
        self.type = NodeType.NULL