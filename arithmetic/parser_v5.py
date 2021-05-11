from lexer import getTokenStream
from graphviz import Digraph

# simple grammar for expressions with +,-,*,/, ** and unary -

# start =   var assign expr | expr 

# expr =    expr OP1 term |
#           term

# term =    term OP2 factor |
#           factor

# factor = atom OP3 factor |
#          - factor |
#          atom

# atom =  lparen start_expr rparen |
#         variable |
#           number


# applying the same logic

# start_expr = start_term expr
# expr = OP1 start_term expr | eps

# start_term =  start_factor term
# term = OP2 start_factor term | eps

# factor = atom OP3 factor |
#          - factor        |
#          atom

# atom =  lparen start_expr rparen |

#         int

# 1*3*5 + 4

st = {}

class SyntaxError(Exception):
    ''' Raised when syntax rules are breached '''
    def __init__(self, message):
        self.message = message

class AST:

    def __init__(self, left, op, right):
        self.ops = {
           '**': lambda x,y : x**y,
           'UMINUS': lambda x : -x,
           '^': lambda x,y : x**y,
           '+': lambda x,y : x+y,
           '-': lambda x,y : x-y,
           '*': lambda x,y : x*y,
           '/': lambda x,y : x/y 
        }
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self):
        if self.op == 'VARIABLE':
            return st[self.left]
        if self.op == 'NUMBER':
            return self.left
        elif self.op == 'UMINUS':
            return -1 * self.left.evaluate()
        return self._apply_op(self.left.evaluate(), self.op, self.right.evaluate())

    def _apply_op(self, left, op, right):
        return self.ops[op](left, right)

class Parser:

    def __init__(self, tokenStream):
        self.tokenStream = tokenStream
        self.AST = self._parse()

    def _parse(self):
        return self._start()

    def _start(self):
        
        cur_token = self.tokenStream.get()

        if cur_token.toktype == 'VARIABLE':
            
            var, self.tokenStream = self.tokenStream.consume()
            
            cur_token = self.tokenStream.get()
            if cur_token.toktype != 'ASSIGN':
                raise SyntaxError('Expected ASSIGN, got {}'.format(cur_token.value))
            
            _, self.tokenStream = self.tokenStream.consume()
            ans = self._start_expr()
            st[var.value] = ans.evaluate()
            return ans

        return self._start_expr()
        

    def _start_expr(self):

        base_term = self._start_term()

        right = self._expr(base_term)

        return base_term if not right else right

    def _expr(self, prev_term):

        cur_token = self.tokenStream.get()

        if cur_token.toktype != 'OP1':
            return None

        op, self.tokenStream = self.tokenStream.consume()
        
        right_term = self._start_term()

        left_expr = AST(prev_term, op.value, right_term)

        # print('right number = ' + str(right_number.value))

        right_expr = self._expr(left_expr)

        if right_expr == None:
            return left_expr

        return right_expr

    def _start_term(self):
        base_factor = self._start_factor()

        right = self._term(base_factor)

        return base_factor if not right else right

    def _term(self, prev_term):
        cur_token = self.tokenStream.get()

        if cur_token.toktype != 'OP2':
            return None

        op, self.tokenStream = self.tokenStream.consume()

        local_right_term = self._start_factor()

        left_term = AST(prev_term, op.value, local_right_term)

        # print('right number = ' + str(right_number.value))

        right_term = self._term(left_term)

        if right_term == None:
            return left_term

        return right_term

    def _start_factor(self):
        cur_token = self.tokenStream.get()

        if cur_token.value == '-':
            _, self.tokenStream = self.tokenStream.consume()
            return AST(self._start_factor(), 'UMINUS', None)

        left_factor = self._start_atom()

        cur_token = self.tokenStream.get()

        if cur_token.toktype != 'OP3':
            return left_factor

        op, self.tokenStream = self.tokenStream.consume()

        local_right_factor = self._start_factor()

        left_term = AST(left_factor, op.value, local_right_factor)

        return left_term

    def _start_atom(self):
        cur_token = self.tokenStream.get()
        
        if cur_token.toktype == 'NUMBER':
            cur_token, self.tokenStream = self.tokenStream.consume()
            return AST(cur_token.value, 'NUMBER', None)

        elif cur_token.toktype == 'VARIABLE':
            cur_token, self.tokenStream = self.tokenStream.consume()
            return AST(st[cur_token.value], 'NUMBER', None)
        
        elif cur_token.toktype == 'LPAREN':
            _, self.tokenStream = self.tokenStream.consume()
            inner_expr = self._start_expr()
            cur_token = self.tokenStream.get()
            if cur_token.toktype != 'RPAREN':
                raise SyntaxError('Expected RPAREN, got {}'.format(cur_token.toktype))
            _, self.tokenStream = self.tokenStream.consume()
            return inner_expr

        else:
            raise SyntaxError('Expected NUMBER, got {}'.format(cur_token.toktype))

data = 'abatata = 1 - ( -2^(4-2^3 + 2*5) / -7^-3 )'
tokenStream = getTokenStream(data)
parser = Parser(tokenStream)
print(data)
print('result = ' + str(parser.AST.evaluate()))
print('abatata = ' + str(st['abatata']))

data2 = '3* abatata + 10'
print(data2)
tokenStream2 = getTokenStream(data2)
parser2 = Parser(tokenStream2)
print('3*abatata + 10 = ' + str(parser2.AST.evaluate()))

#dot = Digraph(comment='ast dump')

# ini = 0

# def dfs(ast):

#     global ini

#     if ast == None:
#         return

#     ini+= 1

#     local_num = str(ini)

#     if ast.op == 'NUMBER':
#         name = str(ast.left)
#     else:
#         name = ast.op
   
#     dot.node(name=str(ini), label=name)
   
#     if type(ast.left) == AST:
#         left_node = dfs(ast.left)
#         dot.edge(local_num, left_node)

#     if type(ast.right) == AST:
#         right_node = dfs(ast.right)
#         dot.edge(local_num, right_node)

#     return local_num

# dfs(parser.AST)

#dot.render('test-output/ast_dump.gv', view=True)        