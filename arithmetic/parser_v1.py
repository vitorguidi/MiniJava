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
# expr = OP start expr | eps

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
        parsedStream = self._parse(tokenStream)
        self.AST = AST(parsedStream.left, parsedStream.op, parsedStream.right)

    def _parse(self, tokenStream):
        return self._start(tokenStream)

    def _start(self, tokenStream):

        cur_token = tokenStream.get()
        
        if cur_token.toktype == 'NUMBER':
            print('getting number ' + str(cur_token.value))
            left, tokenStream = tokenStream.consume()
        else:
            raise SyntaxError('Expected NUMBER, got {}'.format(cur_token.toktype))

        right = self._expr(tokenStream, cur_token)

        return right

    def _expr(self, tokenStream, prev_token):

        cur_token = tokenStream.get()

        if cur_token.toktype == 'END':
            return AST(prev_token.value, 'NUMBER', None)

        elif cur_token.toktype == 'OP1':
            op, tokenStream = tokenStream.consume()
        
        else:
            raise SyntaxError('Expected OP1, found {}'.format(cur_token.toktype))

        left_expr = AST(prev_token.value, prev_token.toktype, None)

        right_number, tokenStream = tokenStream.consume()
        print('right number = ' + str(right_number.value))

        right_expr = self._expr(tokenStream, right_number)

        return AST(left_expr, op.value, right_expr)

                
data = '1 + 23 - 4 + 2 - 2'
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

    if type(ast) == int:
        return str(int)
    elif ast.op == 'NUMBER':
        name = str(ini) + ' : NUMBER ' + str(ast.left)
    else:
        name = str(ini) + ' : OP = ' + ast.op
   
    dot.node(str(ini), name)
   
    if type(ast.left) == AST:
        left_node = dfs(ast.left)
        print('name = ' + name)
        print('left node  = ' + left_node)
        dot.edge(name, left_node)

    if type(ast.right) == AST:
        right_node = dfs(ast.right)
        print('name = ' + name)
        print('right node = ' + right_node)
        dot.edge(name, right_node)

    return name

dfs(parser.AST)

dot.render('test-output/ast_dump.gv', view=True)