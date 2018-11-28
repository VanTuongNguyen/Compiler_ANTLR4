'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
 *   @Student : Nguyen Van Tuong
 *   @ID      : 1614028
'''

from AST import *
from Visitor import *
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod
from CodeGenError import *
from functools import reduce

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [    Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
                    Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("getFloat", MType([], FloatType()), CName(self.libName)),
                    Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("putBool", MType([BoolType()], VoidType()), CName(self.libName)),
                    Symbol("putBoolLn", MType([BoolType()], VoidType()), CName(self.libName)),
                    Symbol("putString", MType([StringType()], VoidType()), CName(self.libName)),
                    Symbol("putStringLn", MType([StringType()], VoidType()), CName(self.libName)),
                    Symbol("putLn", MType([], VoidType()), CName(self.libName)),
                    ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

# class StringType(Type):
    
#     def __str__(self):
#         return "StringType"

#     def accept(self, v, param):
#         return None

class ArrayPointerType(Type):
    def __init__(self, ctype):
        #cname: String
        self.eleType = ctype

    def __str__(self):
        return "ArrayPointerType({0})".format(str(self.eleType))

    def accept(self, v, param):
        return None
        
class ClassType(Type):
    def __init__(self,cname):
        self.cname = cname
    def __str__(self):
        return "Class({0})".format(str(self.cname))
    def accept(self, v, param):
        return None

# use in Function Body
class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym

# use in Expression Body
class Access():
    def __init__(self, frame, sym, isLeft, isFirst):
        #frame: Frame
        #sym: List[Symbol]
        #isLeft: Boolean
        #isFirst: Boolean
        #isDup :Boolean
        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst
        
class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value

class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File

        self.astTree = astTree
        self.env = env
        self.className = "MPClass"
        self.path = dir_
        self.emit = Emitter(self.path + "/" + self.className + ".j")
        self.curFunc = Symbol("null", MType([],VoidType()), CName("MCClass"))

    def VarGlobal(self, ast, c):
        ctxt = c
        nameAtt = ast.variable.name
        typeAtt = ast.varType
        self.emit.printout(self.emit.emitATTRIBUTE(nameAtt, typeAtt, False, ""))
        symbol = Symbol(ast.variable.name, typeAtt, CName(self.className))
        c.append(symbol)
        return c
    
    def FuncGlobal(self,ast, c):
        ctxt = c
        nameFunc = ast.name.name
        typeFunc = MType([x.varType for x in ast.param], ast.returnType)
        symbol = Symbol(nameFunc, typeFunc, CName(self.className))
        c.append(symbol)
        return c
    
    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any

        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        lsVar       = list(filter(lambda x:type(x) is VarDecl, ast.decl))
        lsArrayVar  = list(filter(lambda x:type(x.varType) is ArrayType, lsVar))
        lsFun       = list(filter(lambda x:type(x) is FuncDecl, ast.decl))
        
        
        for x in lsVar:
            self.env = self.VarGlobal(x,self.env)
            
        for x in lsFun:
            self.env = self.FuncGlobal(x,self.env)

        # visit func decl
        reduce(lambda a,b: self.visit(b,a), lsFun, SubBody(None, self.env))

        # generate default constructor
        self.genMETHOD(FuncDecl(Id("<init>"), list(), list(), list(),None), c, Frame("<init>", VoidType))
        
        # generate code for global array
        if lsArrayVar:
            self.emit.printout(self.emit.emitCLINIT(self.className, lsArrayVar, Frame("<clinit>", VoidType())))
        
        self.emit.emitEPILOG()
        return c

    def visitVarDecl(self,ast,c):
        #ast: VarDecl
        #c  : SubBody
        env  = c.sym if type(c) is SubBody else []
        indx = c.frame.getNewIndex()
        #.var
        self.emit.printout(self.emit.emitVAR(indx, ast.variable.name, ast.varType, c.frame.getStartLabel(), c.frame.getEndLabel(), c.frame))
        return SubBody(c.frame, [Symbol(ast.variable.name, ast.varType, Index(indx))] + env)

    #print code gen newarray
    def arrayTypeDecl(self,ast,c):
        #ast : VarDecl
        #c   : any

        index = (self.lookup(ast.variable.name,c.sym,lambda x:x.name)).value.value
        self.emit.printout(self.emit.emitNEWARRAY(ast.varType, c.frame))
        self.emit.printout(self.emit.emitWRITEVAR(ast.variable.name, ast.varType, index, c.frame))
        return SubBody(c.frame, c.sym)


    # gen code for method
    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame

        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayPointerType(StringType())] if isMain else [x.varType for x in consdecl.param]
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))

        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        # param decl other functions
        funcSubBody = SubBody(frame,glenv)
        if intype != [] :
            funcSubBody = reduce(lambda a,b: self.visit(b,a), consdecl.param, funcSubBody) 
        # variables decl in local
        if consdecl.local != []:
            funcSubBody = reduce(lambda a,b: self.visit(b,a), consdecl.local, funcSubBody) 
        
        

        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        
        #gen code for local array
        lsArrVarDecl = list(filter(lambda x:type(x.varType) is ArrayType, consdecl.param))
        lsArrVarDecl += list(filter(lambda x:type(x.varType) is ArrayType, consdecl.local))
        for x in lsArrVarDecl:
            self.arrayTypeDecl(x,funcSubBody)
        
        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        
        body = consdecl.body

        # list(map(lambda x: self.visit(x, funcSubBody), body))
        for x in body:
            self.visit(x,funcSubBody)

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def visitFuncDecl(self, ast, o):
        #ast: FuncDecl
        #o: Any

        subctxt = o
        frame = Frame(ast.name, ast.returnType)
        self.curFunc = self.lookup(ast.name.name, subctxt.sym, lambda x: x.name)
        self.genMETHOD(ast, subctxt.sym, frame)
        #return SubBody(None, [Symbol(ast.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym)
        return o

    # def visitAssign(self, ast, c):
    #     #c  : Access (co the la SubBody)
    #     ctxt = c
    #     frame = ctxt.frame
    #     env = ctxt.sym
    #     assign_Str = ""
    #     str_Dup = "" 
    #     resType = None

    #     (resLeft, typeLeft) = self.visit(ast.lhs,Access(frame,env,True,))


    def visitBinaryOp(self,ast,c):
        #c : Access
        ctxt = c
        frame = ctxt.frame
        env = ctxt.sym

        op = ast.op
        op_Str = ""
        str_Dup = "" 
        str_I2f = "" 
        resType = IntType()

        (resLeft, typeLeft) = self.visit(ast.left,Access(frame,env,True,False))
        (resRight, typeRight) = self.visit(ast.right,Access(frame,env,False,False))
        if op == "+" or op == "-":
            if type(typeLeft) is FloatType and type(typeRight) is IntType:
                op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitADDOP(op,FloatType(),frame)
                resType = FloatType()
            elif type(typeLeft) is IntType and type(typeRight) is FloatType:
                op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitADDOP(op, FloatType(), frame)
                resType = FloatType()
            else:
                op_Str = resLeft + resRight + self.emit.emitADDOP(op, typeLeft, frame)
                resType = typeLeft
        elif op == "*":
            if type(typeLeft) is FloatType and type(typeRight) is IntType:
                op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
                resType = FloatType()
            elif type(typeLeft) is IntType and type(typeRight) is FloatType:
                op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitMULOP(op, FloatType(), frame)
                resType = FloatType()
            else:
                op_Str = resLeft + resRight + self.emit.emitMULOP(op, typeLeft, frame)
                resType = typeLeft

        elif op == "/":
            if type(typeLeft) is FloatType and type(typeRight) is IntType:
                op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
                
            elif type(typeLeft) is IntType and type(typeRight) is FloatType:
                op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitMULOP(op, FloatType(), frame)
            elif type(typeLeft) is IntType and type(typeRight) is IntType:
                op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
            else:
                op_Str = resLeft + resRight + self.emit.emitMULOP(op, typeLeft, frame)
            resType = FloatType()
        elif op == "div":
            op_Str = resLeft + resRight + self.emit.emitDIV(frame)
        elif op == "mod": 
            op_Str = resLeft + resRight + self.emit.emitMOD(frame)
            resType = IntType()

        elif (op == "<") or (op == "<=") or (op == ">") or (op == ">="): 
            if type(typeLeft) is FloatType and type(typeRight) is IntType:
                op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitREOP(op, FloatType(), frame)
            elif type(typeLeft) is IntType and type(typeRight) is FloatType:
                op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitREOP(op, FloatType(), frame)
            else:
                op_Str = resLeft + resRight + self.emit.emitREOP(op, typeLeft, frame)
            resType = BoolType()
        elif (op == "=") or (op == "<>"): 
            op_Str = resLeft + resRight + self.emit.emitREOP(op, IntType(), frame)
            resType = BoolType()
        elif (op == "and") or (op == "or"): 
            op_Str = self.emit.emitAND_OR_SHORT_CIRCUIT(op, resLeft, resRight, frame)
            resType = BoolType()
        return (op_Str,resType)

    def visitUnaryOp(self,ast,c):
        ctxt = c
        frame = ctxt.frame
        env = ctxt.sym
        (resExpr, typeExpr) = self.visit(ast.body, Access(frame, env, False, True))
        if ast.op == "not":
            return (resExpr + self.emit.emitNOT(typeExpr, frame), typeExpr)
        elif ast.op == "-": 
            return (resExpr + self.emit.emitNEGOP(typeExpr, frame), typeExpr)


    def visitIf(self, ast, c):
        # c: SubBody

        frame = c.frame
        env = c.sym
        ( resExpr , typeExpr) = self.visit(ast.expr,Access(frame,env,False,True))
        falseLabel = frame.getNewLabel()

        self.emit.printout(resExpr + self.emit.emitIFFALSE(falseLabel,frame))
        for x in ast.thenStmt:
            self.visit(x,c)
        if not ast.elseStmt:
            self.emit.printout(self.emit.emitLABEL(falseLabel,frame))
        else:
            trueLabel = frame.getNewLabel()
            self.emit.printout(self.emit.emitGOTO(trueLabel, frame) + self.emit.emitLABEL(falseLabel, frame))
            for x in ast.elseStmt:
                self.visit(x,c)
            self.emit.printout(self.emit.emitLABEL(trueLabel, frame))

    def visitWhile(self,ast,c):
        # c: SubBody
        frame = c.frame
        env = c.sym
        beginLabel = frame.getNewLabel()
        
        frame.enterLoop()
        self.emit.printout(self.emit.emitLABEL(beginLabel,frame))
        (resExpr , typeExpr) = self.visit(ast.exp,Access(frame,env,False,True))
        self.emit.printout(resExpr)
        
        self.emit.printout(self.emit.emitIFFALSE(frame.getBreakLabel(),frame))
        for x in ast.sl:
            self.visit(x,c)
        self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
        self.emit.printout(self.emit.emitGOTO(beginLabel,frame))
        self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))
        frame.exitLoop()

    def visitBreak(self,ast,c):
        self.emit.printout(self.emit.emitGOTO(c.frame.getBreakLabel(), c.frame))
    def visitContinue(self,ast,c):
        self.emit.printout(self.emit.emitGOTO(c.frame.getContinueLabel(), c.frame))
    def visitReturn(self,ast,c):
        if ast.expr:
            (resExpr,resType) = self.visit(ast.expr, Access(c.frame,c.sym,False,True))
            print(resExpr,resType,self.curFunc.mtype.rettype)
            typeFunc = self.curFunc.mtype.rettype
            if type(typeFunc) == FloatType and type(resType) == IntType:
                self.emit.printout(resExpr + self.emit.emitI2F(c.frame) + self.emit.emitRETURN(FloatType(),c.frame))
            else:
                self.emit.printout(resExpr + self.emit.emitRETURN(resType,c.frame))
        else:
            self.emit.emitRETURN(VoidType(),c.frame)

    def visitCallExpr(self,ast,o):
        
        ctxt = o
        frame = ctxt.frame
        env = ctxt.sym
        sym = self.lookup(ast.method.name,env,lambda x: x.name)
        cname = sym.value.value
        ctype = sym.mtype
        returnType = ctype.rettype

        if ctxt.isLeft is True and ctxt.isFirst is False:
            return (self.emit.emitWRITEVAR2())
    def visitCallStmt(self, ast, o):
        #ast: CallStmt
        #o: Any
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
    
        ctype = sym.mtype

        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

    def visitIntLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any

        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(ast.value, frame), IntType()

    def visitFloatLiteral(self, ast, o):
        #ast: FloatLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHFCONST(str(ast.value), frame), FloatType()

    def visitStringLiteral(self, ast, o):
        #ast: StringLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHCONST(ast.value, StringType(), frame), StringType()

    def visitBooleanLiteral(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        return (self.emit.emitPUSHICONST(str(ast.value), frame), BoolType())
