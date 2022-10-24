from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Handler():
    def __init__(self, typeIns, typeVar, typeSingle, label, code, temporal, att):
        self.typeIns = typeIns
        self.typeVar = typeVar
        self.typeSingle = typeSingle
        self.label = label
        self.code = code
        self.temporal = temporal
        self.att = att

    def compile(self,enviroment):
        return Retorno(self.typeIns,self.typeVar,self.typeSingle,self.label,self.code,self.temporal,self.att)