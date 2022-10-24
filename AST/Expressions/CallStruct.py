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
        self.row = row
        self.column = column

    def compile(self,enviroment):
        #Buscar struct
        single = self.id.compile(enviroment)
        if(single != None):
            founded = single.att #Nueva ubicación de atributos
            if len(self.parameters) == len(founded):
                temporal = enviroment.generator.generateTemporal()
                CODE = '/* CREANDO STRUCT */\n'
                CODE += f'  {temporal} = HP;\n'
                CODE += f'  HP = HP + {len(self.parameters)};\n'
                for param in range(len(self.parameters)):
                    if self.parameters[param].id == founded[param].id:
                        callExp = self.parameters[param].compile(enviroment)
                        callType = founded[param].compile(enviroment)
                        if callExp != None and callType != None:
                            if callExp.typeVar == callType.typeVar and callExp.typeSingle == callType.typeSingle:
                                temporal2 = enviroment.generator.generateTemporal()
                                CODE += callExp.code
                                CODE += f'  {temporal2} = {temporal} + {param};\n'
                                CODE += f'  Heap[(int) {temporal2}] = {callExp.temporal};\n'
                            else:
                                listError.append(Error("Error: El parámetro no coincide con el tipo de dato declarado en el struct "+str(self.id.idList[0]),"Local",self.row,self.column,"SEMANTICO"))
                                return None
                        else:
                            listError.append(Error("Error: El parámetro o tipo que ha ingresado en el struct "+str(self.id.idList[0])+"es nulo","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    else:
                        listError.append(Error("Error: No coincide el parámetro \'"+str(self.parameters[param].id)+"\' para el struct "+str(self.id.idList[0]),"Local",self.row,self.column,"SEMANTICO"))
                        return None
                return Retorno(None,self.id.idList[-1],TYPE_DECLARATION.STRUCT,None,CODE,temporal,founded)
            else:
                listError.append(Error("Error: El número de atributos del struct "+str(self.id)+"no es el correcto","Local",self.row,self.column,"SEMANTICO"))
                return None