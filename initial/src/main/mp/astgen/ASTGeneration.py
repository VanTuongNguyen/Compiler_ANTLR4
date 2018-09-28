from MPVisitor import MPVisitor
from MPParser import MPParser
from AST import *

class ASTGeneration(MPVisitor):


    def visitProgram(self, ctx:MPParser.ProgramContext):
        return Program(self.visit(ctx.many_declarations()))

    def visitMany_declarations(self, ctx:MPParser.Many_declarationsContext):
        if ctx.many_declarations():
            return self.visit(ctx.declarations()) + self.visit(ctx.many_declarations())
        else:
            return self.visit(ctx.declarations())
        
    def visitDeclarations(self, ctx:MPParser.DeclarationsContext):
        if ctx.var_decl():
            return self.visit(ctx.var_decl())
        if ctx.func_decl():
            return self.visit(ctx.func_decl())
        if ctx.proc_decl():
            return self.visit(ctx.proc_decl())
    


 #VarDecl
    def visitVar_decl(self, ctx:MPParser.Var_declContext):
        return self.visit(ctx.list_decl())

    def visitList_decl(self, ctx:MPParser.List_declContext):
        if ctx.list_decl():
            return self.visit(ctx.decl()) + self.visit(ctx.list_decl())
        else:
            return self.visit(ctx.decl())
        
    def visitDecl(self, ctx:MPParser.DeclContext):
        return [VarDecl(Id(i),self.visit(ctx.types())) for i in self.visit(ctx.list_id())]

    def visitList_id(self, ctx:MPParser.List_idContext):
        if ctx.list_id():
            return [ctx.ID().getText()] + self.visit(ctx.list_id())
        else:
            return [ctx.ID().getText()]



#FuncDecl
    def visitFunc_decl(self, ctx:MPParser.Func_declContext):
        if ctx.var_decl():
            return [FuncDecl(Id(ctx.ID().getText()), self.visit(ctx.param_list()), self.visit(ctx.var_decl()), self.visit(ctx.compound_statement()), self.visit(ctx.types()))]
        else:
            return [FuncDecl(Id(ctx.ID().getText()), self.visit(ctx.param_list()), [] , self.visit(ctx.compound_statement()), self.visit(ctx.types()))]
    def visitParam_list(self, ctx:MPParser.Param_listContext):
        if ctx.not_null_param_list():
            return self.visit(ctx.not_null_param_list())
        else:
            return []
    def visitNot_null_param_list(self, ctx:MPParser.Not_null_param_listContext):
        if ctx.not_null_param_list():
            return self.visit(ctx.param_decl()) + self.visit(ctx.not_null_param_list())
        else:
            return self.visit(ctx.param_decl())
    def visitParam_decl(self, ctx:MPParser.Param_declContext):
        return [VarDecl(Id(i),self.visit(ctx.types())) for i in self.visit(ctx.list_id())]


#ProcDecl
    def visitProc_decl(self, ctx:MPParser.Proc_declContext):
        if ctx.var_decl():
            return [FuncDecl(Id(ctx.ID().getText()), self.visit(ctx.param_list()), self.visit(ctx.var_decl()), self.visit(ctx.compound_statement()) )]
        else:
            return [FuncDecl(Id(ctx.ID().getText()), self.visit(ctx.param_list()), [] , self.visit(ctx.compound_statement()) )]
    
#Types
    def visitTypes(self, ctx:MPParser.TypesContext):
        if ctx.primitive_types():
            return self.visit(ctx.primitive_types())
        else:
            return self.visit(ctx.compound_types())


    def visitPrimitive_types(self, ctx:MPParser.Primitive_typesContext):
        if ctx.BOOLEAN():
            return BoolType()
        if ctx.INTEGER():
            return IntType()
        if ctx.REAL():
            return FloatType()
        if ctx.STRING():
            return StringType()


    def visitCompound_types(self, ctx:MPParser.Compound_typesContext):
        return self.visit(ctx.array_types())
    def visitArray_types(self, ctx:MPParser.Array_typesContext):
        return ArrayType(self.visit(ctx.bound(0)),self.visit(ctx.bound(1)), self.visit(ctx.primitive_types()))
    def visitBound(self, ctx:MPParser.BoundContext):
        if ctx.SUB():
            return int(ctx.SUB().getText() + ctx.INTLIT().getText())
        else:
            return int(ctx.INTLIT().getText())

