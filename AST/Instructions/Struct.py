from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Symbol.SymbolList import listStructsAux

class Struct(Instruccion):
    def __init__(self, id, attributes, row, column):
        self.id = id
        self.attributes = attributes
        self.row = row
        self.column = column

    def compile(self, enviroment):
        #Guardar struct
        listStructsAux.append(self)
        enviroment.saveStruct(self.id, self)