from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import re

class While(Instruccion):
    def __init__(self, condition, statement, row, column):
        self.condition = condition
        self.isExpSentence = False
        self.statement = statement
        self.row = row
        self.column = column

    def compile(self, enviroment):
        #Se compila la condicion y se asignan las etiquetas
        trueLabel = enviroment.generator.generateLabel()
        falseLabel = enviroment.generator.generateLabel()
        self.condition.trueLabel = trueLabel
        self.condition.falseLabel = falseLabel
        condition = self.condition.compile(enviroment)
        if condition != None:
            if condition.typeVar == TYPE_DECLARATION.BOOLEAN:
                whileLabel = enviroment.generator.generateLabel()
                if self.isExpSentence: 
                    self.statement.isExpSentence = True
                    self.statement.insideLoop = True
                returned = self.statement.compile(enviroment)
                functionCode = returned.code
                breakLabel = ''
                continueLabel = ''
                returnLabel = ''
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
                if self.isExpSentence:
                    result = re.findall("ReturnLabel",functionCode)
                    if len(result) > 0:
                        returnLabel = enviroment.generator.generateLabel()
                        functionCode = functionCode.replace("ReturnLabel",returnLabel)
                        returnLabel = returnLabel + ':\n'
                CODE = '/* WHILE */\n'
                CODE += f'{whileLabel}:\n'
                CODE += continueLabel
                CODE += condition.code
                CODE += f'{condition.trueLabel}: \n'
                CODE += functionCode
                CODE += f'  goto {whileLabel};\n'
                CODE += f'{condition.falseLabel}: \n'
                CODE += breakLabel
                CODE += returnLabel
                return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)
            else:listError.append(Error("Error: La condición no es un booleano","Local",self.row,self.column,"SEMANTICO"))
        else:listError.append(Error("Error: No se ha podido ejecutar la sentencia While","Local",self.row,self.column,"SEMANTICO"))