from Ast import Ast
from graphviz import Digraph

class AstPrinter:
    def __init__(self, ast):
        self.ast = ast
        self.cnt = 0
        self.dot = Digraph(comment='ast dump')

        
    def print(self):
        self.dfs(self.ast)
        self.dot.render('test-output/ast_dump.gv', view=True) 

    def dfs(self, node):
        self.cnt += 1
      
        this_id = str(self.cnt)

        self.dot.node(name=this_id, label=str(node))

        for (child, edge_label) in node.get_children():
            child = self.dfs(child)
            self.dot.edge(this_id, child, edge_label = edge_label)

        return this_id      

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