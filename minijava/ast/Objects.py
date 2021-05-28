from .Ast import Ast, NodeType

class ProgramNode(Ast):
    def __init__(self, main_class, other_classes):
        self.type = NodeType.PROGRAM
        self.main_class = main_class
        self.other_classes = other_classes

    def get_main_class(self):
        return self.main_class

    def get_other_classes(self):
        return self.other_classes

class ClassNode(Ast):
    def __init__(self, class_id, var_list, methods, class_type = NodeType.CLASS, parent_class = None):
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

class MainClassNode(ClassNode):
    def __init__(self, class_id, var_list, class_methods):
        super.__init__(class_id, var_list, class_methods, NodeType.MAINCLASS)

class VariableNode(Ast):
    def __init__(self, var_type, var_id):
        self.var_type = var_type
        self.var_id = var_id
        self.type = NodeType.VARIABLE

    def get_id(self):
        return self.var_id

    def get_var_type(self):
        return self.var_type

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