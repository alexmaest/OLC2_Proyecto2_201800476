from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno
from AST.Expressions.AccessArray import AccessArray
from AST.Expressions.AttAssign import AttAssign
from AST.Expressions.CallNative import CallNative
from AST.Expressions.Handler import Handler
from AST.Instructions.Native import Native
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from enum import Enum

class AttAccess():
    def __init__(self, expList, row, column):
        self.expList = expList
        self.row = row
        self.column = column
    
    def compile(self, enviroment):
        exist = None
        if isinstance(self.expList[0],AttAssign):
            if isinstance(self.expList[0].id.id,AccessArray):
                exist = self.expList[0].id.id.compile(enviroment)
            else:
                exist = enviroment.getVariable(self.expList[0].id.id)
        else: 
            exist = self.expList[0].compile(enviroment)
        if exist != None:
            singleId = None
            if isinstance(self.expList[0].id.id,AccessArray):
                singleId = exist
            else:
                singleId = self.expList[0].id.compile(enviroment)
            if len(self.expList) == 1:
                #Se retornan Variables que sean normales, arrays, vectores y structs
                return singleId
            else:
                #Se retornan atributos de structs
                return self.foundAttribute(exist, self.expList, 1, enviroment)
        else:
            listError.append(Error("Error: La variable "+str(self.expList[0].id.id)+"no existe","Local",self.row,self.column,"SEMANTICO"))
    
    def foundAttribute(self, variable, list, number, enviroment):
        if isinstance(list[number].id,CallNative):
            callNativeFunction = Native(Handler(variable.typeVar,variable.value,variable.typeSingle),list[number].id,self.row,self.column)
            return callNativeFunction.compile(enviroment)
        else:
            if list[number].id in variable.value:
                if variable.value[list[number].id].value[0]:
                    typeVar = variable.value[list[number].id].typeVar
                    value = variable.value[list[number].id].value
                    typeSingle = variable.value[list[number].id].typeSingle
                    if (number + 1) == len(list):
                        return Retorno(typeVar,value[1],typeSingle)
                    else:
                        return self.foundAttribute(Retorno(typeVar,value[1],typeSingle), list, number+1, enviroment)
                else:
                    listError.append(Error("Error: El atributo "+str(list[number].id)+" de la instrucción no es público","Local",self.row,self.column,"SEMANTICO"))
                    return None
            else:
                listError.append(Error("Error: Atributo "+str(list[number].id)+" no encontrado de la variable "+str(list[0].id.id),"Local",self.row,self.column,"SEMANTICO"))
                return None