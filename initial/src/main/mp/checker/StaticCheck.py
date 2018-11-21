
"""
 * Nguyen Van Tuong
 * 1614028

"""
from AST import *
from Visitor import *
from Utils import Utils
from StaticError import *
import functools


class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value
        



########## helpFunction
def returnType(sym):
    return Variable() if type(sym) is VarDecl else Procedure() if type(sym.returnType) is VoidType else Function()
        
def checkRedeclared(listDecl, decl, kind):
    if type(kind) in [Parameter, Variable]:
        if any(de.name == decl.variable.name.lower() for de in listDecl):
                raise Redeclared(kind, decl.variable.name)
        return Symbol(decl.variable.name.lower(), decl.varType)
        
    if any(de.name == decl.name.name.lower() for de in listDecl):
        raise Redeclared(kind, decl.name.name)
    
    return Symbol(decl.name.name.lower(), MType([x.varType for x in decl.param], decl.returnType))

def checkAssign(left, right):
    if type(left) is VoidType or type(right) is VoidType:
        return False
    
    if type(left) is ArrayType or type(right) is ArrayType:
        return False
        
    if type(left) is StringType or type(right) is StringType:
        return False
        
    _validAssign = [(BoolType, BoolType), (FloatType, FloatType), (FloatType, IntType), (IntType, IntType)]

    return (type(left), type(right)) in _validAssign

def checkParse(left, right):
    if type(left) is VoidType or type(right) is VoidType:
        return False
        
    if type(left) is ArrayType and type(right) is ArrayType:
        if left.lower != right.lower or\
           left.upper != right.upper or\
           type(left.eleType) != type(right.eleType):
            return False
        return True
        
    _validParse = [(StringType, StringType), (BoolType, BoolType), (FloatType, FloatType), (FloatType, IntType), (IntType, IntType)]
    
    return (type(left), type(right)) in _validParse

def checkOperation(left, right):
    if (type(left), type(right)) == (IntType, IntType):
        return IntType()
    if (type(left), type(right)) in [(IntType, FloatType), (FloatType, IntType), (FloatType, FloatType)]:
        return FloatType()
    return None
    
def overrideDeclaration(ref_env, name):
    [ref_env.remove(id) for id in ref_env if id.name == name.lower()]
    
