from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class If(Instruccion):
    def __init__(self, condition, statement, other, row, column):
        self.condition = condition
        self.isExpSentence = False
        self.insideLoop = False
        self.statement = statement
        self.other = other
        self.row = row
        self.column = column

    def compile(self, enviroment):
        #Se compila la condicion y se asignan las etiquetas
        trueLabel = enviroment.generator.generateLabel()
        falseLabel = enviroment.generator.generateLabel()
        self.condition.trueLabel = trueLabel
        self.condition.falseLabel = falseLabel
        condition = self.condition.compile(enviroment)
        if condition != None:
            if condition.typeVar == TYPE_DECLARATION.BOOLEAN:
                #Generamos codigo de las instrucciones
                exitLabel = enviroment.generator.generateLabel()
                if self.isExpSentence: 
                    self.statement.insideLoop = self.insideLoop
                    self.statement.isLoopOrFunction = False
                    self.statement.isExpSentence = True
                returned = self.statement.compile(enviroment)
                CODE = "/* IF */\n"
                CODE += condition.code
                CODE += f'{trueLabel}: \n'
                CODE += returned.code
                CODE += f'  goto {exitLabel};\n'
                CODE += f'{falseLabel}: \n'
                #Comprobamos si hay un Else if o Else
                if self.other != None:
                    if self.isExpSentence:self.other.isExpSentence = True
                    returned2 = self.other.compile(enviroment)
                    CODE += returned2.code
                #Se añade la etiqueta de salida
                CODE += f'{exitLabel}:\n'
                return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)
            else:listError.append(Error("Error: La condición no es un booleano","Local",self.row,self.column,"SEMANTICO"))