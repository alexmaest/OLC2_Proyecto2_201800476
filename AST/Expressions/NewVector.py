from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class NewVector():

    def __init__(self, list):
        self.list = list

    def executeInstruction(self,enviroment):
        vector = self.list.executeInstruction(enviroment)
        if vector != None:
            if vector.typeVar == None:
                values = []
                values.append(vector.value)
                values.append([])
                return Retorno(None, values, TYPE_DECLARATION.VECTOR)        
            else:
                values = []
                values.append(len(vector.value) + 2)
                values.append(vector.value) 
                return Retorno(vector.typeVar, values, TYPE_DECLARATION.VECTOR)        
        else: return None    