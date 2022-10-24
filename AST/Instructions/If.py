from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class If(Instruccion):
    def __init__(self, condition, statement, other, row, column):
        self.condition = condition
        self.statement = statement
        self.other = other
        self.row = row
        self.column = column

    def compile(self, enviroment):
        condition = self.condition.compile(enviroment)
        if condition != None:
            if condition.typeVar == TYPE_DECLARATION.BOOLEAN:
                #Generamos codigo de las instrucciones
                exitLabel = enviroment.generator.generateLabel()
                returned = self.statement.compile(enviroment)
                CODE = "/* IF */\n"
                CODE += condition.code
                CODE += f'{condition.trueLabel}: \n'
                CODE += returned.code
                CODE += f'  goto {exitLabel};\n'
                CODE += f'{condition.falseLabel}: \n'
                #Comprobamos si hay un Else if o Else
                if self.other != None:
                    returned2 = self.other.compile(enviroment)
                    CODE += returned2.code
                #Se añade la etiqueta de salida
                CODE += f'{exitLabel}:\n'
                return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,None,CODE,None)
            else:listError.append(Error("Error: La condición no es un booleano","Local",self.row,self.column,"SEMANTICO"))