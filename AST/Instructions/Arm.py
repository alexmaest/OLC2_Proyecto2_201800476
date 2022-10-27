from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Arm(Instruccion):
    def __init__(self, expressions, instructions):
        self.isExpSentence = False
        self.expressions = expressions
        self.instructions = instructions

    def compile(self, enviroment):
        if self.isExpSentence: self.instructions.isExpSentence = True
        return self.instructions.compile(enviroment)

    def getExpressions(self):
        return self.expressions