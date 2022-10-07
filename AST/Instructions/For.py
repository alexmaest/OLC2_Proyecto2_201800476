from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.ForIterative import ForIterative
from AST.Symbol.Enviroment import Enviroment
from AST.Symbol.Symbol import Symbol
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class For(Instruccion):
    def __init__(self, id, iterativeExp, statement, row, column):
        self.id = id
        self.iterativeExp = iterativeExp
        self.statement = statement
        self.row = row
        self.column = column

    def executeInstruction(self, enviroment):
        if isinstance(self.iterativeExp,ForIterative):
            iterativeL = self.iterativeExp.lExp.executeInstruction(enviroment)
            iterativeR = self.iterativeExp.rExp.executeInstruction(enviroment)
            Pass = False
            if iterativeL.typeSingle == TYPE_DECLARATION.SIMPLE and iterativeR.typeSingle == TYPE_DECLARATION.SIMPLE:
                if iterativeL.typeVar == TYPE_DECLARATION.INTEGER and iterativeR.typeVar == TYPE_DECLARATION.INTEGER:
                    Pass = True
                elif iterativeL.typeVar == TYPE_DECLARATION.FLOAT and iterativeR.typeVar == TYPE_DECLARATION.FLOAT:
                    Pass = True
                else:
                    listError.append(Error("Error: No se puede iterar debido a que el rango no es correcto","Local",self.row,self.column,"SEMANTICO"))
            else:
                listError.append(Error("Error: No se puede iterar debido a que el rango no son valores simples","Local",self.row,self.column,"SEMANTICO"))
            if Pass:
                newEnv = Enviroment(enviroment, enviroment.console)
                newEnv.saveVariable(Symbol(iterativeL.typeVar,self.id,None,iterativeL.typeSingle,True,self.row,self.column))
                for single in range(iterativeL.value,iterativeR.value):
                    newEnv.editVariable(self.id,single)
                    returned = self.statement.executeInstruction(newEnv)
                    if returned != None:
                        if returned.typeSingle == TYPE_DECLARATION.BREAK:
                            break
                        elif returned.typeSingle == TYPE_DECLARATION.CONTINUE:
                            continue
                        else:
                            return returned
        else:
            iterative = self.iterativeExp.executeInstruction(enviroment)
            if iterative != None:
                if iterative.typeSingle == TYPE_DECLARATION.ARRAY or iterative.typeSingle == TYPE_DECLARATION.VECTOR:
                    newEnv = Enviroment(enviroment,enviroment.console)
                    singleIterative = None
                    if iterative.typeSingle == TYPE_DECLARATION.ARRAY:
                        newEnv.saveVariable(Symbol(iterative.typeVar,self.id,None,iterative.value[0].typeSingle,True,self.row,self.column))
                        singleIterative = iterative.value
                    else:
                        newEnv.saveVariable(Symbol(iterative.typeVar,self.id,None,iterative.value[1][0].typeSingle,True,self.row,self.column))
                        singleIterative = iterative.value[1]
                    for single in singleIterative:
                        newEnv.editVariable(self.id,single.value)
                        returned = self.statement.executeInstruction(newEnv)
                        if returned != None:
                            if returned.typeSingle == TYPE_DECLARATION.BREAK:
                                break
                            elif returned.typeSingle == TYPE_DECLARATION.CONTINUE:
                                continue
                            else:
                                return returned
                else:
                    listError.append(Error("Error: La expresion no se puede iterar","Local",self.row,self.column,"SEMANTICO"))
            else:
                listError.append(Error("Error: La expresion no se puede iterar porque no existe o no ha sido declarada","Local",self.row,self.column,"SEMANTICO"))