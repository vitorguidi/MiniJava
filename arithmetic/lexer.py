import ply.lex as lex

class token:
    def __init__(self, toktype, token_value):
        self.toktype = toktype
        self.value = token_value
    def __str__(self):
        return ("{} - {}".format(self.toktype, self.value))

class tokenStream:
    def __init__(self, lexer, prev=None):

        tok = lexer.token()        
        
        if not tok:
            self.token = token("END", "END")
            self.nxt = None
            return

        self.token = token(tok.type, tok.value)
        self.nxt = tokenStream(lexer, self)

    def __str__(self):
        return str(self.token) + ', ' + str(self.nxt)

    def get(self):
        return self.token
    
    def lookAhead(self):
        return self.nxt.token
    
    def consume(self):
        return self.token, self.nxt

tokens = (
    'NUMBER',
    'OP3',
    'OP2',
    'OP1',
    'LPAREN','RPAREN',
    'END'
)

#tokens

t_OP1 = r'-|\+'
t_OP2 = r'\*|/'
t_OP3 = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'

#ignored characters
t_ignore = " \t"    #space and tab

#lexing logic
#implicit definition of a token (t)

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
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

# data = '1 + 23 * 4 + 2^(3*5 + 2)'
# #print( getTokenStream(data) )

# aux = (getTokenStream(data))
# while aux != None:
#     print(aux.token)
#     _, aux = aux.consume()