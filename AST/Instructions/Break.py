from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Break(Instruccion):
    def __init__(self, exp, row, column):
        self.exp = exp
        self.row = row
        self.column = column
    
    def executeInstruction(self, enviroment):
        if self.exp != None:
            returned = self.exp.executeInstruction(enviroment)
            if returned != None:
                return Retorno(returned.typeVar,returned.value,returned.typeSingle)
            else:
                listError.append(Error("Error: El break no es valido","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            return Retorno(None,None,TYPE_DECLARATION.BREAK)