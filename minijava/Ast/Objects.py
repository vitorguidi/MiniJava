from .Ast import Ast, NodeType
from .Terminal import NullNode

class ProgramNode(Ast):
    def __init__(self, main_class, other_classes):
        self.type = NodeType.PROGRAM
        self.main_class = main_class
        self.other_classes = other_classes

    def get_main_class(self):
        return self.main_class

    def get_other_classes(self):
        return self.other_classes

    def __str__(self):
        return 'program'

    def get_children(self):
        edges = [(self.main_class, 'main class')]
        for other_class in self.other_classes:
            edges.append( (other_class, 'class') )
        return edges

class ClassNode(Ast):
    def __init__(self, class_id, var_list, methods, class_type = NodeType.CLASS, parent_class = NullNode()):
        self.type = class_type
        self.class_id = class_id
        self.var_list = var_list
        self.methods = methods
        self.parent_class = parent_class

    def get_class_id(self):
        return self.class_id

    def get_var_list(self):
        return self.var_list

    def get_methods(self):
        return self.methods

    def get_parent_class(self):
        return self.parent_class

    def __str__(self):
        return 'class : id = {}, parent = {}'.format(self.get_class_id(), self.get_parent_class())

    def get_children(self):
        edges = [ ]
        for method in self.methods:
            edges.append( (method, 'method') )
        for var in self.var_list:
            edges.append( (var, 'inner variable') )
        return edges


class MainClassNode(ClassNode):
    def __init__(self, class_id, var_list, class_methods):
        super().__init__(class_id, var_list, class_methods, NodeType.MAINCLASS)

    def __str__(self):
        return 'main class'

class VariableNode(Ast):
    def __init__(self, var_type, var_id):
        self.var_type = var_type
        self.var_id = var_id
        self.type = NodeType.VARIABLE

    def get_id(self):
        return self.var_id

    def get_var_type(self):
        return self.var_type

    def __str__(self):
        return 'Variable - id = {}, type = {}'.format(self.var_id, self.var_type)

    def get_children(self):
        return []

class MethodNode(Ast):
    def __init__(self, method_id, return_type, args_list, var_list, stmt_list):
        self.method_id = method_id
        self.return_type = return_type
        self.args_list = args_list
        self.var_list = var_list
        self.stmt_list = stmt_list
        self.type = NodeType.METHOD

    def get_method_id(self):
        return self.method_id

    def get_return_type(self):
        return self.return_type

    def get_args_list(self):
        return self.args_list

    def get_var_list(self):
        return self.var_list

    def get_stmt_list(self):
        return self.stmt_list

    def __str__(self):
        return 'method - return type = {}, id = {}'.format(self.return_type, self.method_id)

    def get_children(self):
        edges = []
        cnt = 0
        for arg in self.args_list:
            edges.append( (arg, 'argument {}'.format(cnt)) )
            cnt += 1
        for var in self.var_list:
            edges.append( (var, 'inner variable') )
        cnt = 0
        for stmt in self.stmt_list:
            edges.append( (stmt, 'inner_statement '.format(cnt)) )
        print('method edges = ', edges)
        return edges
