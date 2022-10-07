from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class ParamReference():
    def __init__(self, mutable, id, reference):
        self.mutable = mutable
        self.id = id
        self.reference = reference
    
    def executeInstruction(self, enviroment):
        return self.id.executeInstruction(enviroment)