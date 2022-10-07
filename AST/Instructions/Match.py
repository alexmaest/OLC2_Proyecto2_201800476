from AST.Abstracts.Instruccion import Instruccion
from AST.Expressions.AttAccess import AttAccess
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Match(Instruccion):
    def __init__(self, expression, statement, row, column):
        self.expression = expression
        self.statement = statement
        self.row = row
        self.column = column

    def executeInstruction(self, enviroment):
        singleExp = self.expression.executeInstruction(enviroment)
        if singleExp != None:
            #Validación si se encuentra el caso '_'
            founded = False
            for arm in self.statement.instructions:
                armExps = arm.getExpressions()
                for singleArmExp in armExps:
                    if isinstance(singleArmExp,AttAccess):
                        if singleArmExp.expList[0].id.id == '_' and self.statement.instructions[-1] == arm:
                            founded = True
                    
            if founded:
                executed = False
                for arm in self.statement.instructions:
                    armExps = arm.getExpressions()
                    for singleArmExp in armExps:
                        if isinstance(singleArmExp,AttAccess):
                            if singleArmExp.expList[0].id.id  == '_':
                                if not executed:
                                    return arm.executeInstruction(enviroment)
                            else:
                                returned = singleArmExp.executeInstruction(enviroment)
                                if returned != None:
                                    if singleExp.typeVar == returned.typeVar:
                                        if singleExp.typeSingle == returned.typeSingle:
                                            if singleExp.value == returned.value:
                                                executed = True
                                                return arm.executeInstruction(enviroment)
                                            else: continue
                                        else:
                                            listError.append(Error("Error: El valor que desea comparar no posee las dimensiones correctas","Local",self.row,self.column,"SEMANTICO"))
                                            break
                                    else:
                                        listError.append(Error("Error: El valor que desea comparar no posee el tipo correcto","Local",self.row,self.column,"SEMANTICO"))
                                        break
                                else:
                                    listError.append(Error("Error: El valor del brazo es nulo","Local",self.row,self.column,"SEMANTICO"))
                                    break
                        else:
                            returned = singleArmExp.executeInstruction(enviroment)
                            if returned != None:
                                if singleExp.typeVar == returned.typeVar:
                                    if singleExp.typeSingle == returned.typeSingle:
                                        if singleExp.value == returned.value:
                                            executed = True
                                            return arm.executeInstruction(enviroment)
                                        else: continue
                                    else:
                                        listError.append(Error("Error: El valor que desea comparar no posee las dimensiones correctas","Local",self.row,self.column,"SEMANTICO"))
                                        break
                                else:
                                    listError.append(Error("Error: El valor que desea comparar no posee el tipo correcto","Local",self.row,self.column,"SEMANTICO"))
                                    break
                            else:
                                listError.append(Error("Error: El valor del brazo es nulo","Local",self.row,self.column,"SEMANTICO"))
                                break
            else:
                listError.append(Error("Error: El brazo '_' debe de ser el último de la sentencia match","Local",self.row,self.column,"SEMANTICO"))
        else:
            listError.append(Error("Error: No se ha podido ejecutar la sentencia match porque su valor a comparar es nulo","Local",self.row,self.column,"SEMANTICO"))