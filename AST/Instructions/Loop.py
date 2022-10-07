from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Loop(Instruccion):
    def __init__(self, statement):
        self.statement = statement

    def compile(self, enviroment):
        returned = self.statement.compile(enviroment)
        loopLabel = enviroment.generator.obtenerEtiqueta()
        CODE = '/* INSTRUCCION LOOP */\n'
        CODE += f'{loopLabel}:\n'
        CODE += self.statement.compile(enviroment)
        CODE += f'  goto {loopLabel};\n'
        return CODE
        '''
        if returned != None:
            if returned.typeSingle == TYPE_DECLARATION.BREAK:
                break
            elif returned.typeSingle == TYPE_DECLARATION.CONTINUE:
                continue
            else:
                return returned
        '''