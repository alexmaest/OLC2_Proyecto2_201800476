from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.AccessTypeVector import AccessTypeVector
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class AccessTypeArray():
    def __init__(self, type, row, column):
        self.type = type
        self.row = row
        self.column = column

    def compile(self, enviroment):
        returned = self.type.compile(enviroment)
        if returned != None:
            if not isinstance(self.type,AccessTypeVector):
                return Retorno(None,returned.typeVar,TYPE_DECLARATION.ARRAY,returned.label,returned.code,returned.temporal,returned.att)
            else:
                listError.append(Error("Error: Un vector no puede ser un tipo de variable para un array","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            return None