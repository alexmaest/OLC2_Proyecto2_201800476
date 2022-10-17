from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Return(Instruccion):
    def __init__(self, exp, row, column):
        self.exp = exp
        self.row = row
        self.column = column
    
    def compile(self, enviroment):
        if self.exp != None:
            returned = self.exp.compile(enviroment)
            if returned != None:
                temporal = enviroment.generator.generateTemporal()
                CODE = '/* RETURN */\n'
                CODE += returned.code
                CODE += f'  {temporal} = SP + 0;\n'
                CODE += f'  Stack[(int){temporal}] = {returned.temporal};\n'
                CODE += f'  goto ReturnLabel;\n'
                return Retorno(TYPE_DECLARATION.VALOR,returned.typeVar,returned.value,returned.typeSingle,None,CODE,temporal)
            else:
                listError.append(Error("Error: El return no es valido","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            return None