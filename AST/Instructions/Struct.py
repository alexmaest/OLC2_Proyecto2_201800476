from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Struct(Instruccion):
    def __init__(self, id, attributes, row, column):
        self.id = id
        self.attributes = attributes
        self.row = row
        self.column = column

    def executeInstruction(self, enviroment):
        #Guardar struct
        enviroment.saveStruct(self.id, self)