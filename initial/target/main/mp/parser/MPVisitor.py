# Generated from main/mp/parser/MP.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MPParser import MPParser
else:
    from MPParser import MPParser

# This class defines a complete generic visitor for a parse tree produced by MPParser.

class MPVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MPParser#program.
    def visitProgram(self, ctx:MPParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#many_declarations.
    def visitMany_declarations(self, ctx:MPParser.Many_declarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#declarations.
    def visitDeclarations(self, ctx:MPParser.DeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#var_decl.
    def visitVar_decl(self, ctx:MPParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#list_decl.
    def visitList_decl(self, ctx:MPParser.List_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#decl.
    def visitDecl(self, ctx:MPParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#list_id.
    def visitList_id(self, ctx:MPParser.List_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#func_decl.
    def visitFunc_decl(self, ctx:MPParser.Func_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#param_list.
    def visitParam_list(self, ctx:MPParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#not_null_param_list.
    def visitNot_null_param_list(self, ctx:MPParser.Not_null_param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#param_decl.
    def visitParam_decl(self, ctx:MPParser.Param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#proc_decl.
    def visitProc_decl(self, ctx:MPParser.Proc_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#types.
    def visitTypes(self, ctx:MPParser.TypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#primitive_types.
    def visitPrimitive_types(self, ctx:MPParser.Primitive_typesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#compound_types.
    def visitCompound_types(self, ctx:MPParser.Compound_typesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#array_types.
    def visitArray_types(self, ctx:MPParser.Array_typesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#operand.
    def visitOperand(self, ctx:MPParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression.
    def visitExpression(self, ctx:MPParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression_1.
    def visitExpression_1(self, ctx:MPParser.Expression_1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression_2.
    def visitExpression_2(self, ctx:MPParser.Expression_2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression_3.
    def visitExpression_3(self, ctx:MPParser.Expression_3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression_4.
    def visitExpression_4(self, ctx:MPParser.Expression_4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression_5.
    def visitExpression_5(self, ctx:MPParser.Expression_5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression_6.
    def visitExpression_6(self, ctx:MPParser.Expression_6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#element_arr.
    def visitElement_arr(self, ctx:MPParser.Element_arrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#func_call.
    def visitFunc_call(self, ctx:MPParser.Func_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp_list.
    def visitExp_list(self, ctx:MPParser.Exp_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#not_null_exp_list.
    def visitNot_null_exp_list(self, ctx:MPParser.Not_null_exp_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#statement.
    def visitStatement(self, ctx:MPParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#assignment_statement.
    def visitAssignment_statement(self, ctx:MPParser.Assignment_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#if_statement.
    def visitIf_statement(self, ctx:MPParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#while_statement.
    def visitWhile_statement(self, ctx:MPParser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#for_statement.
    def visitFor_statement(self, ctx:MPParser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#break_statement.
    def visitBreak_statement(self, ctx:MPParser.Break_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#continue_statement.
    def visitContinue_statement(self, ctx:MPParser.Continue_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#return_statement.
    def visitReturn_statement(self, ctx:MPParser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#compound_statement.
    def visitCompound_statement(self, ctx:MPParser.Compound_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#list_statement.
    def visitList_statement(self, ctx:MPParser.List_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#not_null_list_statement.
    def visitNot_null_list_statement(self, ctx:MPParser.Not_null_list_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#with_statement.
    def visitWith_statement(self, ctx:MPParser.With_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#call_statement.
    def visitCall_statement(self, ctx:MPParser.Call_statementContext):
        return self.visitChildren(ctx)



del MPParser