import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS','MINUS','MULT','DIV',
    'LPAREN','RPAREN',
)

#tokens

t_MINUS = r'-'
t_PLUS = r'\+'
t_MULT = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

#ignored characters
t_ignore = " \t"    #space and tab

#lexing logic
#implicit definition of a token (t)

class token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.value = token_value
    def __repr__(self):
        return ("{} - {}".format(self.token_type, self.value))

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

def get_token_list(data):
    lexer = lex.lex()

    lexer.input(data)
    output_tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        converted_token = token(tok.type, tok.value)
        output_tokens.append( converted_token )

    print(output_tokens)
    return output_tokens
    
data = '1 + 23 * 4 + 2*(3+5)'
get_token_list(data)