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
        self.trueLabel = ''
        self.falseLabel = ''
    
    def compile(self, enviroment):
        leftValue = self.lExp.compile(enviroment)
        rightValue = self.rExp.compile(enviroment)
        if leftValue != None and rightValue != None:
            CODE = ''
            CODE += leftValue.code
            CODE += rightValue.code
            if self.type == TYPE_RELATIONAL.IGUALI:
                CODE += f'  if ({leftValue.temporal} == {rightValue.temporal}) goto {self.trueLabel};\n'
                CODE += f'  goto {self.falseLabel};\n'
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.DIF:
                CODE += f'  if ({leftValue.temporal} != {rightValue.temporal}) goto {self.trueLabel};\n'
                CODE += f'  goto {self.falseLabel};\n'
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MAYOR:
                CODE += f'  if ({leftValue.temporal} > {rightValue.temporal}) goto {self.trueLabel};\n'
                CODE += f'  goto {self.falseLabel};\n'
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MENOR:
                CODE += f'  if ({leftValue.temporal} < {rightValue.temporal}) goto {self.trueLabel};\n'
                CODE += f'  goto {self.falseLabel};\n'
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MAYORI:
                CODE += f'  if ({leftValue.temporal} >= {rightValue.temporal}) goto {self.trueLabel};\n'
                CODE += f'  goto {self.falseLabel};\n'
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            elif self.type == TYPE_RELATIONAL.MENORI:
                CODE += f'  if ({leftValue.temporal} <= {rightValue.temporal}) goto {self.trueLabel};\n'
                CODE += f'  goto {self.falseLabel};\n'
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            else:
                listError.append(Error("Error: No se ha podido realizar la comparación","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            listError.append(Error("Error: No se ha podido realizar la comparación","Local",self.row,self.column,"SEMANTICO"))
            return None