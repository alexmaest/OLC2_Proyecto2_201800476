from AST.Abstracts.Instruccion import Instruccion
from AST.Expressions.AccessArray import AccessArray
from AST.Expressions.AttAccess import AttAccess
from AST.Expressions.NewArray import NewArray
from AST.Expressions.NewVector import NewVector
from AST.Instructions.For import For
from AST.Instructions.ListArraySimple import ListArraySimple
from AST.Symbol.Symbol import Symbol
from AST.Instructions.Match import Match
from AST.Instructions.While import While
from AST.Instructions.Loop import Loop
from AST.Instructions.Match import Match
from AST.Instructions.If import If
from AST.Expressions.Access import Access
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class DeclarationSingle(Instruccion):

    def __init__(self, asignation, expression, row, column):
        self.asignation = asignation
        self.expression = expression
        self.isExpSentence = False
        self.isReference = False
        self.newEnv = None
        self.oldSize = None
        self.isParam = False
        self.row = row
        self.column = column

    def compile(self, enviroment):
        content = self.asignation.compile(enviroment)
        dimensions = None
        if isinstance(self.expression,While) or isinstance(self.expression,If) or isinstance(self.expression,Loop) or isinstance(self.expression,Match) or isinstance(self.expression,For):
            self.expression.isExpSentence = True
            self.isExpSentence = True
        exp = self.expression.compile(enviroment)
        if self.newEnv != None:
            enviroment = self.newEnv
        if self.oldSize == None:
            self.oldSize = enviroment.size
        if content != None and exp != None:
            if content.typeSingle == TYPE_DECLARATION.SIMPLE or content.typeSingle == TYPE_DECLARATION.VECTOR:
                if exp.typeVar == None and exp.typeSingle == TYPE_DECLARATION.VECTOR:
                    enviroment.saveVariable(Symbol(content.typeVar[3],content.typeVar[1],content.typeSingle,content.typeVar[0],exp.att,dimensions,self.row,self.column))
                elif content.typeSingle == exp.typeSingle:
                    if exp.typeVar == content.typeVar[3]:
                        if isinstance(self.expression,NewArray) or isinstance(self.expression,NewVector):dimensions = self.expression.dimensions
                        if isinstance(self.expression,AttAccess): 
                            if isinstance(self.expression.expList[0].id.id,AccessArray):dimensions = self.expression.expList[0].id.id.dimensions
                        size = enviroment.size
                        if enviroment.saveVariable(Symbol(content.typeVar[3],content.typeVar[1],content.typeSingle,content.typeVar[0],enviroment.size,self.isReference,exp.att,dimensions,self.row,self.column)):
                            return Retorno(None,None,None,None,self.createDeclaration(enviroment,exp,self.oldSize,self.isParam,size),None,None)
                        else:pass
                    elif self.uSizeValidation(exp.typeVar,content.typeVar[3]):
                        size = enviroment.size
                        if enviroment.saveVariable(Symbol(TYPE_DECLARATION.USIZE,content.typeVar[1],content.typeSingle,content.typeVar[0],enviroment.size,self.isReference,exp.att,dimensions,self.row,self.column)):
                            return Retorno(None,None,None,None,self.createDeclaration(enviroment,exp,self.oldSize,self.isParam,size),None,None)
                        else:pass
                    else: listError.append(Error("Error: No se puede asignar un valor "+str(exp.typeVar)+" a una variable tipo "+str(content.typeVar[3]),"Local",self.row,self.column,"SEMANTICO"))
                else: listError.append(Error("Error: Está tratando de asignar un valor de diferentes dimensiones a las que intenta declarar","Local",self.row,self.column,"SEMANTICO"))
            else:
                #Comparar si las dimensiones a asignar son las mismas
                if exp.typeVar == content.typeVar[3]:
                    if exp.typeSingle == TYPE_DECLARATION.ARRAY:
                        if isinstance(self.expression,NewArray) or isinstance(self.expression,NewVector) or isinstance(self.expression,AccessArray):dimensions = self.expression.dimensions
                        if isinstance(self.expression,AttAccess): 
                            if isinstance(self.expression.expList[0].id.id,AccessArray):dimensions = self.expression.expList[0].id.id.dimensions
                        if isinstance(self.asignation.type, ListArraySimple):
                            size = enviroment.size
                            if enviroment.saveVariable(Symbol(content.typeVar[3],content.typeVar[1],content.typeSingle,content.typeVar[0],enviroment.size,True,exp.att,dimensions,self.row,self.column)):
                                return Retorno(None,None,None,None,self.createDeclaration(enviroment,exp,self.oldSize,self.isParam,size),None,None)
                            else:pass
                        else:
                            if isinstance(self.expression,NewArray) or isinstance(self.expression,NewVector) or isinstance(self.expression,AccessArray):dimensions = self.expression.dimensions
                            if isinstance(self.expression,AttAccess): 
                                if isinstance(self.expression.expList[0].id.id,AccessArray):dimensions = self.expression.expList[0].id.id.dimensions
                            size = enviroment.size
                            if enviroment.saveVariable(Symbol(content.typeVar[3],content.typeVar[1],content.typeSingle,content.typeVar[0],enviroment.size,True,exp.att,dimensions,self.row,self.column)):
                                return Retorno(None,None,None,None,self.createDeclaration(enviroment,exp,self.oldSize,self.isParam,size),None,None)
                            else:pass
                    elif exp.typeSingle == content.typeSingle:
                        if isinstance(self.expression,NewArray) or isinstance(self.expression,NewVector) or isinstance(self.expression,AccessArray):dimensions = self.expression.dimensions
                        if isinstance(self.expression,AttAccess): 
                            if isinstance(self.expression.expList[0].id.id,AccessArray):dimensions = self.expression.expList[0].id.id.dimensions
                        enviroment.saveVariable(Symbol(content.typeVar[3],content.typeVar[1],content.typeSingle,content.typeVar[0],exp.att,dimensions,self.row,self.column))
                    else: listError.append(Error("Error: No se puede asignar un valor simple a una variable de varias dimensiones","Local",self.row,self.column,"SEMANTICO"))
                else: listError.append(Error("Error: No se puede asignar un valor "+str(exp.typeVar)+" a una variable tipo "+str(content.typeVar[3]),"Local",self.row,self.column,"SEMANTICO"))
        else: listError.append(Error("Error: No se pudo asignar la variable porque su valor es nulo","Local",self.row,self.column,"SEMANTICO"))

    def createDeclaration(self, enviroment, exp, size, param, newSize):
        if param and self.isReference:
            temporal = enviroment.generator.generateTemporal()
            temporal2 = enviroment.generator.generateTemporal()
            CODE = '/* DECLARACIÓN PARAMETRO CON REFERENCIA */\n'
            CODE += exp.code
            CODE += f'  {temporal} = SP + {size};\n'
            CODE += f'  {temporal2} = {temporal} + {newSize};\n'
            CODE += f'  Stack[(int) {temporal2}] = {exp.temporal};\n'
            return CODE
        elif param and not self.isReference:
            temporal = enviroment.generator.generateTemporal()
            temporal2 = enviroment.generator.generateTemporal()
            CODE = '/* DECLARACIÓN PARAMETRO */\n'
            CODE += exp.code
            CODE += f'  {temporal} = SP + {size};\n'
            CODE += f'  {temporal2} = {temporal} + {newSize};\n'
            CODE += f'  Stack[(int) {temporal2}] = {exp.temporal};\n'
            return CODE
        else:
            temporal = enviroment.generator.generateTemporal()
            CODE = "/* DECLARACIÓN */\n"
            CODE += exp.code
            CODE += f'  {temporal} = SP + {size};\n'
            if self.isExpSentence:
                temporal2 = enviroment.generator.generateTemporal()
                CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                CODE += f'  Stack[(int) {temporal}] = {temporal2};\n'
            else:
                CODE += f'  Stack[(int) {temporal}] = {exp.temporal};\n'
            return CODE

    def uSizeValidation(self, assignation, expression):
        if assignation == TYPE_DECLARATION.USIZE and expression == TYPE_DECLARATION.INTEGER:
            return True
        elif assignation == TYPE_DECLARATION.INTEGER and expression == TYPE_DECLARATION.USIZE:
            return True
        else:
            return False

    '''
        [[1,4],[1,4],[1,4],[1,4],[1,4]]
        [[1,4],4,3,2,1]
    '''