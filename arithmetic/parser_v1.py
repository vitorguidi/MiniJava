from lexer import getTokenStream
from graphviz import Digraph

# simple grammar for expressions with + and - operations

#   expr =
#           expr OP final 
#       |   final

# eliminates left recursion
# Given A = Ax | B
# we get
# A = BA'
# A' = xA' | eps

# A = expr
# x = (OP final)
# B = final

# then we have
# expr = final A'
# A' = OP final A' | eps

#for clarity sake
# start = final expr
# expr = OP final expr | eps

class SyntaxError(Exception):
    ''' Raised when syntax rules are breached '''
    def __init__(self, message):
        self.message = message

class AST:

    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self):
        if self.op == 'NUMBER':
            return self.left
        return self._apply_op(self.left.evaluate(), self.op, self.right.evaluate())

    def _apply_op(self, left, op, right):
        if op == '+':
            return left + right
        else:
            return left - right

class Parser:

    def __init__(self, tokenStream):
        self.AST = self._parse(tokenStream)

    def _parse(self, tokenStream):
        return self._start(tokenStream)

    def _start(self, tokenStream):

        cur_token = tokenStream.get()
        
        if cur_token.toktype == 'NUMBER':
            left, tokenStream = tokenStream.consume()
        else:
            raise SyntaxError('Expected NUMBER, got {}'.format(cur_token.toktype))

        base_ast = AST(cur_token.value, 'NUMBER', None)

        right = self._expr(tokenStream, base_ast)

        return right

    def _expr(self, tokenStream, prev_ast):

        cur_token = tokenStream.get()

        if cur_token.toktype == 'END':
            return None

        elif cur_token.toktype == 'OP1':
            op, tokenStream = tokenStream.consume()
        
        else:
            raise SyntaxError('Expected OP1, found {}'.format(cur_token.toktype))

        right_number, tokenStream = tokenStream.consume()
        local_right_ast = AST(right_number.value, 'NUMBER', None)

        left_expr = AST(prev_ast, op.value, local_right_ast)

        # print('right number = ' + str(right_number.value))

        right_expr = self._expr(tokenStream, left_expr)

        if right_expr == None:
            return left_expr

        return right_expr

                
data = '1 -2 + 3 - 4'
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