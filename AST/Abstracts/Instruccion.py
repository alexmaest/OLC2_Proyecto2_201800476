from AST.Symbol.Generator import Generator
from abc import ABC, abstractmethod

class Instruccion(ABC):

    @abstractmethod
    def compile(self, enviroment):
        pass