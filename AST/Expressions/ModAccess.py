from unicodedata import name
from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno
from AST.Expressions.CallFunction import CallFunction
from AST.Expressions.Handler import Handler
from AST.Expressions.Access import Access
from AST.Instructions.Function import Function
from AST.Instructions.Modulo import Modulo
from AST.Symbol.Enviroment import Enviroment
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from enum import Enum

class ModAccess():
    def __init__(self, nameList, functionCall, row, column):
        self.nameList = nameList
        self.functionCall = functionCall
        self.row = row
        self.column = column
    
    def executeInstruction(self, enviroment):
        #Se retornan funciones dentro de modulos
        found = enviroment.getModule(self.nameList[0])#Modulo()
        if found != None:
            self.nameList.append(self.functionCall.id)
            return self.saveModuleInstructions(self.nameList, found, enviroment.getGlobal(), 1, enviroment)
        else: 
            listError.append(Error("Error: El modulo con id "+str(self.nameList[0])+" no existe","Local",self.row,self.column,"SEMANTICO"))
            return None

    def saveModuleInstructions(self, nameList, module, enviroment, number, permanentEnv):
        newEnv = Enviroment(enviroment,enviroment.console)
        for instruction in module.instructions.instructions:
            instruction.executeInstruction(newEnv)

        for instruction in module.instructions.instructions:
            if instruction.instruction.id == nameList[number]:
                if (number + 1) == len(nameList):
                    returned = newEnv.getFunction(nameList[number])
                    if returned != None:
                        if instruction.isPublic:
                            #Si el id coincide con la funcion dentro del modulo
                            self.functionCall.newFunction = returned
                            self.functionCall.newEnviroment = newEnv
                            return self.functionCall.executeInstruction(permanentEnv)
                        else:
                            listError.append(Error("Error: La función "+str(nameList[number])+" no es pública","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    else:
                        listError.append(Error("Error: El modulo "+str(module.id)+" no tiene ninguna función llamada "+str(nameList[number]),"Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    returned = newEnv.getModule(nameList[number])
                    if returned != None:
                        if instruction.isPublic:
                            return self.saveModuleInstructions(nameList, instruction.instruction, newEnv, number+1, permanentEnv)
                        else:
                            listError.append(Error("Error: El modulo "+str(nameList[number])+" no es público","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    else:
                        listError.append(Error("Error: El modulo "+str(module.id)+" no tiene ningún modulo llamado "+str(nameList[number]),"Local",self.row,self.column,"SEMANTICO"))
                        return None
        listError.append(Error("Error: No existe ningún modulo, struct o función con el nombre "+str(nameList[number]),"Local",self.row,self.column,"SEMANTICO"))
        return None

