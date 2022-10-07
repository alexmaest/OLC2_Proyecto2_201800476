from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class ListArraySimple(Instruccion):

    def __init__(self, parameters, expression):
        self.parameters = parameters
        self.expression = expression

    def executeInstruction(self, enviroment):
        if isinstance(self.parameters,ListArraySimple):
            returned = self.createArrays(self,enviroment)
            if returned != None:
                return Retorno(returned.typeVar,returned.value,TYPE_DECLARATION.ARRAY)
            else: return None
        else:
            typeVar = self.parameters.executeInstruction(enviroment)
            exp = self.expression.executeInstruction(enviroment)
            if typeVar != None and exp != None:
                list = [0] * exp.value
                return Retorno(typeVar.typeVar,list,TYPE_DECLARATION.ARRAY)
            else: return None

    def createArrays(self,listArray,enviroment):
        exp = listArray.expression.executeInstruction(enviroment)
        if exp != None:
            if isinstance(listArray.parameters,ListArraySimple):
                returned = self.createArrays(listArray.parameters,enviroment)
                list = [returned.value] * exp.value
                return Retorno(returned.typeVar,list,TYPE_DECLARATION.ARRAY)
            else:
                typeVar = listArray.parameters.executeInstruction(enviroment)
                list = [0] * exp.value
                return Retorno(typeVar.typeVar,list,TYPE_DECLARATION.ARRAY)
        else: return None

'''
-[[[i64;2];3];2];
[[[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]]]
-[[i64;3];5]
[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
'''