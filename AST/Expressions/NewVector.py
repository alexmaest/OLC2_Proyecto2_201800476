from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.NewArray import NewArray
from AST.Expressions.NewDefaultArray import NewDefaultArray

class NewVector():

    def __init__(self, list):
        self.list = list

    def compile(self,enviroment):
        if isinstance(self.list,NewArray) or isinstance(self.list,NewDefaultArray):
            self.list.isVector = True
        else:pass
        vector = self.list.compile(enviroment)
        if vector != None:
            if vector.typeVar == None:
                values = []
                values.append(vector.value)
                values.append([])
                return Retorno(None,values,TYPE_DECLARATION.VECTOR)        
            else:
                values = []
                values.append(len(vector.value) + 2)
                values.append(vector.value) 
                return Retorno(vector.typeIns,vector.typeVar,values,TYPE_DECLARATION.VECTOR,vector.label,vector.code,vector.temporal)        
        else: return None