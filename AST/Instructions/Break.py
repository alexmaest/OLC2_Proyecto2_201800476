from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Break(Instruccion):
    def __init__(self, exp, row, column):
        self.exp = exp
        self.isExpSentence = False
        self.row = row
        self.column = column
    
    def compile(self, enviroment):
        if self.exp != None:
            returned = self.exp.compile(enviroment)
            if returned != None:
                if self.isExpSentence:
                    CODE = '/* BREAK */\n'
                    CODE += returned.code
                    CODE += f'  goto BreakLabel;\n'
                    return Retorno(TYPE_DECLARATION.BREAK,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)
                else:
                    temporal = enviroment.generator.generateTemporal()
                    CODE = '/* BREAK */\n'
                    CODE += returned.code
                    CODE += f'  {temporal} = SP;\n'
                    CODE += f'  Stack[(int){temporal}] = {returned.temporal};\n'
                    CODE += f'  goto BreakLabel;\n'
                    return Retorno(TYPE_DECLARATION.BREAK,returned.typeVar,returned.typeSingle,returned.label,CODE,temporal,returned.att)
            else:
                listError.append(Error("Error: El break no es valido","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            CODE = '/* BREAK */\n'
            CODE += f'  goto BreakLabel;\n'
            return Retorno(TYPE_DECLARATION.BREAK,None,None,None,CODE,None,None)