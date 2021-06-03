from Ast import *

class Block:
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list
        self.main_next = None
        self.alt_next = None
        self.cond_expr = None
        self.visited = set()

    def __str__(self):
        return '####\n' + '\n'.join([str(x) for x in self.stmt_list]) + '\n###\n'

    #can make a basic block untill we find a if/while block
    def join(self, other_block):
        self.stmt_list += other_block.get_stmt_list()
        self.main_next = other_block.get_main_next()

    def connect_main(self, other_block):
        self.main_next = other_block

    def connect_alt(self, other_block):
        self.alt_next = other_block

    def get_main_next(self):
        return self.main_next

    def get_alt_next(self):
        return self.alt_next

    def get_stmt_list(self):
        return self.stmt_list

class ConditionalBlock(Block):
    def __init__(self, cond_expr):
        super().__init__([])
        self.cond_expr = cond_expr

    def get_cond_expr(self):
        return self.cond_expr

class IfBlock(ConditionalBlock):
    def __init__(self, cond_expr):
        super().__init__(cond_expr)

    def __str__(self):
        return 'if'

class WhileBlock(ConditionalBlock):
    def __init__(self, cond_expr):
        super().__init__(cond_expr)

    def __str__(self):
        return 'while'

class ConditionalEndBlock(Block):
    def __init__(self):
        super().__init__([])

    def __str__(self):
        return 'separator'

class ReturnBlock(Block):
    def __init__(self, stmt_list):
        super().__init__(stmt_list)

class StartBlock(Block):
    def __init__(self, class_name, method_name):
        self.class_name = class_name
        self.method_name = method_name
        super().__init__([])

    def __str__(self):
        return '{} : {}'.format(self.class_name, self.method_name)

class CFG:

    #takes a class as argument
    def __init__(self, program : ProgramNode):
        self.cfg_list = []

        main_class = program.get_main_class()
        for method in main_class.get_methods():
            self._build_head_node(main_class.get_class_id(), method.get_method_id(), method)
         
        for other_class in program.get_other_classes():
            for method in other_class.get_methods():
                self._build_head_node(other_class.get_class_id(), method.get_method_id(), method)

    def _build_head_node(self, class_id, method_id, method):
        head_node = StartBlock(class_id, method_id)
        method_cfg, _ = self._cfg_from_stmt_list(method.get_stmt_list())
        method_cfg = self._clean(method_cfg)
        method_cfg = self._build_basic_blocks(method_cfg)
        head_node.connect_main(method_cfg)
        self.cfg_list.append(head_node)

    #retorna bloco de inicio e bloco de fim da cadeia
    def _cfg_from_stmt_list(self, stmt_list):
        
        # if not stmt_list:
        #     dummy = Block([])
        #     return dummy, dummy


        cur_ast_node = stmt_list[0]
 
        
        cur_cfg_node, cur_cfg_exit = self._cfg_from_stmt_node(cur_ast_node)

        if len(stmt_list) > 1:
            nxt_cfg_node, nxt_cfg_exit = self._cfg_from_stmt_list(stmt_list[1:])
            cur_cfg_exit.connect_main(nxt_cfg_node)
        else:
            nxt_cfg_node, nxt_cfg_exit = cur_cfg_node, cur_cfg_exit

        return cur_cfg_node, nxt_cfg_exit

    #idem
    def _cfg_from_stmt_node(self, node):

        if isinstance(node, StmtBlock):
            return self._cfg_from_stmt_list(node.get_stmt_list())
        
        elif isinstance(node, IfStmt):
          
            head_block = IfBlock(node.get_cond_expr())
            main_path, exit_main_path = self._cfg_from_stmt_node(node.get_main_stmt())
            alt_path, exit_alt_path = self._cfg_from_stmt_node(node.get_alt_stmt())
               
            dummy_null_exit = ConditionalEndBlock()
            head_block.connect_main(main_path)
            head_block.connect_alt(alt_path)

            exit_main_path.connect_main(dummy_null_exit)
            exit_alt_path.connect_main(dummy_null_exit)
            
            return head_block, dummy_null_exit

        elif isinstance(node, WhileStmt):

            head_block = WhileBlock(node.get_cond_expr())
            main_path_entry, main_path_exit = self._cfg_from_stmt_node(node.get_stmt())
            dummy_null_exit = ConditionalEndBlock()
          
            head_block.connect_main(main_path_entry)
            head_block.connect_alt(dummy_null_exit)
            main_path_exit.connect_main(head_block)

            return head_block, dummy_null_exit

        elif isinstance(node, ReturnStmt):

            head_block = ReturnBlock([node])
            return head_block, head_block

        else:
            head_block = Block([node])
            return head_block, head_block

    def _clean(self, node):
        visited = set()
        return self._clean_dfs(node, visited)

    def _clean_dfs(self, node, visited, dad = None):
        if not node:
            return

        if id(node) in visited:
            return        

        visited.add(id(node))

        self._clean_dfs(node.get_alt_next(), visited, node)
        self._clean_dfs(node.get_main_next(), visited, node)

        nxt_main_node = node.get_main_next()
        nxt_alt_node = node.get_alt_next()

        if isinstance(nxt_main_node, ConditionalEndBlock):
            node.main_next = nxt_main_node.get_main_next()

        if isinstance(nxt_alt_node, ConditionalEndBlock):
            node.alt_next = nxt_alt_node.get_main_next()


        return node

    def _build_basic_blocks(self, node):
        visited = set()
        return self._basic_blocks_dfs(node, visited)

    def _basic_blocks_dfs(self, node, visited, dad = None):
        if id(node) in visited or not node:
            return

        visited.add(id(node))

        self._basic_blocks_dfs(node.get_alt_next(), visited, node)
        self._basic_blocks_dfs(node.get_main_next(), visited, node)

        nxt_main_node = node.get_main_next()
        nxt_alt_node = node.get_alt_next()

        forbidden_types = [IfBlock, WhileBlock, ConditionalEndBlock, StartBlock, ReturnBlock]

        if not nxt_alt_node and type(node) not in forbidden_types and type(nxt_main_node) not in forbidden_types and nxt_main_node:
            node.join(nxt_main_node)
      

        return node



    def get_cfg_list(self):
        return self.cfg_list