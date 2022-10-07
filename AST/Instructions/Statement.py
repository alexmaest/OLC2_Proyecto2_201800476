from AST.Abstracts.Instruccion import Instruccion
from AST.Symbol.Enviroment import Enviroment
from AST.Symbol.Generator import Generator

class Statement(Instruccion):
    def __init__(self, instructions):
        self.instructions = instructions
        self.newEnv = None

    def compile(self, enviroment):
        self.newEnv = Enviroment(enviroment.generator, enviroment)
        CODE = ''
        for line in self.instructions:
            instruction = line.compile(self.newEnv)
            if instruction != None:
                CODE += instruction
        return CODE