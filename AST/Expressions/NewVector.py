from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.NewArray import NewArray
from AST.Expressions.NewDefaultArray import NewDefaultArray

class NewVector():

    def __init__(self, list):
        self.list = list
        self.dimensions = []

    def compile(self,enviroment):
        if isinstance(self.list,NewArray) or isinstance(self.list,NewDefaultArray): self.list.isVector = True
        vector = self.list.compile(enviroment)
        if isinstance(self.list,NewArray) or isinstance(self.list,NewDefaultArray): self.dimensions = self.list.dimensions
        print(self.dimensions)
        if vector != None: return Retorno(vector.typeIns,vector.typeVar,TYPE_DECLARATION.VECTOR,vector.label,vector.code,vector.temporal,vector.att)        
        else: return None