from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class ForIterative():

    def __init__(self, lExp, rExp):
        self.lExp = lExp
        self.rExp = rExp

    def executeInstruction(self,enviroment):
        pass