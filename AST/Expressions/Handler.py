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
        self.id = id
        self.dimensions = None
        self.trueLabel = ''
        self.falseLabel = ''

    def compile(self,enviroment):
        value = Retorno(self.typeIns,self.typeVar,self.typeSingle,self.label,self.code,self.temporal,self.att)
        value.trueLabel = self.trueLabel
        value.falseLabel = self.falseLabel
        value.dimensions = self.dimensions
        return value