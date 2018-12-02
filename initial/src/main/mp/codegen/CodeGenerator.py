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
from CodeGenError import *
from functools import reduce

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"
        self.curFunc = Symbol("null", MType([], VoidType()), CName("MPClass"))

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
    def __init__(self, frame, sym, isLeft, isFirst, isDup = False):
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
        
        index = (self.lookup(ast.variable.name.lower(),c.sym,lambda x:x.name.lower())).value.value
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
        if (isMain is False) and intype != [] :
            funcSubBody = reduce(lambda a,b: self.visit(b,a), consdecl.param, funcSubBody) 
        # variables decl in local
        if consdecl.local != []:
            funcSubBody = reduce(lambda a,b: self.visit(b,a), consdecl.local, funcSubBody) 
        
        

        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        
        #gen code for local array
        # lsArrVarDecl = list(filter(lambda x:type(x.varType) is ArrayType, consdecl.param))
        lsArrVarDecl = list(filter(lambda x:type(x.varType) is ArrayType, consdecl.local))
        for x in lsArrVarDecl:
            self.arrayTypeDecl(x,funcSubBody)
        
        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        
        body = consdecl.body
        returnStmt = list(filter(lambda x:type(x) is Return, consdecl.body))

        # list(map(lambda x: self.visit(x, funcSubBody), body))
        for x in body:
            self.visit(x,funcSubBody)

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if (type(returnType) is VoidType) or (not returnStmt):      
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


    

    # def visitBinaryOp(self,ast,c):
    #     #c : Access
    #     ctxt = c
    #     frame = ctxt.frame
    #     env = ctxt.sym

    #     op = ast.op.lower()
    #     op_Str = ""
    #     resType = IntType()

        
    #     (resLeft, typeLeft) = self.visit(ast.left,Access(frame,env,False,True))
    #     (resRight, typeRight) = self.visit(ast.right,Access(frame,env,False,True))
        
        
    #     if op == "+" or op == "-":
    #         if type(typeLeft) is FloatType and type(typeRight) is IntType:
    #             op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitADDOP(op,FloatType(),frame)
    #             resType = FloatType()
    #         elif type(typeLeft) is IntType and type(typeRight) is FloatType:
    #             op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitADDOP(op, FloatType(), frame)
    #             resType = FloatType()
    #         else:
    #             op_Str = resLeft + resRight + self.emit.emitADDOP(op, typeLeft, frame)
    #             resType = typeLeft
    #     if op == "*":
    #         if type(typeLeft) is FloatType and type(typeRight) is IntType:
    #             op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
    #             resType = FloatType()
    #         elif type(typeLeft) is IntType and type(typeRight) is FloatType:
    #             op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitMULOP(op, FloatType(), frame)
    #             resType = FloatType()
    #         else:
    #             op_Str = resLeft + resRight + self.emit.emitMULOP(op, typeLeft, frame)
    #             resType = typeLeft

    #     if op == "/":
    #         if type(typeLeft) is FloatType and type(typeRight) is IntType:
    #             op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
                
    #         elif type(typeLeft) is IntType and type(typeRight) is FloatType:
    #             op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitMULOP(op, FloatType(), frame)
    #         elif type(typeLeft) is IntType and type(typeRight) is IntType:
    #             op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
    #         else:
    #             op_Str = resLeft + resRight + self.emit.emitMULOP(op, typeLeft, frame)
    #         resType = FloatType()
    #     if op == "div":
    #         op_Str = resLeft + resRight + self.emit.emitDIV(frame)
    #     if op == "mod": 
    #         op_Str = resLeft + resRight + self.emit.emitMOD(frame)
    #         resType = IntType()

    #     if (op == "<") or (op == "<=") or (op == ">") or (op == ">="): 
    #         if type(typeLeft) is FloatType and type(typeRight) is IntType:
    #             op_Str = resLeft + resRight + self.emit.emitI2F(frame) + self.emit.emitREOP(op, FloatType(), frame)
    #         elif type(typeLeft) is IntType and type(typeRight) is FloatType:
    #             op_Str = resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitREOP(op, FloatType(), frame)
    #         else:
    #             op_Str = resLeft + resRight + self.emit.emitREOP(op, typeLeft, frame)
    #         resType = BoolType()
    #     if (op == "=") or (op == "<>"): 
    #         op_Str = resLeft + resRight + self.emit.emitREOP(op, IntType(), frame)
    #         resType = BoolType()
    #     if (op == "andthen") or (op == "orelse"): 
    #         op_Str = self.emit.emitAND_OR_SHORT_CIRCUIT(op, resLeft, resRight, frame)
    #         resType = BoolType()
    #     if op == "and":
    #         op_Str = resLeft + resRight + self.emit.emitANDOP(frame)
    #         resType = BoolType()
    #     if op == "or":
    #         op_Str = resLeft + resRight + self.emit.emitOROP(frame)
    #         resType = BoolType()
    #     return (op_Str,resType)
    def genBinExpr(self, frame, resLeft, typeLeft, resRight, typeRight, isFloat = False):
        if type(typeLeft) is FloatType and type(typeRight) is IntType:
            return resLeft + resRight + self.emit.emitI2F(frame), FloatType()
        if type(typeLeft) is IntType and type(typeRight) is FloatType:
            return resLeft + self.emit.emitI2F(frame) + resRight, FloatType()
        if isFloat and type(typeLeft) is IntType:
            return resLeft + self.emit.emitI2F(frame) + resRight + self.emit.emitI2F(frame), FloatType()
        return resLeft + resRight, typeLeft

    def visitBinaryOp(self, ast, c):
        _frame = c.frame
        _sym = c.sym
        op = ast.op
        (resLeft, typeLeft) = self.visit(ast.left, Access(_frame, _sym, False, True, True))
        (resRight, typeRight) = self.visit(ast.right, Access(_frame, _sym, False, True, True))
        
        if op == "/":
            _exp, _type = self.genBinExpr(_frame, resLeft, typeLeft, resRight, typeRight, True)
            _op = self.emit.emitMULOP(op, FloatType(), _frame)
            _string = _exp + _op
            return _string, _type
            
        _exp, _type = self.genBinExpr(_frame, resLeft, typeLeft, resRight, typeRight)
        if op in ["andthen", "orelse"]: 
            _string = self.emit.emitAND_OR_SHORT_CIRCUIT(op, resLeft, resRight, _frame)
            return _string, _type
            
        if op in ["+", "-"]:
            _op = self.emit.emitADDOP(op, _type, _frame)
        elif op == "*":
            _op = self.emit.emitMULOP(op, _type, _frame)
        elif op.lower() == "div":
            _op = self.emit.emitDIV(_frame)
        elif op.lower() == "mod":
            _op = self.emit.emitMOD(_frame)
        elif op in ["<", "<=", ">", ">="]:
            _op = self.emit.emitREOP(op, _type, _frame)
            _type = BoolType()
        elif op in ["=", "<>"]:
            _op = self.emit.emitREOP(op, _type, _frame)
            _type = BoolType()
        elif op.lower() == "and":
            _op = self.emit.emitANDOP(_frame)
            _type = BoolType()
        elif op.lower() == "or":
            _op = self.emit.emitOROP(_frame)
            _type = BoolType()
        _string = _exp + _op   
        
        return _string, _type

    def visitUnaryOp(self,ast,c):
        ctxt = c
        frame = ctxt.frame
        env = ctxt.sym
        (resExpr, typeExpr) = self.visit(ast.body, Access(frame, env, False, True))
        
        if ast.op == "not":
            return (resExpr + self.emit.emitNOT(BoolType(), frame), BoolType())
        elif ast.op == "-": 
            return (resExpr + self.emit.emitNEGOP(typeExpr, frame), typeExpr)

    def visitCallExpr(self, ast, c):
        ctxt = c
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name.lower(), nenv, lambda x: x.name.lower())
        cname = sym.value.value
        ctype = sym.mtype
        returnType = ctype.rettype
        
        if ctxt.isLeft and not ctxt.isFirst:
            return self.emit.emitWRITEVAR2(ast.method.name, returnType, frame), returnType
            
        listParamType = ctype.partype
        checkList = []
        for item in range(len(listParamType)):
            checkList.append((ast.param[item], listParamType[item]))
            
        in_ = ("", [])
        
        for x in checkList:
            (str1, typ1) = self.visit(x[0], Access(frame, nenv, False, True, True))
            if type(x[1]) is ArrayType:
                str1 += self.emit.emitCLONE(typ1) + self.emit.emitCHECKCAST(typ1)
            if type(typ1) is IntType and type(x[1]) is FloatType:
                in_ = (in_[0] + str1 + self.emit.emitI2F(frame), in_[1] + [typ1])
            else:
                in_ = (in_[0] + str1, in_[1] + [typ1])
                
        return in_[0] + self.emit.emitINVOKESTATIC(cname + "/" + sym.name, ctype, frame), returnType
    
    def visitId(self, ast, c):
        if type(c) != SubBody:
            sym = self.lookup(ast.name.lower(), c.sym, lambda x: x.name.lower())
            code = ""
            if c.isLeft is True and c.isFirst is True:
                pass
            elif c.isLeft is True and c.isFirst is False:
                if type(sym.mtype) is ArrayType or type(sym.mtype) is ArrayPointerType:
                    code = self.emit.emitWRITEVAR2(sym.name, sym.mtype, c.frame)
                else:
                    if type(sym.value) is CName:
                        code = self.emit.emitPUTSTATIC(sym.value.value + "." + sym.name, sym.mtype, c.frame)
                    elif type(sym.value) is Index:
                        code = self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, c.frame)
            elif c.isLeft is False:
                if type(sym.value) is CName:
                    code = self.emit.emitGETSTATIC(sym.value.value + "." + sym.name, sym.mtype, c.frame)
                elif type(sym.value) is Index:
                    code = self.emit.emitREADVAR(ast, sym.mtype, sym.value.value, c.frame)
            return code, sym.mtype
        else:
            sym = self.lookup(ast.name.lower(), c.sym, lambda x: x.name.lower())
            return ("", sym.mtype)
    def visitArrayCell(self, ast, c):
        if type(c) != SubBody:
            frame = c.frame
            lsSym = c.sym

            arrt = self.lookup(ast.arr.method.name.lower() if type(ast.arr) is CallExpr else ast.arr.name.lower(), lsSym, lambda x: x.name.lower())
            lw = int(arrt.mtype.rettype.lower) if type(arrt.mtype) is MType else int(arrt.mtype.lower)

            if c.isLeft is True and c.isFirst is True:
                (resArr, typeArr) = self.visit(ast.arr, Access(frame, lsSym, False, True, False))
                if lw >= 0:
                    (resIdx, typIdx) = self.visit(BinaryOp("-", ast.idx, IntLiteral(lw)), Access(frame, lsSym, False, True, True))
                else:
                    (resIdx, typIdx) = self.visit(BinaryOp("+", ast.idx, IntLiteral(- lw)), Access(frame, lsSym, False, True, True))
                return (resArr + resIdx, typeArr.eleType)
            
            elif c.isLeft is True and c.isFirst is False:
                (resArr, typeArr) = self.visit(ast.arr, Access(frame, lsSym, True, False, False))
                return (resArr, typeArr)
            
            elif c.isLeft is False:
                (resArr, typeArr) = self.visit(ast.arr, Access(frame, lsSym, False, True, False))
                if lw >= 0:
                    (resIdx, typIdx) = self.visit(BinaryOp("-", ast.idx, IntLiteral(lw)), Access(frame, lsSym, False, True, True))
                else:
                    (resIdx, typIdx) = self.visit(BinaryOp("+", ast.idx, IntLiteral(- lw)), Access(frame, lsSym, False, True, True))
                
                if type(typeArr) is ArrayType:
                    arrayType = typeArr.eleType
                    aload = self.emit.emitALOAD(arrayType, frame)
                    return (resArr + resIdx + aload, arrayType)
                elif type(typeArr) is ArrayPointerType:
                    arrayPointerType = typeArr.eleType
                    aload = self.emit.emitALOAD(arrayPointerType, frame)
                    return (resArr + resIdx + aload, arrayPointerType)
        else:
            frame = c.frame
            lsSym = c.sym
            (resArr, typeArr) = self.visit(ast.arr, Access(frame, lsSym, False, True, False))
            arrType = typeArr.eleType
            return ("", arrayType)
        

    def visitAssign(self, ast, c):
        ctxt = c
        frame = ctxt.frame
        env = ctxt.sym
        op_Str = ""
        str_I2f = "" 
        resType = IntType()
        print(ast)
        (resLeft1, typeLeft1) = self.visit(ast.lhs, Access(frame, env, True, True))
        (resRight, typeRight) = self.visit(ast.exp,Access(frame, env, False, True))

        if type(typeLeft1) == FloatType and type(typeRight) == IntType:
            str_I2f = self.emit.emitI2F(frame)
        
        (resLeft2, typeLeft2) = self.visit(ast.lhs, Access(frame, env, True, False))
        
        _fcp, _type = self.genBinExpr(frame, resLeft1, typeLeft1, resRight, typeRight)
        _string = _fcp + resLeft2
        
        self.emit.printout(_string)
        return (_string, _type)
    
    def visitWith(self, ast, c):
        ctxt = c
        frame = ctxt.frame
        newEnv = ctxt.sym
        
        frame.enterScope(False)
        
        varEnv = functools.reduce(lambda a, b: self.visit(b, a), ast.decl, SubBody(frame, newEnv))
        
        # list Vardecl
        listVarDecl = ast.decl
        listArrayVarDecl = filter(lambda x: type(x.varType) is ArrayType, listVarDecl)
        
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        [self.arrayTypeDecl(x, varEnv) for x in listArrayVarDecl]
        [self.visit(x, varEnv) for x in ast.stmt]
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        frame.exitScope()
        return None

    def visitFor(self, ast, c):
        frame = c.frame
        env = c.sym
        beginLabel = frame.getNewLabel()
        frame.enterLoop()

        self.visit(Assign(ast.id, ast.expr1), SubBody(frame, env))
        self.emit.printout(self.emit.emitLABEL(beginLabel, frame))
        if ast.up:
            (resExpr2, typeExpr2) = self.visit(BinaryOp("<=", ast.id, ast.expr2), Access(frame, env, False, True, False))
        else:
            (resExpr2, typeExpr2) = self.visit(BinaryOp(">=", ast.id, ast.expr2), Access(frame, env, False, True, False))
        self.emit.printout(resExpr2)
        self.emit.printout(self.emit.emitIFFALSE(frame.getBreakLabel(), frame))
        [self.visit(i, c) for i in ast.loop]
        
        self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
        if ast.up:
            self.visit(Assign(ast.id, BinaryOp("+", ast.id, IntLiteral(1))), c)
        else:
            self.visit(Assign(ast.id, BinaryOp("-", ast.id, IntLiteral(1))), c)
        self.emit.printout(self.emit.emitGOTO(beginLabel, frame))
        self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))
        
        frame.exitLoop()
        return None

        

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
            typeFunc = self.curFunc.mtype.rettype
            if type(typeFunc) == FloatType and type(resType) == IntType:
                self.emit.printout(resExpr + self.emit.emitI2F(c.frame) + self.emit.emitRETURN(FloatType(),c.frame))
            else:
                self.emit.printout(resExpr + self.emit.emitRETURN(resType,c.frame))
        else:
            self.emit.printout(self.emit.emitRETURN(VoidType(), c.frame))
            
        return None
    # def visitCallExpr(self,ast,o):
        
    #     ctxt = o
    #     frame = ctxt.frame
    #     env = ctxt.sym
    #     sym = self.lookup(ast.method.name,env,lambda x: x.name)
    #     cname = sym.value.value
    #     ctype = sym.mtype
    #     returnType = ctype.rettype

    #     if ctxt.isLeft is True and ctxt.isFirst is False:
    #         return (self.emit.emitWRITEVAR2(ast.method.name,returnType,frame))
        
    def visitCallStmt(self, ast, c):
        ctxt = c
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name.lower(), nenv, lambda x: x.name.lower())
        cname = sym.value.value

        ctype = sym.mtype
        
        listParamType = ctype.partype
        checkList = []
        for item in range(len(listParamType)):
            checkList.append((ast.param[item], listParamType[item]))
        
        in_ = ("", list())
        
        for x in checkList:
            (str1, typ1) = self.visit(x[0], Access(frame, nenv, False, True))
            if type(x[1]) is ArrayType:
                str1 += self.emit.emitCLONE(typ1) + self.emit.emitCHECKCAST(typ1)
            if type(typ1) is IntType and type(x[1]) is FloatType:
                in_ = (in_[0] + str1 + self.emit.emitI2F(frame), in_[1] + [typ1])
            else:
                in_ = (in_[0] + str1, in_[1] + [typ1])

        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + sym.name, ctype, frame))
        return None
    
    # def visitId(self, ast,o):
    #     # o : Access (SubBody)

    #     if type(o) != SubBody: 
    #         sym  = self.lookup(ast.name, o.sym, lambda x: x.name)

    #         code = ""
    #         if o.isLeft is True and o.isFirst is True:
    #             pass
    #         elif o.isLeft is True and o.isFirst is False:
    #             if type(sym.mtype) is ArrayType or type(sym.mtype) is ArrayPointerType:
    #                 code = self.emit.emitWRITEVAR2(ast.name, sym.mtype, o.frame)
    #             else:
    #                 if type(sym.value) is CName:
    #                     code = self.emit.emitPUTSTATIC(sym.value.value + "." + ast.name, sym.mtype, o.frame)
    #                 elif type(sym.value) is Index:
    #                     code = self.emit.emitWRITEVAR(ast.name, sym.mtype, sym.value.value, o.frame) 

    #         elif o.isLeft is False:
    #             if type(sym.value) is CName:
    #                 code = self.emit.emitGETSTATIC(sym.value.value + "." + ast.name, sym.mtype, o.frame)
    #             elif type(sym.value) is Index:
    #                 code = self.emit.emitREADVAR(ast, sym.mtype, sym.value.value, o.frame)
                    
    #         return (code,sym.mtype)
    #     else:
    #         sym  = self.lookup(ast.name, o.sym, lambda x: x.name)
    #         return ("",sym.mtype)
    
    # def visitAssign(self,ast,c):
    #     ctxt = c
    #     frame = ctxt.frame
    #     env = ctxt.sym
    #     op = ast.op
    #     op_Str = ""
    #     str_I2f = "" 
    #     resType = IntType()

    #     (resLeft, typeLeft) = self.visit(ast.left, Access(frame, env, True, True, False))
    #     (resRight, typeRight) = self.visit(ast.right,Access(frame, env, False, True, True))

    #     if type(typeLeft) == FloatType and type(typeRight) == IntType:
    #         str_I2f = self.emit.emitI2F(frame)    
    #     op_Str = resLeft + resRight + str_I2f 
    #     resType = typeLeft
    #     self.emit.printout(op_Str)
    
    
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
