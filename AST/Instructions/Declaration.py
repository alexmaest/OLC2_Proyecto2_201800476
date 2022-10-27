from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Expressions.AccessArray import AccessArray
from AST.Expressions.AttAccess import AttAccess
from AST.Expressions.NewArray import NewArray
from AST.Expressions.NewVector import NewVector
from AST.Instructions.For import For
from AST.Instructions.Match import Match
from AST.Instructions.While import While
from AST.Instructions.Loop import Loop
from AST.Instructions.Match import Match
from AST.Instructions.If import If
from AST.Symbol.Symbol import Symbol
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Declaration(Instruccion):

    def __init__(self, mutable, assignation, row, column):
        self.mutable = mutable
        self.assignation = assignation
        self.isExpSentence = False
        self.row = row
        self.column = column

    def compile(self, enviroment):
        if isinstance(self.assignation.expression,While) or isinstance(self.assignation.expression,If) or isinstance(self.assignation.expression,Loop) or isinstance(self.assignation.expression,Match) or isinstance(self.assignation.expression,For):
            self.assignation.expression.isExpSentence = True
            self.isExpSentence = True
        exp = self.assignation.expression.compile(enviroment)
        if exp != None:
            if exp.typeVar == None and exp.typeSingle == TYPE_DECLARATION.VECTOR:
                listError.append(Error("Error: La variable no ha podido ser declarada porque no posee un tipo para crear un vector","Local",self.row,self.column,"SEMANTICO"))
            else:
                isNotSimple = False
                dimensions = None
                size = enviroment.size
                #Por si el valor es primitivo o no
                if exp.typeSingle != TYPE_DECLARATION.SIMPLE: isNotSimple = True
                if isinstance(self.assignation.expression,NewArray) or isinstance(self.assignation.expression,NewVector):dimensions = self.assignation.expression.dimensions
                if isinstance(self.assignation.expression,AttAccess): 
                    if isinstance(self.assignation.expression.expList[0].id.id,AccessArray):dimensions = self.assignation.expression.expList[0].id.id.dimensions
                if enviroment.saveVariable(Symbol(exp.typeVar,self.assignation.idList[0].id.id,exp.typeSingle,self.mutable,size,isNotSimple,exp.att,dimensions,self.row,self.column)):
                    temporal = enviroment.generator.generateTemporal()
                    CODE = "/* DECLARACIÓN */\n"
                    CODE += exp.code
                    CODE += f'  {temporal} = SP + {size}; \n'
                    if self.isExpSentence:
                        temporal2 = enviroment.generator.generateTemporal()
                        CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                        CODE += f'  Stack[(int) {temporal}] = {temporal2};\n'
                    else:
                        CODE += f'  Stack[(int) {temporal}] = {exp.temporal};\n'
                    return Retorno(None,None,None,None,CODE,None,None)
                else:
                    #Ya se notificó todo
                    return None
        else:
            listError.append(Error("Error: La variable no ha podido ser declarada","Local",self.row,self.column,"SEMANTICO"))