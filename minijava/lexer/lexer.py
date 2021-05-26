import ply.lex as lex
import re

class token:
    def __init__(self, toktype, token_value):
        self.toktype = toktype
        self.value = token_value
    def __str__(self):
        return ("{} - {}".format(self.toktype, str(self.value)) )

class tokenStream:
    def __init__(self, lexer):

        self.pos = 0
        self.tokens = []

        tok = lexer.token()

        while tok:
            self.tokens.append(token(tok.type, tok.value))
            tok = lexer.token()

    def __str__(self):
        return '\n'.join([str(token) for token in self.tokens])

    def peep(self, lookahead):
        try:
            return self.tokens[self.pos + lookahead]
        except IndexError:
            return token("END","END")
    
    def consume(self):
        ans = self.tokens[self.pos]
        self.pos += 1
        return ans

tokens = (
    #statement blocks    
    'IF', 'ELSE',
    'WHILE', 'FOR',
    'PRINTLN',

    #bin ops
    'ASSIGN',
    'LESS', 'LESSOREQ',
    'GREATER', 'GREATEROREQ',
    'EQUAL', 'DIFFERENT',
    'PLUSEQUALS', 'MINUSEQUALS',
    'PLUS', 'MINUS',
    'MULT', 'DIV',
    'AND', 'OR',

    #unary ops
    'NEGATE',
    'UMINUS',

    #types and stuff
    'MAIN', 'CLASS',
    'THIS', 'NEW',
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
    'DOT',


    'END'
)

#tokens

reserved = {
    #statements
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
    'return' : 'RETURN',
    'int' : 'INTEGER',
    'String' : 'STRING',
    'boolean' : 'BOOLEAN',
    'length' : 'LENGTH',
    'true' : 'TRUE',
    'false' : 'FALSE',
}

#separators
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQPAREN = r'\['
t_RSQPAREN = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'

#binops
t_LESSOREQ = r'<='
t_LESS = r'<'
t_GREATEROREQ = r'>='
t_GREATER = r'>'
t_EQUAL = r'=='
t_DIFFERENT = r'!='
t_PLUSEQUALS = r'\+='
t_MINUSEQUALS = r'-='
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'  #redundante for unOp as well
t_MULT = r'\*'
t_DIV = r'/'
t_AND = r'&&'
t_OR = r'\|\|'

#unops
t_NEGATE = r'!'

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


with open("../samples/smallTest.java") as file:
    data='\n'.join(file.readlines())


print(getTokenStream(data))
