from abc import ABC, abstractmethod

class Instruccion(ABC):

    @abstractmethod
    def compile(self, enviroment):
        pass