from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from enum import Enum

class TYPE_LOGICAL(Enum):
    AND = 0,
    OR = 1,
    NOT = 2,

class Logic():
    def __init__(self, lExp, type, rExp, row, column):
        self.lExp = lExp
        self.type = type
        self.rExp = rExp
        self.row = row
        self.column = column
        self.trueLabel = ''
        self.falseLabel = ''
    
    def compile(self, enviroment):
        if self.type == TYPE_LOGICAL.AND:
            #Se colocan las respectivas etiquetas
            self.lExp.trueLabel = enviroment.generator.generateLabel()
            self.lExp.falseLabel = self.falseLabel 
            self.rExp.trueLabel = self.trueLabel 
            self.rExp.falseLabel = self.falseLabel 
            #Se compilan las expresiones
            leftValue = self.lExp.compile(enviroment)
            rightValue = self.rExp.compile(enviroment)
            if leftValue != None and rightValue != None:
                CODE = leftValue.code
                CODE += f'{leftValue.trueLabel}:\n'
                CODE += rightValue.code
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            else:
                listError.append(Error("Error: No se ha podido realizar la logica de comparación","Local",self.row,self.column,"SEMANTICO"))
                return None
        elif self.type == TYPE_LOGICAL.OR:
            #Se colocan las respectivas etiquetas
            self.lExp.trueLabel = self.trueLabel
            self.lExp.falseLabel = enviroment.generator.generateLabel()
            self.rExp.trueLabel = self.trueLabel 
            self.rExp.falseLabel = self.falseLabel 
            #Se compilan las expresiones
            leftValue = self.lExp.compile(enviroment)
            rightValue = self.rExp.compile(enviroment)
            if leftValue != None and rightValue != None:
                CODE = leftValue.code
                CODE += f'{leftValue.falseLabel}:\n'
                CODE += rightValue.code
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            else:
                listError.append(Error("Error: No se ha podido realizar la logica de comparación","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:#NOT
            #Se colocan las respectivas etiquetas
            self.lExp.trueLabel = self.falseLabel
            self.lExp.falseLabel = self.trueLabel
            #Se compila la expresión
            leftValue = self.lExp.compile(enviroment)
            if leftValue != None:
                CODE = leftValue.code
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.falseLabel
                value.falseLabel = self.trueLabel
                return value
            else:
                listError.append(Error("Error: No se ha podido realizar la logica de comparación","Local",self.row,self.column,"SEMANTICO"))
                return None