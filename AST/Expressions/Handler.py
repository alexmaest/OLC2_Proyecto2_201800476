from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Handler():
    def __init__(self, typeIns, typeVar, value, typeSingle, label, code, temporal):
        self.typeIns = typeIns
        self.typeVar = typeVar
        self.value = value
        self.typeSingle = typeSingle
        self.label = label
        self.code = code
        self.temporal = temporal

    def compile(self,enviroment):
        return Retorno(self.typeIns,self.typeVar,self.value,self.typeSingle,self.label,self.code,self.temporal)