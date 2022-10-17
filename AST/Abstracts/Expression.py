from abc import ABC, abstractmethod
from AST.Abstracts.Retorno import Retorno

class Expression(ABC):

    @abstractmethod
    def obtainValue(self, enviroment):
        pass