class StaticChecker(BaseVisitor,Utils):

    global_envi = [Symbol("getint",MType([],IntType())),
    			   Symbol("putintln",MType([IntType()],VoidType())),
                   Symbol("putint", MType([IntType()], VoidType())),
                   Symbol("getfloat", MType([], FloatType())),
                   Symbol("putfloat", MType([FloatType()], VoidType())),
                   Symbol("putfloatln", MType([FloatType()], VoidType())),
                   Symbol("putbool", MType([BoolType()], VoidType())),
                   Symbol("putboolln", MType([BoolType()], VoidType())),
                   Symbol("putstring", MType([StringType()], VoidType())),
                   Symbol("putstringln", MType([StringType()], VoidType())),
                   Symbol("putln", MType([], VoidType()))]

                   
    def __init__(self,ast):
        self.ast = ast

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)




    #################### Visitor
    def visitProgram(self,ast, c):
        _env = c.copy()
        _returnType = None
        _isLoop = False
        _reachableFunctions = {}
        _mainCall = None
        
        _entryPoint = False
        
        for decl in ast.decl:
            _env.append(checkRedeclared(_env, decl, returnType(decl)))
            if type(decl) is FuncDecl:
                if not _entryPoint:
                    _entryPoint = (decl.name.name.lower() == "main" and type(decl.returnType) is VoidType and decl.param == [])
                _reachableFunctions[decl.name.name.lower()] = decl.name.name.lower() == "main"

        if not _entryPoint:
            raise NoEntryPoint()
        
        for decl in ast.decl:
            if not type(decl) is VarDecl:
                self.visit(decl, (_env, _returnType, _isLoop, _reachableFunctions, _mainCall))
                
        for func in _reachableFunctions:
            if not _reachableFunctions[func]:
                _func = self.lookup(func.lower(), _env, lambda x: x.name)
                ftype = Procedure() if type(_func.mtype.rettype) is VoidType else Function()
                raise Unreachable(ftype, func)
        
        return None
        


    def visitVarDecl(self, ast, c):
        _local = c[0]
        _type = c[1]
        _ref_env = c[2]
        _local.append(checkRedeclared(_local, ast, c[1]))
        overrideDeclaration(_ref_env, ast.variable.name)
        return None


        

    def visitFuncDecl(self, ast, c):
        _ref_env = c[0].copy()
        _returnType = ast.returnType
        _mainCall = ast.name.name
        _isEnd = 0
        
        _local = []
        [self.visit(param, (_local, Parameter(), _ref_env)) for param in ast.param]
        [self.visit(local, (_local, Variable(), _ref_env)) for local in ast.local]
        
        _ref_env += _local
        
        _isEnd = self.visitBlock(ast.body, (_ref_env, _returnType, c[2], c[3], _mainCall))
        
        if _isEnd != 1 and not type(_returnType) is VoidType:
            raise FunctionNotReturn(ast.name.name)
            
        return None
        

        
    def visitBlock(self, ls, c):
        _isEnd = 0
        
        for stmt in ls:
            if _isEnd:
                raise UnreachableStatement(stmt)
            _isEnd = self.visit(stmt, c)
        
        return _isEnd
        


    def visitAssign(self, ast, c):
        _ref_env = c[0].copy()
        
        if not type(ast.lhs) in [Id, ArrayCell]:
            raise TypeMismatchInStatement(ast)
        
        _lhsType = self.visit(ast.lhs, (_ref_env, c[1], c[2], c[3], c[4]))
        _rhsType = self.visit(ast.exp, (_ref_env, c[1], c[2], c[3], c[4]))
        
        if not checkAssign(_lhsType, _rhsType):
            raise TypeMismatchInStatement(ast)

        return 0

    def visitIf(self, ast, c):
        _ref_env = c[0].copy()
        
        _exp = self.visit(ast.expr, (_ref_env, c[1], c[2], c[3], c[4]))
        if not type(_exp) is BoolType:
            raise TypeMismatchInStatement(ast)

        _isEndT = self.visitBlock(ast.thenStmt, (_ref_env, c[1], c[2], c[3], c[4]))
        _isEndE = self.visitBlock(ast.elseStmt, (_ref_env, c[1], c[2], c[3], c[4]))
        
        if _isEndT == 1 and _isEndE == 1:
            return 1
        if _isEndT != 0 and _isEndE != 0:
            return 2
        return 0
        
    def visitWhile(self, ast, c):
        _ref_env = c[0].copy()
        _exp = self.visit(ast.exp, (_ref_env, c[1], True, c[3], c[4]))
        if not type(_exp) is BoolType:
            raise TypeMismatchInStatement(ast)
            
        _isEnd = self.visitBlock(ast.sl, (_ref_env, c[1], True, c[3], c[4]))
        
        return 0
        
    def visitFor(self, ast, c):
        _ref_env = c[0].copy()

        _id = self.visit(ast.id, (_ref_env, c[1], c[2], c[3], c[4]))
        if not type(_id) is IntType:
            raise TypeMismatchInStatement(ast)

        _exp1 = self.visit(ast.expr1, (_ref_env, c[1], c[2], c[3], c[4]))
        if not type(_exp1) is IntType:
            raise TypeMismatchInStatement(ast)

        _exp2 = self.visit(ast.expr2, (_ref_env, c[1], c[2], c[3], c[4]))
        if not type(_exp2) is IntType:
            raise TypeMismatchInStatement(ast)

        _isEnd = self.visitBlock(ast.loop, (_ref_env, c[1], True, c[3], c[4]))
        
        return 0
        
    def visitBreak(self, ast, c):
        _isLoop = c[2]
        
        if not _isLoop:
            raise BreakNotInLoop()
            
        return 2
        
    def visitContinue(self, ast, c):
        _isLoop = c[2]
        
        if not _isLoop:
            raise ContinueNotInLoop()
        
        return 2
        
    def visitReturn(self, ast, c):
        _ref_env = c[0].copy()
        _returnType = c[1]
        
        if ast.expr is None:
            if type(_returnType) is VoidType:
                return 1
            raise TypeMismatchInStatement(ast)
        
        if checkParse(_returnType, self.visit(ast.expr, (_ref_env, c[1], c[2], c[3], c[4]))):
            return 1
        raise TypeMismatchInStatement(ast)
        
    def visitWith(self, ast, c):
        _ref_env = c[0].copy()
        
        _local = []
        for decl in ast.decl:
            _local.append(checkRedeclared(_local, decl, Variable()))
            overrideDeclaration(_ref_env, decl.variable.name)
        _ref_env += _local
        
        _isEnd = 0
        for stmt in ast.stmt:
            if _isEnd != 0:
                raise UnreachableStatement(stmt)
            _isEnd = self.visit(stmt, (_ref_env, c[1], c[2], c[3], c[4]))
        return _isEnd
        
    def visitCallBody(self, ast, c):
        _ref_env = c[0].copy()
        _mainCall = c[4]
        _type = c[5]
        
        _param = [self.visit(x, (_ref_env, c[1], c[2], c[3], c[4])) for x in ast.param]
        _func = self.lookup(ast.method.name.lower(), _ref_env, lambda x: x.name)

        if _func is None or not type(_func.mtype) is MType:
            raise Undeclared(c[5], ast.method.name)

        if (not type(_func.mtype.rettype) is VoidType and type(c[5]) is Procedure) or (type(_func.mtype.rettype) is VoidType and type(c[5]) is Function):
            raise Undeclared(c[5], ast.method.name)

        if len(_func.mtype.partype) != len(_param):
            if type(c[5]) is Procedure:
                raise TypeMismatchInStatement(ast)
            raise TypeMismatchInExpression(ast)
        
        if not all([checkParse(_func.mtype.partype[i], _param[i]) for i in range(len(_param))]):
            if type(c[5]) is Procedure:
                raise TypeMismatchInStatement(ast)
            raise TypeMismatchInExpression(ast)
            
        
        if _mainCall.lower() != ast.method.name.lower():
            c[3][ast.method.name.lower()] = True
        
        return _func.mtype.rettype
        
    def visitCallStmt(self, ast, c):
        self.visitCallBody(ast, (c[0], c[1], c[2], c[3], c[4], Procedure()))
        return 0

    def visitBinaryOp(self, ast, c):
        _ref_env = c[0].copy()
        
        leftType = self.visit(ast.left, (_ref_env, c[1], c[2], c[3], c[4]))
        rightType = self.visit(ast.right, (_ref_env, c[1], c[2], c[3], c[4]))
        op = ast.op
        
        if op in ["+", "-", "*"]:
            rtype = checkOperation(leftType, rightType)
            if rtype is None:
                raise TypeMismatchInExpression(ast)
            return rtype
            
        if op == "/":
            rtype = checkOperation(leftType, rightType)
            if rtype is None:
                raise TypeMismatchInExpression(ast)
            return FloatType()
            
        if op in ["<", ">", "<=", ">=", "=", "<>"]:
            rtype = checkOperation(leftType, rightType)
            if rtype is None:
                raise TypeMismatchInExpression(ast)
            return BoolType()
            
        if op.lower() in ["and", "or", "andthen", "orelse"]:
            if (type(leftType), type(rightType)) == (BoolType, BoolType):
                return BoolType()
            raise TypeMismatchInExpression(ast)
            
        if op.lower() in ["div", "mod"]:
            if (type(leftType), type(rightType)) == (IntType, IntType):
                return IntType()
            raise TypeMismatchInExpression(ast)
            
        raise TypeMismatchInExpression(ast)
        
    def visitUnaryOp(self, ast, c):
        _ref_env = c[0].copy()
        expType = self.visit(ast.body, (_ref_env, c[1], c[2], c[3], c[4]))
        op = ast.op
        if op == "-":
            if type(expType) in [IntType, FloatType]:
                return expType
            raise TypeMismatchInExpression(ast)
        if op.lower() == "not":
            if type(expType) is BoolType:
                return BoolType()
            raise TypeMismatchInExpression(ast)
        
        raise TypeMismatchInExpression(ast)

    def visitCallExpr(self, ast, c):
        ret = self.visitCallBody(ast, (c[0], c[1], c[2], c[3], c[4], Function()))
        return ret

    def visitId(self, ast, c):
        _ref_env = c[0].copy()
        id = self.lookup(ast.name.lower(), _ref_env, lambda x: x.name)
        if id is None or type(id.mtype) is MType:
            raise Undeclared(Identifier(), ast.name)
        return id.mtype
        
    def visitArrayCell(self, ast, c):
        _ref_env = c[0].copy()
        
        if not type(ast.arr) is Id and not type(ast.arr) is CallExpr:
            raise TypeMismatchInExpression(ast)
        
        _arr = self.lookup(ast.arr.name.lower() if type(ast.arr) is Id else ast.arr.method.name, _ref_env, lambda x: x.name)
        if _arr is None:
            if type(ast.arr) is Id:
                raise Undeclared(Identifier(), ast.arr.name)
            else:
                raise Undeclared(Function(), ast.arr.method.name)
        
        _idx = self.visit(ast.idx, (_ref_env, c[1], c[2], c[3], c[4]))
        
        if not type(_idx) is IntType:
            raise TypeMismatchInExpression(ast)
        
        if type(_arr.mtype) is MType:
            if (c[4]):
                c[3][_arr.name.lower()] = True
            return _arr.mtype.rettype.eleType
        
        if not type(_arr.mtype) is ArrayType:
            raise TypeMismatchInExpression(ast)
        
        return _arr.mtype.eleType
        
    def visitIntLiteral(self,ast, c):
        return IntType()

    def visitFloatLiteral(self, ast, c):
        return FloatType()

    def visitStringLiteral(self, ast, c):
        return StringType()

    def visitBooleanLiteral(self, ast, c):
        return BoolType()
        