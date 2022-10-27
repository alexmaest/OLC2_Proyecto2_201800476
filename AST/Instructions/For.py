from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.ForIterative import ForIterative
from AST.Symbol.Enviroment import Enviroment
from AST.Symbol.Symbol import Symbol
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import re

class For(Instruccion):
    def __init__(self, id, iterativeExp, statement, row, column):
        self.id = id
        self.iterativeExp = iterativeExp
        self.isExpSentence = False
        self.statement = statement
        self.row = row
        self.column = column

    def compile(self, enviroment):
        if isinstance(self.iterativeExp,ForIterative):
            iterativeL = self.iterativeExp.lExp.compile(enviroment)
            iterativeR = self.iterativeExp.rExp.compile(enviroment)
            Pass = False
            if iterativeL.typeSingle == TYPE_DECLARATION.SIMPLE and iterativeR.typeSingle == TYPE_DECLARATION.SIMPLE:
                if iterativeL.typeVar == TYPE_DECLARATION.INTEGER and iterativeR.typeVar == TYPE_DECLARATION.INTEGER: Pass = True
                elif iterativeL.typeVar == TYPE_DECLARATION.FLOAT and iterativeR.typeVar == TYPE_DECLARATION.FLOAT: Pass = True
                else: listError.append(Error("Error: No se puede iterar debido a que el rango no es correcto","Local",self.row,self.column,"SEMANTICO"))
            else: listError.append(Error("Error: No se puede iterar debido a que el rango no son valores simples","Local",self.row,self.column,"SEMANTICO"))
            if Pass:
                varPos = enviroment.size
                newEnv = Enviroment(enviroment, enviroment.generator)
                newEnv.saveVariable(Symbol(iterativeL.typeVar,self.id,iterativeL.typeSingle,True,enviroment.size,False,iterativeL.att,None,self.row,self.column))
                temporal = enviroment.generator.generateTemporal()
                temporal2 = enviroment.generator.generateTemporal()
                temporal3 = enviroment.generator.generateTemporal()
                forLabel = enviroment.generator.generateLabel()
                trueLabel = enviroment.generator.generateLabel()
                falseLabel = enviroment.generator.generateLabel()
                if self.isExpSentence: 
                    self.statement.isExpSentence = True
                    self.statement.insideLoop = True
                iterativeCode = iterativeL.code
                iterativeCode += iterativeR.code
                iterativeCode += f'  {temporal} = 0;\n'
                conditionCode = f'  {temporal2} = {temporal} + {iterativeL.temporal};\n'
                functionCode = f'  {temporal3} = SP + {varPos};\n'
                functionCode += f'  Stack[(int){temporal3}] = {temporal2};//Asignación del valor iterado\n'
                conditionCode += f'  if({temporal2} != {iterativeR.temporal}) goto {trueLabel};\n'
                conditionCode += f'  goto {falseLabel};\n'
                returned = self.statement.compile(newEnv)
                functionCode += returned.code
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
                CODE = '/* FOR */\n'
                CODE += iterativeCode
                CODE += f'{forLabel}:\n'
                CODE += conditionCode
                CODE += f'{trueLabel}: \n'
                CODE += functionCode
                CODE += f'  {temporal} = {temporal} + 1;\n'
                CODE += f'  goto {forLabel};\n'
                CODE += f'{falseLabel}: \n'
                CODE += breakLabel
                CODE += returnLabel
                return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)
        else:
            iterative = self.iterativeExp.compile(enviroment)
            if iterative != None:
                if iterative.typeSingle == TYPE_DECLARATION.ARRAY or iterative.typeSingle == TYPE_DECLARATION.VECTOR:
                    newEnv = Enviroment(enviroment,enviroment.generator)
                    varPos = enviroment.size
                    newEnv.size = enviroment.size
                    if iterative.typeSingle == TYPE_DECLARATION.ARRAY: newEnv.saveVariable(Symbol(iterative.typeVar,self.id,TYPE_DECLARATION.SIMPLE,True,newEnv.size,False,iterative.att,self.iterativeExp.dimensions,self.row,self.column))
                    else: newEnv.saveVariable(Symbol(iterative.typeVar,self.id,iterative.typeSingle,True,self.row,self.column))
                    temporalAux = enviroment.generator.generateTemporal()
                    temporal = enviroment.generator.generateTemporal()
                    temporal2 = enviroment.generator.generateTemporal()
                    temporal3 = enviroment.generator.generateTemporal()
                    temporal4 = enviroment.generator.generateTemporal()
                    temporal5 = enviroment.generator.generateTemporal()
                    forLabel = enviroment.generator.generateLabel()
                    trueLabel = enviroment.generator.generateLabel()
                    falseLabel = enviroment.generator.generateLabel()
                    if self.isExpSentence: 
                        self.statement.isExpSentence = True
                        self.statement.insideLoop = True
                    iterativeCode = iterative.code
                    iterativeCode += f'  {temporal} = 0;\n'
                    iterativeCode += f'  {temporal2} = Heap[(int){iterative.temporal}];//Len del array\n'
                    functionCode = f'  {temporalAux} = {temporal} + 1;\n'
                    functionCode += f'  {temporal3} = {temporalAux} + {iterative.temporal};\n'
                    functionCode += f'  {temporal4} = Heap[(int){temporal3}];\n'
                    functionCode += f'  {temporal5} = SP + {varPos};\n'
                    functionCode += f'  Stack[(int){temporal5}] = {temporal4};//Asignación del valor iterado\n'
                    conditionCode = f'  if({temporal} != {temporal2}) goto {trueLabel};\n'
                    conditionCode += f'  goto {falseLabel};\n'
                    returned = self.statement.compile(newEnv)
                    functionCode += returned.code
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
                    CODE = '/* FOR */\n'
                    CODE += iterativeCode
                    CODE += f'{forLabel}:\n'
                    CODE += conditionCode
                    CODE += f'{trueLabel}: \n'
                    CODE += functionCode
                    CODE += f'  {temporal} = {temporal} + 1;\n'
                    CODE += f'  goto {forLabel};\n'
                    CODE += f'{falseLabel}: \n'
                    CODE += breakLabel
                    CODE += returnLabel
                    return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)
                else: listError.append(Error("Error: La expresion no se puede iterar","Local",self.row,self.column,"SEMANTICO"))
            else: listError.append(Error("Error: La expresion no se puede iterar porque no existe o no ha sido declarada","Local",self.row,self.column,"SEMANTICO"))