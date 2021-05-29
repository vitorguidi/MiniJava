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

        print(node)
        print(node.get_children())
        print('###')

        for (child, edge_label) in node.get_children():
            child = self.dfs(child)
            self.dot.edge(this_id, child, label = edge_label)

        return this_id