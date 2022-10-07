from AST.Abstracts.Expression import Expression
from AST.Instructions.Modulo import Modulo
from AST.Instructions.Struct import Struct
from AST.Instructions.Function import Function
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class AccessInstruction():
    def __init__(self, idList, row, column):
        self.idList = idList
        self.row = row
        self.column = column

    def executeInstruction(self, enviroment):
        if len(self.idList) == 1:
            if self.idList == '_': return None
            value = enviroment.getStruct(self.idList[0])
            if(value == None):
                listError.append(Error("Error: El struct "+str(self.idList[0])+" no existe","Local",self.row,self.column,"SEMANTICO"))
                return None
            else:
                return Retorno(self.idList[0],value.attributes,TYPE_DECLARATION.STRUCT)
        else:
            value = enviroment.getModule(self.idList[0])
            if(value == None):
                listError.append(Error("Error: El módulo "+str(self.idList[0])+"no existe","Local",self.row,self.column,"SEMANTICO"))
                return None
            else:
                return self.searchInstruction(value.instructions.instructions, 1)

    def searchInstruction(self, insList, number):
        for single in insList:
            if single.instruction.id == self.idList[number]:
                if single.isPublic:
                    if isinstance(single.instruction,Struct):
                        if (number + 1) == len(self.idList):
                            return Retorno(single.instruction.id,single.instruction.attributes,TYPE_DECLARATION.STRUCT)
                        else:
                            listError.append(Error("Error: No se puede acceder a un atributo de un struct para devolver un tipo de dato","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    elif isinstance(single.instruction,Modulo):
                        if (number + 1) == len(self.idList):
                            listError.append(Error("Error: Un modulo no es un tipo de dato, debe de acceder a uno de sus atributos que sean structs","Local",self.row,self.column,"SEMANTICO"))
                            return None
                        else:
                            return self.searchInstruction(single.instruction.instructions.instructions, number+1)
                    else:
                        #Función
                        listError.append(Error("Error: No se puede acceder a una función de un struct para devolver un tipo de dato","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: El atributo "+str(self.idList[number])+" de la instrucción "+str(self.idList[number-1])+" no es público","Local",self.row,self.column,"SEMANTICO"))
                    return None
            else: continue
        listError.append(Error("Error: El modulo "+str(self.idList[number-1])+" no tiene ningún modulo, struct o función con el nombre "+str(self.idList[number]),"Local",self.row,self.column,"SEMANTICO"))
        return None
