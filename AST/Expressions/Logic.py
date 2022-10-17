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
    
    def compile(self, enviroment):
        leftValue = self.lExp.compile(enviroment)
        rightValue = self.rExp.compile(enviroment)
        
        if leftValue != None and rightValue != None:
            CODE = ''
            if self.type == TYPE_LOGICAL.AND:
                result = leftValue.value and rightValue.value
                CODE += leftValue.code
                CODE += f'{leftValue.trueLabel}:\n'
                CODE += rightValue.code
                value = Retorno(TYPE_DECLARATION.VALOR,TYPE_DECLARATION.BOOLEAN,result,TYPE_DECLARATION.SIMPLE,None,CODE,None)
                value.trueLabel = rightValue.trueLabel
                value.falseLabel = f'{leftValue.falseLabel}:\n{rightValue.falseLabel}'
                return value
            elif self.type == TYPE_LOGICAL.OR:
                result = leftValue.value or rightValue.value
                CODE += leftValue.code
                CODE += f'{leftValue.falseLabel}:\n'
                CODE += rightValue.code
                value = Retorno(TYPE_DECLARATION.VALOR,TYPE_DECLARATION.BOOLEAN,result,TYPE_DECLARATION.SIMPLE,None,CODE,None)
                value.trueLabel = f'{leftValue.trueLabel}:\n{rightValue.trueLabel}'
                value.falseLabel = rightValue.falseLabel
                return value
            elif self.type == TYPE_LOGICAL.NOT:
                result = not(leftValue.value)
                CODE += leftValue.code
                value = Retorno(TYPE_DECLARATION.VALOR,TYPE_DECLARATION.BOOLEAN,result,TYPE_DECLARATION.SIMPLE,None,CODE,None)
                value.trueLabel = leftValue.falseLabel
                value.falseLabel = leftValue.trueLabel
                return value
        else:
            listError.append(Error("Error: No se ha podido realizar la logica de comparación","Local",self.row,self.column,"SEMANTICO"))
            return None