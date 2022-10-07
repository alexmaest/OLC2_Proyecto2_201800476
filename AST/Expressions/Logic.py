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
        CODE = ''
        CODE += leftValue.code
        CODE += rightValue.code
        trueLabel = enviroment.generator.obtenerEtiqueta()
        falseLabel = enviroment.generator.obtenerEtiqueta()
        if leftValue != None and rightValue != None:
            if self.type == TYPE_LOGICAL.AND:
                result = leftValue.value and rightValue.value
                CODE += f'if ({leftValue.temporal} && {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            elif self.type == TYPE_LOGICAL.OR:
                result = leftValue.value or rightValue.value
                CODE += f'if ({leftValue.temporal} || {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            elif self.type == TYPE_LOGICAL.NOT:
                result = not(leftValue.value)
                CODE += f'if ({leftValue.temporal}) goto {trueLabel};\n'
                CODE += f'goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = falseLabel
                value.falseLabel = trueLabel
                return value
            else:
                listError.append(Error("Error: No se ha podido realizar la logica de comparación","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            listError.append(Error("Error: No se ha podido realizar la logica de comparación","Local",self.row,self.column,"SEMANTICO"))
            return None