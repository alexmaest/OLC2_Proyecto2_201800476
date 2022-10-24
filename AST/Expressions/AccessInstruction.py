from AST.Abstracts.Expression import Expression
from AST.Instructions.Modulo import Modulo
from AST.Instructions.Struct import Struct
from AST.Instructions.Function import Function
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Symbol.SymbolList import listStructsAux
from AST.Error.ErrorList import listError

class AccessInstruction():
    def __init__(self, idList, row, column):
        self.idList = idList
        self.isAux = False
        self.row = row
        self.column = column

    def compile(self, enviroment):
        if len(self.idList) == 1:
            if self.idList == '_': return None
            value = None
            if self.isAux:
                value = listStructsAux(self.idList[0])
            else:
                value = enviroment.getStruct(self.idList[0])
            if(value == None):
                listError.append(Error("Error: El struct "+str(self.idList[0])+" no existe","Local",self.row,self.column,"SEMANTICO"))
                return None
            else:return Retorno(None,self.idList[0],TYPE_DECLARATION.STRUCT,None,None,None,value.attributes)
        else:
            value = None
            if self.isAux:
                value = listStructsAux(self.idList[0])
            else:
                value = enviroment.getModule(self.idList[0])
            if(value == None):
                listError.append(Error("Error: El módulo "+str(self.idList[0])+"no existe","Local",self.row,self.column,"SEMANTICO"))
                return None
            elif self.isAux:return self.searchAttribute(value.attributes,0,enviroment)
            else:return self.searchInstruction(value.instructions.instructions,1)

    def searchInstruction(self, insList, number):
        for single in insList:
            if single.instruction.id == self.idList[number]:
                if single.isPublic:
                    if isinstance(single.instruction,Struct):
                        if (number + 1) == len(self.idList):
                            return Retorno(None,single.instruction.id,TYPE_DECLARATION.STRUCT,None,None,None,insList)
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

    def searchAttribute(self, atts, number, enviroment):
        for single in atts:
            if single.id == self.idList[number]:
                if single.isPublic:
                    return single.type.compile(enviroment)
                else:
                    listError.append(Error("Error: El atributo "+str(single.instruction.id)+" no es público","Local",self.row,self.column,"SEMANTICO"))
                    return None
            else: continue
        listError.append(Error("Error: El modulo "+str(self.idList[number-1])+" no tiene ningún modulo, struct o función con el nombre "+str(self.idList[number]),"Local",self.row,self.column,"SEMANTICO"))
        return None