#Operand       
    def visitOperand(self, ctx:MPParser.OperandContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        if ctx.BOOLLIT():
            return BooleanLiteral(bool((ctx.BOOLLIT().getText()).lower()=="true"))
        if ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        if ctx.ID():
            return Id(ctx.ID().getText())
        if ctx.func_call():
            return self.visit(ctx.func_call())


#Expr
    def visitExpression(self, ctx:MPParser.ExpressionContext):
        if ctx.AND():
            return BinaryOp("andthen",self.visit(ctx.expression()),self.visit(ctx.expression_1()))
        if ctx.OR():
            return BinaryOp("orelse",self.visit(ctx.expression()),self.visit(ctx.expression_1()))
        else:
            return self.visit(ctx.expression_1())

    def visitExpression_1(self, ctx:MPParser.Expression_1Context):
        if ctx.EQ():
            return BinaryOp(ctx.EQ().getText(),self.visit(ctx.expression_2(0)),self.visit(ctx.expression_2(1)))
        if ctx.NEQ():
            return BinaryOp(ctx.NEQ().getText(),self.visit(ctx.expression_2(0)),self.visit(ctx.expression_2(1)))
        if ctx.LT():
            return BinaryOp(ctx.LT().getText(),self.visit(ctx.expression_2(0)),self.visit(ctx.expression_2(1)))
        if ctx.GT():
            return BinaryOp(ctx.GT().getText(),self.visit(ctx.expression_2(0)),self.visit(ctx.expression_2(1)))
        if ctx.GTE():
            return BinaryOp(ctx.GTE().getText(),self.visit(ctx.expression_2(0)),self.visit(ctx.expression_2(1)))
        if ctx.LTE():
            return BinaryOp(ctx.LTE().getText(),self.visit(ctx.expression_2(0)),self.visit(ctx.expression_2(1)))
        else:
            return self.visit(ctx.expression_2(0))
    def visitExpression_2(self, ctx:MPParser.Expression_2Context):
        if ctx.ADD():
            return BinaryOp(ctx.ADD().getText(),self.visit(ctx.expression_2()),self.visit(ctx.expression_3()))
        if ctx.SUB():
            return BinaryOp(ctx.SUB().getText(),self.visit(ctx.expression_2()),self.visit(ctx.expression_3()))
        if ctx.OR():
            return BinaryOp(ctx.OR().getText(),self.visit(ctx.expression_2()),self.visit(ctx.expression_3()))
        else:
            return self.visit(ctx.expression_3())
    def visitExpression_3(self, ctx:MPParser.Expression_3Context):
        if ctx.DIV():
            return BinaryOp(ctx.DIV().getText(),self.visit(ctx.expression_3()),self.visit(ctx.expression_4()))
        if ctx.MUL():
            return BinaryOp(ctx.MUL().getText(),self.visit(ctx.expression_3()),self.visit(ctx.expression_4()))
        if ctx.MOD():
            return BinaryOp(ctx.MOD().getText(),self.visit(ctx.expression_3()),self.visit(ctx.expression_4()))
        if ctx.IDIV():
            return BinaryOp(ctx.IDIV().getText(),self.visit(ctx.expression_3()),self.visit(ctx.expression_4()))
        if ctx.AND():
            return BinaryOp(ctx.AND().getText(),self.visit(ctx.expression_3()),self.visit(ctx.expression_4()))
        else:
            return self.visit(ctx.expression_4())
    def visitExpression_4(self, ctx:MPParser.Expression_4Context):
        if ctx.SUB():
            return UnaryOp(ctx.SUB().getText(),self.visit(ctx.expression_4()))
        if ctx.NOT():
            return UnaryOp(ctx.NOT().getText(),self.visit(ctx.expression_4()))
        else:
            return self.visit(ctx.expression_5())
    def visitExpression_5(self, ctx:MPParser.Expression_5Context):
        if ctx.LSB():
            return ArrayCell(self.visit(ctx.expression_5()),self.visit(ctx.expression()))
        else:
            return self.visit(ctx.expression_6())
    def visitExpression_6(self, ctx:MPParser.Expression_6Context):
        if ctx.LB():
            return self.visit(ctx.expression())
        else:
            return self.visit(ctx.operand())

#Element_arr
    def visitElement_arr(self, ctx:MPParser.Element_arrContext):
        return ArrayCell(self.visit(ctx.expression_5()),self.visit(ctx.expression()))


#Func_call
    def visitFunc_call(self, ctx:MPParser.Func_callContext):
        return CallExpr(Id(ctx.ID().getText()),self.visit(ctx.exp_list()))

#Exp_list
    def visitExp_list(self, ctx:MPParser.Exp_listContext):
        if ctx.not_null_exp_list():
            return self.visit(ctx.not_null_exp_list())
        else:
            return []
    def visitNot_null_exp_list(self, ctx:MPParser.Not_null_exp_listContext):
        if ctx.not_null_exp_list():
            return [self.visit(ctx.expression())] + self.visit(ctx.not_null_exp_list())
        else:
            return [self.visit(ctx.expression())]

#statement
    def visitStatement(self, ctx:MPParser.StatementContext):
        if ctx.assignment_statement():
            return self.visit(ctx.assignment_statement())
        if ctx.if_statement():
            return self.visit(ctx.if_statement())
        if ctx.while_statement():
            return self.visit(ctx.while_statement())
        if ctx.for_statement():
            return self.visit(ctx.for_statement())
        if ctx.break_statement():
            return self.visit(ctx.break_statement())
        if ctx.continue_statement():
            return self.visit(ctx.continue_statement())
        if ctx.return_statement():
            return self.visit(ctx.return_statement())
        if ctx.compound_statement():
            return self.visit(ctx.compound_statement())
        if ctx.with_statement():
            return self.visit(ctx.with_statement())
        if ctx.call_statement():
            return self.visit(ctx.call_statement())

    def visitAssignment_statement(self, ctx:MPParser.Assignment_statementContext):
        if ctx.expression():
            if ctx.ID():
                return [Assign(Id(ctx.ID().getText()),self.visit(ctx.expression()))]
            else:
                return [Assign(self.visit(ctx.element_arr()),self.visit(ctx.expression()))]
        else:
            if ctx.ID():
               
                return self.visit(ctx.assignment_statement()) + [Assign(Id(ctx.ID().getText()),self.visit(ctx.assignment_statement())[-1].lhs)] 
               
            else:
                return self.visit(ctx.assignment_statement()) + [Assign(self.visit(ctx.element_arr()),self.visit(ctx.assignment_statement())[-1].lhs)] 
                




#If_stmt
    def visitIf_statement(self, ctx:MPParser.If_statementContext):
        if ctx.ELSE():
            return [If(self.visit(ctx.expression()) , self.visit(ctx.statement(0)) , self.visit(ctx.statement(1)))]
        else:
            return [If(self.visit(ctx.expression()) , self.visit(ctx.statement(0)))]
            
    
        
#While_stmt
    def visitWhile_statement(self, ctx:MPParser.While_statementContext):
        return [While(self.visit(ctx.expression()) , self.visit(ctx.statement()) )]

#For_stmt
    def visitFor_statement(self, ctx:MPParser.For_statementContext):
        if ctx.TO():
            return [For(Id(ctx.ID().getText()),self.visit(ctx.expression(0)),self.visit(ctx.expression(1)),True,self.visit(ctx.statement()))]
        else:
            return [For(Id(ctx.ID().getText()),self.visit(ctx.expression(0)),self.visit(ctx.expression(1)),False,self.visit(ctx.statement()))]
        
#Break_stmt
    def visitBreak_statement(self, ctx:MPParser.Break_statementContext):
        return [Break()]

#Continue_stmt
    def visitContinue_statement(self, ctx:MPParser.Continue_statementContext):
        return [Continue()]

#Return_stmt
    def visitReturn_statement(self, ctx:MPParser.Return_statementContext):
        if ctx.expression():
            return [Return(self.visit(ctx.expression()))]
        else:
            return [Return()]
#Compound_stmt
    def visitCompound_statement(self, ctx:MPParser.Compound_statementContext):
        return self.visit(ctx.list_statement())
    def visitList_statement(self, ctx:MPParser.List_statementContext):
        if ctx.not_null_list_statement():
            return self.visit(ctx.not_null_list_statement())
        else:
            return []
    def visitNot_null_list_statement(self, ctx:MPParser.Not_null_list_statementContext):
        if ctx.not_null_list_statement():
            return self.visit(ctx.statement()) + self.visit(ctx.not_null_list_statement())
        else:
            return self.visit(ctx.statement())
#With_stmt
    def visitWith_statement(self, ctx:MPParser.With_statementContext):
        return [With(self.visit(ctx.list_decl()),self.visit(ctx.statement()))]
#Call_stmt
    def visitCall_statement(self, ctx:MPParser.Call_statementContext):
        return [CallStmt(Id(ctx.ID().getText()), self.visit(ctx.exp_list()))]
    














