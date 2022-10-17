from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import re

class While(Instruccion):
    def __init__(self, condition, statement, row, column):
        self.condition = condition
        self.statement = statement
        self.row = row
        self.column = column

    def compile(self, enviroment):
        condition = self.condition.compile(enviroment)
        if condition != None:
            if condition.typeVar == TYPE_DECLARATION.BOOLEAN:
                whileLabel = enviroment.generator.generateLabel()
                returned = self.statement.compile(enviroment)
                breakLabel = ''
                continueLabel = ''
                result = re.findall("BreakLabel",functionCode)
                if len(result) > 0:
                    breakLabel = enviroment.generator.generateLabel()
                    functionCode = functionCode.replace("BreakLabel",breakLabel)
                    breakLabel = breakLabel + ':\n'
                result = re.findall("ContinueLabel",functionCode)
                if len(result) > 0:
                    continueLabel = enviroment.generator.generateLabel()
                    functionCode = functionCode.replace("ContinueLabel",continueLabel)
                    continueLabel = continueLabel + ':\n'
                CODE = '/* WHILE */\n'
                CODE += f'{whileLabel}:\n'
                CODE += continueLabel
                CODE += condition.code
                CODE += f'{condition.trueLabel}: \n'
                CODE += returned.code
                CODE += f'  goto {whileLabel};\n'
                CODE += f'{condition.falseLabel}: \n'
                CODE += breakLabel
                return Retorno(returned.typeIns,returned.typeVar,returned.value,returned.typeSingle,None,CODE,None)
            else:
                listError.append(Error("Error: La condición no es un booleano","Local",self.row,self.column,"SEMANTICO"))
        else:
            listError.append(Error("Error: No se ha podido ejecutar la sentencia While","Local",self.row,self.column,"SEMANTICO"))