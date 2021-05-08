from lexer import getTokenStream
from graphviz import Digraph

# simple grammar for expressions with +,-,*,/

# expr =    expr OP1 term |
#           term

# term =    term OP2 factor |
#           factor

# factor =  lparen start_expr rparen |final

# applying the same logic

# start_expr = start_term expr
# expr = OP1 start_term expr | eps

# start_term = final term
# term = OP2 final term | eps

# final = number

# 1*3*5 + 4

class SyntaxError(Exception):
    ''' Raised when syntax rules are breached '''
    def __init__(self, message):
        self.message = message

class AST:

    def __init__(self, left, op, right):
        self.ops = {
           '+': lambda x,y : x+y,
           '-': lambda x,y : x-y,
           '*': lambda x,y : x*y,
           '/': lambda x,y : x/y 
        }
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self):
        if self.op == 'NUMBER':
            return self.left
        return self._apply_op(self.left.evaluate(), self.op, self.right.evaluate())

    def _apply_op(self, left, op, right):
        return self.ops[op](left, right)

class Parser:

    def __init__(self, tokenStream):
        self.tokenStream = tokenStream
        self.AST = self._parse()

    def _parse(self):
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
        base_final = self._final()

        right = self._term(base_final)

        return base_final if not right else right

    def _term(self, prev_term):
        cur_token = self.tokenStream.get()

        if cur_token.toktype != 'OP2':
            return None

        op, self.tokenStream = self.tokenStream.consume()

        cur_token = self.tokenStream.get()

        if cur_token.toktype != 'NUMBER':
            raise SyntaxError('Expected NUMBER, got {}'.format(cur_token.toktype))

        local_right_term = self._final()

        left_term = AST(prev_term, op.value, local_right_term)

        # print('right number = ' + str(right_number.value))

        right_term = self._term(left_term)

        if right_term == None:
            return left_term

        return right_term

    def _final(self):
        cur_token = self.tokenStream.get()
        if cur_token.toktype == 'NUMBER':
            cur_token, self.tokenStream = self.tokenStream.consume()
            return AST(cur_token.value, 'NUMBER', None)
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

data = '1 - (2- (4-5*7 + 2/5) )'
tokenStream = getTokenStream(data)
parser = Parser(tokenStream)
print(parser.AST.evaluate())

dot = Digraph(comment='ast dump')

ini = 0

def dfs(ast):

    global ini

    if ast == None:
        return

    ini+= 1

    local_num = str(ini)

    if ast.op == 'NUMBER':
        name = str(ast.left)
    else:
        name = ast.op
   
    dot.node(name=str(ini), label=name)
   
    if type(ast.left) == AST:
        left_node = dfs(ast.left)
        dot.edge(local_num, left_node)

    if type(ast.right) == AST:
        right_node = dfs(ast.right)
        dot.edge(local_num, right_node)

    return local_num

dfs(parser.AST)

dot.render('test-output/ast_dump.gv', view=True)        