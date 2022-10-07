from AST.Abstracts.Instruccion import Instruccion

class Function(Instruccion):
    def __init__(self, id, parameters, type, statement, row, column):
        self.id = id
        self.parameters = parameters
        self.type = type
        self.statement = statement
        self.generated = False
        self.row = row
        self.column = column

    def compile(self, enviroment):
        #Guardar función
        if enviroment.saveFunction(self.id, self):
            CODE = f'/* INSTRUCCION FUNCION {self.id} */\n'
            CODE += f'void {self.id}(){{\n'
            #Generar codigo de instrucciones
            CODE += self.statement.compile(enviroment)
            CODE += '   return;\n'
            CODE += '}\n'
            self.generated = True
            return CODE
