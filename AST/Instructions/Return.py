from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Return(Instruccion):
    def __init__(self, exp, row, column):
        self.exp = exp
        self.isExpSentence = False
        self.isLoopOrFunction = True
        self.row = row
        self.column = column
    
    def compile(self, enviroment):
        if self.exp != None:
            returned = self.exp.compile(enviroment)
            if returned != None:
                temporal = enviroment.generator.generateTemporal()
                CODE = '/* RETURN */\n'
                CODE += returned.code
                size = enviroment.size
                if self.isExpSentence: CODE += f'  {temporal} = SP + {size}; \n'
                else: CODE += f'  {temporal} = SP;\n'
                CODE += f'  Stack[(int){temporal}] = {returned.temporal};\n'
                if self.isLoopOrFunction: CODE += f'  goto ReturnLabel;\n'
                return Retorno(TYPE_DECLARATION.RETURN,returned.typeVar,returned.typeSingle,returned.label,CODE,temporal,returned.att)
            else:
                listError.append(Error("Error: El return no es valido","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            CODE = '/* RETURN */\n'
            CODE += f'  goto ReturnLabel;\n'
            return Retorno(TYPE_DECLARATION.RETURN,None,None,None,CODE,None,None)