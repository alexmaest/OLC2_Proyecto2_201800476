from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class LiteralType():
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def compile(self,enviroment):
        if self.type == 0:
            return Retorno(TYPE_DECLARATION.INTEGER,self.value,TYPE_DECLARATION.SIMPLE,"","","")
        elif self.type == 1:
            return Retorno(TYPE_DECLARATION.FLOAT,self.value,TYPE_DECLARATION.SIMPLE,"","","")
        elif self.type == 2:
            return Retorno(TYPE_DECLARATION.STRING,self.value,TYPE_DECLARATION.SIMPLE,"","","")
        elif self.type == 3:
            return Retorno(TYPE_DECLARATION.aSTRING,self.value,TYPE_DECLARATION.SIMPLE,"","","")
        elif self.type == 4:
            return Retorno(TYPE_DECLARATION.BOOLEAN,self.value,TYPE_DECLARATION.SIMPLE,"","","")
        elif self.type == 5:
            return Retorno(TYPE_DECLARATION.CHAR,self.value,TYPE_DECLARATION.SIMPLE,"","","")
        elif self.type == 6:
            return Retorno(TYPE_DECLARATION.USIZE,self.value,TYPE_DECLARATION.SIMPLE,"","","")