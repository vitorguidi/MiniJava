from Ast import *
from Lexer import getTokenStream, TokenTypes
import pdb

cnt = 0

class SyntaxError(Exception):
    ''' Raised when syntax rules are breached '''
    def __init__(self, message):
        self.message = message

class Parser:

    def __init__(self, data):
        self.tokens = getTokenStream(data)
        self.AST = self._parse()

    def get_ast(self):
        return self.AST

    def _parse(self):
        return self._program()

    def _consume_many_from_stream(self, expected):
        ans = []
        for expected_type in expected:
            cur_type = self.tokens.peep(0)
            if cur_type != expected_type:
                raise SyntaxError('Expected {}, found {}'.format(expected_type ,cur_type))
            ans.append(self.tokens.consume())
        return ans

    def _consume_single_from_stream(self, expected):
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
        
        [_, class_id] = self._consume_many_from_stream([TokenTypes.CLASS, TokenTypes.ID])

        class_id = class_id.value

        self._consume_many_from_stream([TokenTypes.LBRACE, TokenTypes.PUBLIC, TokenTypes.STATIC, TokenTypes.VOID,
            TokenTypes.MAIN, TokenTypes.LPAREN, TokenTypes.STRING, TokenTypes.LSQPAREN, TokenTypes.RSQPAREN, TokenTypes.ID,
                TokenTypes.RPAREN]) 

        body = self._stmt()

        main_method = MethodNode('main', 'void', [], [], [body], NullNode())

        self._consume_many_from_stream([TokenTypes.RBRACE]) 

        return MainClassNode(class_id, [], [main_method])

    def _class_decl(self):

        peep = self.tokens.peep(0)

        if peep != TokenTypes.CLASS:
            return None
    
        [_, class_id] = self._consume_many_from_stream([TokenTypes.CLASS, TokenTypes.ID])
        class_id = class_id.value

        parent_class = None

        if self.tokens.peep(0) == TokenTypes.EXTENDS:
            [_, parent_class_id] = self._consume_many_from_stream([TokenTypes.EXTENDS, TokenTypes.ID])
            parent_class = parent_class_id.value


        self._consume_single_from_stream(TokenTypes.LBRACE)
        # get var decls
        #should return None if nothing to match
        var_list = self._var_decl()
        
        #get methods
        #should return None if nothing to match
        methods_list = []
        while True:
            consumed_method = self._method_decl()
            if consumed_method:
                methods_list.append(consumed_method)
            else:
                break

        self._consume_single_from_stream(TokenTypes.RBRACE)

        return ClassNode(class_id, var_list, methods_list, parent_class = parent_class)

    def _type(self):
        peep = self.tokens.peep(0)
        peep_ahead = self.tokens.peep(1)
        
        if peep == TokenTypes.INTEGER:
            if self.tokens.peep(1) == TokenTypes.LSQPAREN and self.tokens.peep(2) == TokenTypes.RSQPAREN:
                self._consume_many_from_stream([TokenTypes.INTEGER, TokenTypes.LSQPAREN, TokenTypes.RSQPAREN])
                return 'INTEGER_ARRAY'
            else:
                self._consume_single_from_stream(TokenTypes.INTEGER)
                return 'INTEGER_LITERAL'

        elif peep == TokenTypes.BOOLEAN:
            self._consume_single_from_stream(TokenTypes.BOOLEAN)
            return 'BOOLEAN'

        elif peep == TokenTypes.ID  and peep_ahead != TokenTypes.ASSIGN: #avid conflict with assign stmt
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

        return_stmt = ReturnStmt(self._expr())
        print('return stmt = ', return_stmt)
        
        statement_list.append(return_stmt)
        self._consume_many_from_stream([TokenTypes.SEMICOLON, TokenTypes.RBRACE])
        
        return MethodNode(method_id.value, consumed_type, formal_list, var_decl, statement_list, return_stmt)


    def _formal_list(self):
        consumed_type = self._type()
        if not consumed_type:
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
            
            alt_stmt = NullNode()
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
                return AssignStmt( id.value, expr)
                
            elif next_peep == TokenTypes.LSQPAREN:
                [id, _] = self._consume_many_from_stream([TokenTypes.ID, TokenTypes.LSQPAREN])
                pos_expr = self._expr()
                self._consume_many_from_stream([TokenTypes.RSQPAREN, TokenTypes.ASSIGN])
                value_expr = self._expr()
                self._consume_single_from_stream(TokenTypes.SEMICOLON)
                return ArrayAssigntStmt(id.value, pos_expr, value_expr)

            else:
                raise SyntaxError('Expected {} or {}, found {}', TokenTypes.ASSIGN, TokenTypes.RSQPAREN, next_peep)

    # Exp               -> OrExpr
    # OrExpr            -> AndExpr  ( || AndExpr)*
    # AndExpr           -> EqualityExpr ( && EqualityExpr )*
    # EqualityExpr      -> CompExpr ( OP4 CompExpr)
    # CompExpr          -> AdditiveExpr [ OP3 AdditiveExpr ]
    # AdditiveExpr      -> TimesExpr ( OP2 TimesExpr )*
    # TimesExpr         -> PrefixExpr ( OP1 PrefixExpr )*
    # PrefixExp         -> Not | PostfixExp
    # Not               -> ( ! )+ PostfixExp
    # PostfixExp        -> PrimaryExp Suffix
    # Suffix            -> ( "[" Exp "]" 
    #                      | . id ["(" ExpList ")"]  
    #                      | . length )*
    # PrimaryExp        -> INTEGER_LITERAL
    #                   -> true
    #                   -> false
    #                   -> id
    #                   -> this
    #                   -> "(" Exp ")"
    #                   -> new int "[" Exp "]"
    #                   -> new id "(" ")"

    def _expr(self):
        return self._or_expr()

    def _or_expr(self):
        left_term = self._and_expr()
        if self.tokens.peep(0) == TokenTypes.OR:
            self._consume_single_from_stream(TokenTypes.OR)
            right_term = self._or_expr()
            return OrExpr(left_term, right_term)
        return left_term

    def _and_expr(self):
        left_term = self._equality_expr()
        if self.tokens.peep(0) == TokenTypes.AND:
            self._consume_single_from_stream(TokenTypes.AND)
            right_term = self._and_expr()
            return AndExpr(left_term, right_term)
        return left_term

    def _equality_expr(self):               #not gonna support chained comparisons for eq;ineq
        left_term = self._comp_expr()
        potential_expr_sign = self.tokens.peep(0)
        if potential_expr_sign == TokenTypes.OP4:
            op = self._consume_single_from_stream(TokenTypes.OP4)
            right_term = self._comp_expr()
            return EqualityExprFactory(left_term, op, right_term)
        return left_term

    def _comp_expr(self):
        left_term = self._additive_expr()           #not gonna support chained comparisons for < > <= >=
        potential_expr_sign = self.tokens.peep(0)
        if potential_expr_sign == TokenTypes.OP3:
            op = self._consume_single_from_stream(TokenTypes.OP3)
            right_term = self._additive_expr()
            return CompExprFactory(left_term, op, right_term)
        return left_term

    def _additive_expr(self):
        left_term = self._times_expr()
        potential_expr_sign = self.tokens.peep(0)
        if potential_expr_sign == TokenTypes.OP2:
            op = self._consume_single_from_stream(TokenTypes.OP2)
            right_term = self._additive_expr()
            return AdditiveExprFactory(left_term, op, right_term)
        return left_term

    def _times_expr(self):
        left_term = self._prefix_expr()
        potential_expr_sign = self.tokens.peep(0)
        if potential_expr_sign == TokenTypes.OP1:
            op = self._consume_single_from_stream(TokenTypes.OP1)
            right_term = self._times_expr()
            return TimesExprFactory(left_term, op, right_term)
        return left_term

    def _prefix_expr(self):
        peep = self.tokens.peep(0)
        if peep ==  TokenTypes.NOT:
            self._consume_single_from_stream(TokenTypes.NOT)
            arg = self._postfix_expr()
            return NotExpr(arg)
        return self._postfix_expr()

    def _postfix_expr(self):
        primary_expr = self._primary_expr()
        return self._suffix(primary_expr)

    def _suffix(self, left_expr):
        peep = self.tokens.peep(0)

        #array access
        if peep == TokenTypes.LSQPAREN:
            self._consume_single_from_stream(TokenTypes.LSQPAREN)
            inner_expr = self._expr()
            self._consume_single_from_stream(TokenTypes.RSQPAREN)
            cur_production = ArrayAccessExpr(left_expr, inner_expr)

            return self._suffix(cur_production)

        #method access, object variable access or length
        elif peep == TokenTypes.DOT:
            self._consume_single_from_stream(TokenTypes.DOT)
            peep = self.tokens.peep(0)

            if peep == TokenTypes.ID:
                id = IdNode(self._consume_single_from_stream(TokenTypes.ID).value)
                peep = self.tokens.peep(0)

                #method access
                if peep == TokenTypes.LPAREN:
                    self._consume_single_from_stream(TokenTypes.LPAREN)
                    expr_list = self._expr_list()
                    self._consume_single_from_stream(TokenTypes.RPAREN)
                    cur_production = MethodCallExpr(left_expr, id, expr_list)
                    return self._suffix(cur_production)

                #object access
                else:
                    cur_production = ObjectAccessExpr(left_expr, id)
                    return self._suffix(cur_production)

            #length op
            elif peep == TokenTypes.LENGTH:
                self._consume_single_from_stream(TokenTypes.LENGTH)
                cur_production = ArrayLengthExpr(left_expr)
                return self._suffix(cur_production)


        #no suffix
        else:
            return left_expr

    def _primary_expr(self):
        
        peep = self.tokens.peep(0)

        if peep == TokenTypes.LPAREN:
            self._consume_single_from_stream(TokenTypes.LPAREN)
            ans = self._expr()
            self._consume_single_from_stream(TokenTypes.RPAREN)
            return ans
        
        elif peep == TokenTypes.INTEGER_LITERAL:
            value = self._consume_single_from_stream(TokenTypes.INTEGER_LITERAL).value
            return IntegerLiteralNode(value)

        elif peep == TokenTypes.THIS:
            _ = self._consume_single_from_stream(TokenTypes.THIS).value
            return ThisNode()

        elif peep == TokenTypes.TRUE:
            _value = self._consume_single_from_stream(TokenTypes.TRUE).value
            return TrueNode()

        elif peep == TokenTypes.FALSE:
            _ = self._consume_single_from_stream(TokenTypes.FALSE).value
            return FalseNode()

        elif peep == TokenTypes.ID:
            value = self._consume_single_from_stream(TokenTypes.ID).value
            return IdNode(value)

        elif peep == TokenTypes.NEW:
            self._consume_single_from_stream(peep)
            peep = self.tokens.peep(0)
          
            if peep == TokenTypes.INTEGER:
                self._consume_many_from_stream([TokenTypes.INTEGER, TokenTypes.LSQPAREN])
                size_expr = self._expr()
                self._consume_single_from_stream(TokenTypes.RSQPAREN)
                return NewIntArrayExpr(size_expr)

            elif peep == TokenTypes.ID:
                [id, _, _] = self._consume_many_from_stream([TokenTypes.ID, TokenTypes.LPAREN, TokenTypes.RPAREN])
                return NewObjectExpr(id.value)
            else:
                raise SyntaxError("Expected {} or {}, found {}.".format(TokenTypes.INTEGER, TokenTypes.ID, peep))

        else:
            return None


    def _expr_list(self):
        expr_list = []
        first_expr = self._expr()
        
        if not first_expr:
            return expr_list
        
        expr_list.append(first_expr)
        
        while self.tokens.peep(0) == TokenTypes.COMMA:
            self._consume_single_from_stream(TokenTypes.COMMA)
            inner_expr = self._expr()
            if not inner_expr:
                raise SyntaxError('Expected an expr after comma in ExprList, got nothing.')
            expr_list.append(inner_expr)
        
        return expr_list
