from AST.Expressions.Handler import Handler
from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.Access import Access
from AST.Expressions.ParamReference import ParamReference
from AST.Instructions.DeclarationSingle import DeclarationSingle
from AST.Symbol.Enviroment import Enviroment
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class CallStruct():
    def __init__(self, id, parameters, row, column):
        self.id = id
        self.parameters = parameters
        self.content = {}
        self.row = row
        self.column = column

    def executeInstruction(self,enviroment):
        #Buscar struct
        single = self.id.executeInstruction(enviroment)
        self.content = {}
        if(single != None):
            founded = single.value
            if len(self.parameters) == len(founded):
                for param in range(len(self.parameters)):
                    if self.parameters[param].id == founded[param].id:
                        callExp = self.parameters[param].executeInstruction(enviroment)
                        callType = founded[param].executeInstruction(enviroment)
                        if callExp != None and callType != None:
                            if callExp.typeVar == callType.typeVar and callExp.typeSingle == callType.typeSingle:
                                content = []
                                content.append(founded[param].isPublic)
                                content.append(callExp.value)
                                self.content[self.parameters[param].id] = Retorno(callExp.typeVar,content,callExp.typeSingle)
                            else:
                                listError.append(Error("Error: El parámetro no coincide con el tipo de dato declarado en el struct "+str(self.id.idList[0]),"Local",self.row,self.column,"SEMANTICO"))
                                return None
                        else:
                            listError.append(Error("Error: El parámetro o tipo que ha ingresado en el struct "+str(self.id.idList[0])+"es nulo","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    else:
                        listError.append(Error("Error: No coincide el parámetro \'"+str(self.parameters[param].id)+"\' para el struct "+str(self.id.idList[0]),"Local",self.row,self.column,"SEMANTICO"))
                        return None
                return Retorno(self.id.idList[-1],self.content,TYPE_DECLARATION.STRUCT)
            else:
                listError.append(Error("Error: El número de atributos del struct "+str(self.id)+"no es el correcto","Local",self.row,self.column,"SEMANTICO"))
                return None