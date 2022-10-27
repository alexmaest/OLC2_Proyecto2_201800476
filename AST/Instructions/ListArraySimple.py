from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class ListArraySimple(Instruccion):

    def __init__(self, parameters, expression):
        self.parameters = parameters
        self.expression = expression

    def compile(self, enviroment):
        if isinstance(self.parameters,ListArraySimple):
            returned = self.createArrays(self,enviroment)
            if returned != None:
                return Retorno(None,returned.typeVar,TYPE_DECLARATION.ARRAY,None,None,None,None)
            else: return None
        else:
            typeVar = self.parameters.compile(enviroment)
            if typeVar != None:
                return Retorno(None,typeVar.typeVar,TYPE_DECLARATION.ARRAY,None,None,None,None)
            else: return None

    def createArrays(self,listArray,enviroment):
        if isinstance(listArray.parameters,ListArraySimple):
            returned = self.createArrays(listArray.parameters,enviroment)
            return Retorno(None,returned.typeVar,TYPE_DECLARATION.ARRAY,None,None,None,None)
        else:
            typeVar = listArray.parameters.compile(enviroment)
            return Retorno(None,typeVar.typeVar,TYPE_DECLARATION.ARRAY,None,None,None,None)

'''
-[[[i64;2];3];2];
[[[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]]]
-[[i64;3];5]
[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
'''