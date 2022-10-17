from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Continue(Instruccion):
    def __init__(self):
        pass
    
    def compile(self, enviroment):
        CODE = '/* CONTINUE */\n'
        CODE += f'  goto ContinueLabel;\n'
        return Retorno(TYPE_DECLARATION.VALOR,None,None,None,None,CODE,None)