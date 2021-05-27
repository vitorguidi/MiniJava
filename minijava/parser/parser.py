from minijava.ast.Stmt import ArrayAssigntStmt, AssignStmt, IfStmt, PrintStmt, StmtBlock, WhileStmt, ifStmt
from minijava.ast.Objects import MainClassNode, MethodNode, ProgramNode
from ply import lex
from ..lexer.lexer import getTokenStream, TokenTypes
from ..ast.Objects import *

class SyntaxError(Exception):
    ''' Raised when syntax rules are breached '''
    def __init__(self, message):
        self.message = message

class parser:

    def __init__(self, data):
        self.tokens = getTokenStream(data)
        self.AST = self._parse()

    def _parse(self):
        return self._program()

    def _consume_single_from_stream(self, expected):
        ans = []
        for expected_type in expected:
            cur_type = self.tokens.peep(0)
            if cur_type != expected_type:
                raise SyntaxError('Expected {}, found {}'.format(expected_type ,cur_type))
            ans.append(self.tokens.consume())
        return ans

    def _consume_many_from_stream(self, expected):
        cur_type = self.tokens.peep(0)
        if cur_type != expected:
            raise SyntaxError('Expected {}, found {}'.format(expected ,cur_type))
        return self.tokens.consume()

     
    def _program(self):
        classes = []
        main_class = self._main_class()
        
        while True:
            consumed_class = self._class_decl()
            if consumed_class:
                classes.append( consumed_class )
            else:
                break
        
        return ProgramNode(main_class, classes)

    def _main_class(self):

        if self.tokens.peep(0) != TokenTypes.CLASS:
            return None
        
        [_, class_id] = self.consume_many_from_stream([TokenTypes.CLASS, TokenTypes.ID])

        class_id = class_id.value

        self.consume_many_from_stream([TokenTypes.LBRACE, TokenTypes.PUBLIC, TokenTypes.STATIC, TokenTypes.VOID,
            TokenTypes.MAIN, TokenTypes.LPAREN, TokenTypes.STRING, TokenTypes.LSQPAREN, TokenTypes.RQSPAREN, TokenTypes.ID,
                TokenTypes.RPAREN, TokenTypes.LBRACE])

        body = self._stmt()

        main_method = MethodNode('main', ObjectTypes.VOID, [], [body])

        self._consume_many_from_stream([TokenTypes.RBRACE, TokenTypes.RBRACE]) 

        return MainClassNode(class_id, [], [main_method])

    def _class_decl(self):

        if self.tokens.peep(0) != TokenTypes.CLASS:
            return None
    
        [_, class_id] = self._consume_many_from_stream([TokenTypes.CLASS, TokenTypes.ID])

        diff_token = self.tokens.peep(0)

        var_list = []
        methods_list = []

        if diff_token == TokenTypes.LBRACE:
            self._consume_single_from_stream(TokenTypes.LBRACE)
            # get var decls
            #should return None if nothing to match
            while True:
                consumed_var = self._var_decl()
                if consumed_var:
                    var_list.append(consumed_var)
                else:
                    break
            
            #get methods
            #should return None if nothing to match
            while True:
                consumed_method = self._method_decl()
                if consumed_method:
                    methods_list.append(self._method_decl())
                else:
                    break

        #elif diff_token == TokenTypes.EXTENDS:
        #to be implemented

        else:
            raise SyntaxError('Expected {} , found {}', TokenTypes.LBRACE, diff_token)

        return ClassNode(class_id, var_list, methods_list)

    def _type(self):
        peep = self.tokens.peep(0)
        
        if peep == TokenTypes.INTEGER:
            if self.tokens.peep(1) == TokenTypes.LSQPAREN and self.tokens.peep(2) == TokenTypes.RQSPAREN:
                self._consume_many_from_stream(TokenTypes.INTEGER, TokenTypes.LSQPAREN, TokenTypes.RQSPAREN)
                return 'INTEGER_ARRAY'
            else:
                self._consume_single_from_stream(TokenTypes.INTEGER)
                return 'INTEGER_LITERAL'

        elif peep == TokenTypes.BOOLEAN:
            self._consume_single_from_stream(TokenTypes.BOOLEAN)
            return 'BOOLEAN'

        elif peep == TokenTypes.ID:
            return self._consume_single_from_stream(TokenTypes.ID).value
            
        else:
            return None
  

    def _var_decl(self):
        var_list = []
        while True:
            consumed_type = self._type()
            if not consumed_type:
                break
            consumed_id = self._consume_single_from_stream(TokenTypes.ID)
            self._consume_single_from_stream(TokenTypes.SEMICOLON)
            var_list.append(VariableNode(consumed_type, consumed_id.value))
        return var_list

    def _method_decl(self):
        peep = self.tokens.peep(0)
        if peep != TokenTypes.PUBLIC:
            return None
        
        self._consume_single_from_stream(TokenTypes.PUBLIC)

        consumed_type = self._type()
        if not consumed_type:
            raise SyntaxError("Expected to find a type, came across {}".format(peep))

        [method_id, _] = self._consume_many_from_stream([TokenTypes.ID, TokenTypes.LPAREN])

        formal_list = self._formal_list()

        self._consume_many_from_stream([TokenTypes.RPAREN, TokenTypes.LBRACE])

        var_decl = self._var_decl()

        statement_list = []

        while True:
            consumed_statement = self._stmt()
            if not consumed_statement:
                break
            statement_list.append(consumed_statement)

        self._consume_single_from_stream(TokenTypes.RETURN)

        return_expr = self._expr()
        self._consume_many_from_stream([TokenTypes.SEMICOLON, TokenTypes.RBRACE])

        return MethodNode(method_id.value, consumed_type, formal_list, var_decl, statement_list)


    def _formal_list(self):
        consumed_type = self._type()
        if not Type:
            return []
        consumed_id = self._consume_single_from_stream(TokenTypes.ID)
        formal_list = []
        formal_list.append(VariableNode(consumed_type, consumed_id.value))
        return formal_list + self._formal_rest()

    def _formal_rest(self):
        formal_rest = []
        while True:
            peep = self.tokens.peep(0)
            if peep != TokenTypes.COMMA:
                break
            self._consume_single_from_stream(TokenTypes.COMMA)
            consumed_type = self._type()
            consumed_id = self._consume_single_from_stream(TokenTypes.ID)
            formal_rest.append(VariableNode(consumed_type, consumed_id.value))
        return formal_rest

        

    def _stmt(self):
        peep = self.tokens.peep(0)
        if peep not in [TokenTypes.LBRACE, TokenTypes.IF, TokenTypes.WHILE, TokenTypes.PRINTLN, TokenTypes.ID]:
            return None
        
        if peep == TokenTypes.LBRACE:
            self._consume_single_from_stream(TokenTypes.LBRACE)
            stmt_list = []
            while True:
                stmt = self._stmt()
                if not stmt:
                    break
                stmt_list.append(stmt)
            self._consume_single_from_stream(TokenTypes.RBRACE)
            return StmtBlock(stmt_list)

        elif peep == TokenTypes.IF:
            self._consume_many_from_stream([TokenTypes.IF, TokenTypes.LPAREN])
            cond_expr = self._expr()
            self._consume_single_from_stream(TokenTypes.RPAREN)
            main_stmt = self._stmt()
            alt_stmt = None
            if self.tokens.peep(0) == TokenTypes.ELSE:
                self._consume_single_from_stream(TokenTypes.ELSE)
                alt_stmt = self._stmt()
            return IfStmt(main_stmt, cond_expr, alt_stmt)
        
        elif peep == TokenTypes.WHILE:
            self._consume_many_from_stream([TokenTypes.WHILE, TokenTypes.LPAREN])
            cond_expr = self._expr()
            self._consume_single_from_stream(TokenTypes.RPAREN)
            stmt = self._stmt()
            return WhileStmt(cond_expr, stmt)

        elif peep == TokenTypes.PRINTLN:
            self._consume_many_from_stream([TokenTypes.PRINTLN, TokenTypes.LPAREN])
            print_expr = self._expr()
            self._consume_many_from_stream([TokenTypes.RPAREN, TokenTypes.SEMICOLON])
            return PrintStmt(print_expr)

        elif peep == TokenTypes.ID:
            next_peep = self.tokens.peep(1)

            if next_peep == TokenTypes.ASSIGN:
                [id, _] = self._consume_many_from_stream([TokenTypes.ID, TokenTypes.ASSIGN])
                expr = self._expr()
                self._consume_single_from_stream(TokenTypes.SEMICOLON)
                return AssignStmt(id.value, expr)
                
            elif next_peep == TokenTypes.RSQPAREN:
                [id, _] = self._consume_many_from_stream([TokenTypes.ID, TokenTypes.RSQPAREN])
                pos_expr = self._expr()
                self._consume_many_from_stream([TokenTypes.RSQPAREN, TokenTypes.ASSIGN])
                value_expr = self._expr()
                self._consume_single_from_stream(TokenTypes.SEMICOLON)
                return ArrayAssigntStmt(id.value, pos_expr, value_expr)

            else:
                raise SyntaxError('Expected {} or {}, found {}', TokenTypes.ASSIGN, TokenTypes.RQSPAREN, next_peep)

    def _expr(self):






