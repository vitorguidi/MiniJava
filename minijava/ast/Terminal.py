from .Ast import *

class Terminal(Ast):
    pass

class Integer(Terminal):
    pass

class IntegerArray(Terminal):
    pass

class String(Terminal):
    pass

class Boolean(Terminal):
    pass

class Id(Terminal):
    pass

class NullNode(Terminal):
    pass