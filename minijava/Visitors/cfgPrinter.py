from CFG import *
from graphviz import Digraph

class CFGPrinter:
    def __init__(self, cfg):
        self.cfg_list = cfg.get_cfg_list()
        self.cnt = 0
        self.dot = Digraph(comment='cfg dump')
        self.visited = dict()
        self.visited2 = dict()

        
    def print(self):
        for method in self.cfg_list:
            #method = self.dfs_clean(method)
            self.dfs(method)
        self.dot.render('test-output/cfg_dump.gv', view=True)

    #second pass over cfg to join
    def dfs_clean(self, node):
        if id(node) in self.visited2:
            return self.visited2[id(node)]


        if node.get_main_next():
            node.main_next = self.dfs_clean(node.get_main_next())

        if node.get_alt_next():
            node.alt_next = self.dfs_clean(node.get_alt_next())

        if not node.get_stmt_list() and not isinstance(node, StartBlock):
            self.visited2[id(node)] = node.get_main_next()
        else:
            self.visited2[id(node)] = node

        return self.visited2[id(node)]

        

    def dfs(self, node, dad=None):
       
        #id(x) = unique identifier of an object
        #serves our purpose here
        if id(node) in self.visited:
            return self.visited[id(node)]
            
        self.cnt += 1
      
        this_id = str(self.cnt)
        self.visited[id(node)] = this_id

        self.dot.node(name=this_id, label=str(node))

        main = node.get_main_next()
        alt = node.get_alt_next()

        for (child, label) in [(main, 'main flow'), (alt, 'alt flow')]:
            if not child:
                continue
            child_id = self.dfs(child, node)
            self.dot.edge(this_id, child_id, label = label)

        return this_id
