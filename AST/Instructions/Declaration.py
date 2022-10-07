from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION
from AST.Symbol.Symbol import Symbol
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Declaration(Instruccion):

    def __init__(self, mutable, assignation, row, column):
        self.mutable = mutable
        self.assignation = assignation
        self.row = row
        self.column = column

    def compile(self, enviroment):
        exp = self.assignation.expression.compile(enviroment)
        if exp != None:
            if exp.typeVar == None and exp.typeSingle == TYPE_DECLARATION.VECTOR:
                listError.append(Error("Error: La variable no ha podido ser declarada porque no posee un tipo para crear un vector","Local",self.row,self.column,"SEMANTICO"))
            else:
                sizeEnv = enviroment.size
                if enviroment.saveVariable(Symbol(exp.typeVar, self.assignation.idList[0].id.id, exp.value, exp.typeSingle, self.mutable, sizeEnv)):
                    temporal = enviroment.generator.obtenerTemporal()
                    CODE = "/* DECLARACIÓN */\n"
                    CODE += exp.code + '\n'
                    CODE += f'  {temporal} = SP + {sizeEnv}; \n'
                    CODE += f'  Stack[(int) {temporal}] = {exp.temporal};\n'
                    return CODE
        else:
            listError.append(Error("Error: La variable no ha podido ser declarada","Local",self.row,self.column,"SEMANTICO"))