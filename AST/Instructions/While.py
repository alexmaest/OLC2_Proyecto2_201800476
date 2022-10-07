from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class While(Instruccion):
    def __init__(self, condition, statement, row, column):
        self.condition = condition
        self.statement = statement
        self.row = row
        self.column = column

    def compile(self, enviroment):
        condition = self.condition.compile(enviroment)
        if condition != None:
            if condition.typeVar == TYPE_DECLARATION.BOOLEAN:
                whileLabel = enviroment.generator.obtenerEtiqueta()
                CODE = '/* INSTRUCCION WHILE */\n'
                CODE += f'{whileLabel}:\n'
                CODE += condition.code
                CODE += f'{condition.trueLabel}: \n'
                CODE += self.statement.compile(enviroment)
                CODE += f'  goto {whileLabel};\n'
                CODE += f'{condition.falseLabel}: \n'
                return CODE
                '''if returned != None:
                    if returned.typeSingle == TYPE_DECLARATION.BREAK:
                        pass
                        #break
                    elif returned.typeSingle == TYPE_DECLARATION.CONTINUE:
                        condition = self.condition.compile(enviroment)
                        pass
                        #continue
                    else:
                        return returned'''
            else:
                listError.append(Error("Error: La condición no es un booleano","Local",self.row,self.column,"SEMANTICO"))
        else:
            listError.append(Error("Error: No se ha podido ejecutar la sentencia While","Local",self.row,self.column,"SEMANTICO"))