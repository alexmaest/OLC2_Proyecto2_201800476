from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from enum import Enum

class TYPE_RELATIONAL(Enum):
    IGUALI = 0,
    DIF = 1,
    MAYOR = 2,
    MENOR = 3,
    MAYORI = 4,
    MENORI = 5

class Relational():
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
            CODE += leftValue.code
            CODE += rightValue.code
            trueLabel = enviroment.generator.obtenerEtiqueta()
            falseLabel = enviroment.generator.obtenerEtiqueta()
            if self.type == TYPE_RELATIONAL.IGUALI:
                result = leftValue.value == rightValue.value
                CODE += f'  if ({leftValue.temporal} == {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'  goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.DIF:
                result = leftValue.value != rightValue.value
                CODE += f'  if ({leftValue.temporal} != {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'  goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MAYOR:
                result = leftValue.value > rightValue.value
                CODE += f'  if ({leftValue.temporal} > {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'  goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MENOR:
                result = leftValue.value < rightValue.value
                CODE += f'  if ({leftValue.temporal} < {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'  goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MAYORI:
                result = leftValue.value >= rightValue.value
                CODE += f'  if ({leftValue.temporal} >= {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'  goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MENORI:
                result = leftValue.value <= rightValue.value
                CODE += f'  if ({leftValue.temporal} <= {rightValue.temporal}) goto {trueLabel};\n'
                CODE += f'  goto {falseLabel};\n'
                value = Retorno(TYPE_DECLARATION.BOOLEAN, result, TYPE_DECLARATION.SIMPLE,"",CODE,"")
                value.trueLabel = trueLabel
                value.falseLabel = falseLabel
                return value
            else:
                listError.append(Error("Error: No se ha podido realizar la comparación","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            listError.append(Error("Error: No se ha podido realizar la comparación","Local",self.row,self.column,"SEMANTICO"))
            return None