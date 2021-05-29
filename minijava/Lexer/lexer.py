from typing import Tuple
import ply.lex as lex
from enum import Enum

class TokenTypes(Enum):
   
    #statements and ops
    IF = 'IF',
    ELSE = 'ELSE',
    WHILE = 'WHILE',
    FOR = 'FOR',
    PLUSEQUALS = 'PLUSEQUALS',
    MINUSEQUALS = 'MINUSEQUALS',
    PRINTLN = 'PRINTLN',
    ASSIGN = 'ASSIGN',
    OP1 = 'OP1',   # * /
    OP2 = 'OP2',   # + -
    OP3 = 'OP3',   # > >= < <= 
    OP4 = 'OP4',    # == !=
    NOT = 'NOT',
    AND = 'AND',
    OR = 'OR',

    #types and stuff
    MAIN ='MAIN',
    CLASS = 'CLASS',
    THIS = 'THIS',
    NEW = 'NEW',
    EXTENDS = 'EXTENDS',
    INTEGER = 'INTEGER',
    BOOLEAN = 'BOOLEAN',
    STRING = 'STRING',
    PUBLIC = 'PUBLIC',
    STATIC = 'STATIC',
    VOID = 'VOID',
    RETURN = 'RETURN',
    LENGTH = 'LENGTH',

    #literals
    INTEGER_LITERAL = 'INTEGER_LITERAL',
    STRING_LITERAL = 'STRING_LITERAL',
    TRUE ='TRUE',
    FALSE = 'FALSE',
    ID = 'ID',

    #separators
    LPAREN = 'LPAREN',
    RPAREN = 'RPAREN',
    LSQPAREN = 'LSQPAREN',
    RSQPAREN = 'RSQPAREN',
    LBRACE = 'LBRACE',
    RBRACE = 'RBRACE',
    SEMICOLON = 'SEMICOLON',
    COMMA = 'COMMA',
    DOT = 'DOT'

class Token:
    def __init__(self, toktype, token_value):
        for item in TokenTypes:       
            if item.value[0] == toktype or item.value == toktype:
                self.type = item
        self.value = token_value
    def __str__(self):
        return ("{} - {}".format(self.type, str(self.value)) )

class tokenStream:
    def __init__(self, lexer):

        self.pos = 0
        self.tokens = []

        tok = lexer.token()

        while tok:
            self.tokens.append(Token(tok.type, tok.value))
            tok = lexer.token()

    def __str__(self):
        return '\n'.join([str(token) for token in self.tokens])

    def peep(self, lookahead):
        try:
            return self.tokens[self.pos + lookahead].type
        except IndexError:
            return None
    
    def consume(self):
        try:
            ans = self.tokens[self.pos]
            self.pos += 1
            #print(self.tokens[self.pos-1])
        except IndexError:
            return None
        return ans

tokens = (

    #statement blocks    
    'IF', 'ELSE',
    'WHILE', 'FOR',
    'PLUSEQUALS', 'MINUSEQUALS',
    'PRINTLN',
    'ASSIGN',

    #ops
    #all left associative
    'OP1',   # * /
    'OP2',   # + -
    'OP3',   # > >= < <= 
    'OP4',   # == !=
    'NOT',
    'AND',
    'OR',

    #types and stuff
    'MAIN', 'CLASS',
    'THIS', 'NEW', 'EXTENDS',
    'INTEGER', 'BOOLEAN', 'STRING',
    'PUBLIC', 'STATIC', 'VOID',
    'RETURN',
    'LENGTH',

    #literals
    'INTEGER_LITERAL', 'STRING_LITERAL',
    'TRUE', 'FALSE',
    'ID',

    #separators
    'LPAREN', 'RPAREN',
    'LSQPAREN', 'RSQPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA',
    'DOT'

)

#tokens

reserved = {
    'for' : 'FOR',
    'while' : 'WHILE',
    'if' : 'IF',
    'else' : 'ELSE',
    'main' : 'MAIN',
    'class' : 'CLASS',
    'public' : 'PUBLIC',
    'static' : 'STATIC',
    'void' : 'VOID',
    'this' : 'THIS',
    'new' : 'NEW',
    'extends' : 'EXTENDS',
    'return' : 'RETURN',
    'int' : 'INTEGER',
    'String' : 'STRING',
    'boolean' : 'BOOLEAN',
    'length' : 'LENGTH',
    'true' : 'TRUE',
    'false' : 'FALSE',
}

#separators
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQPAREN = r'\['
t_RSQPAREN = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','

#binops
t_OP1 = r'\*|/'
t_OP2 = r'\+|-'
t_OP3 = r'<=|<|>=|>'
t_OP4 = r'==|!='
t_NOT = r'!'
t_AND = r'&&'
t_OR = r'\|\|'

#stmts
t_PLUSEQUALS = r'\+='
t_MINUSEQUALS = r'-='
t_ASSIGN = r'='

#ignored characters
t_ignore = "\t "    #space and tab

def t_PRINTLN(t):
    r'System\.out\.println'
    return t

def t_INTEGER_LITERAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRING_LITERAL(t):
    r'\".*\"'
    t.value = t.value.replace("\"", "")
    return t

def t_ID(t):
    r'[a-zA-Z_][_a-zA-Z\d]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def getTokenStream(data):
    lexer = lex.lex()
    lexer.input(data)
    return tokenStream(lexer)