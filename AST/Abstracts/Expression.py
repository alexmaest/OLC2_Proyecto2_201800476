from AST.Symbol.Generator import Generator
from abc import ABC, abstractmethod

class Expression(ABC):

    @abstractmethod
    def obtainValue(self, enviroment):
        pass