from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Continue(Instruccion):
    def __init__(self):
        pass
    
    def executeInstruction(self, enviroment):
        return Retorno(None,None,TYPE_DECLARATION.CONTINUE)