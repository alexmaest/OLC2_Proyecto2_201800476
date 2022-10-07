from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Arm(Instruccion):
    def __init__(self, expressions, instructions):
        self.expressions = expressions
        self.instructions = instructions

    def executeInstruction(self, enviroment):
        return self.instructions.executeInstruction(enviroment)

    def getExpressions(self):
        return self.expressions