from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
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
                size = enviroment.size
                if exp.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if enviroment.saveVariable(Symbol(exp.typeVar,self.assignation.idList[0].id.id,exp.value,exp.typeSingle,self.mutable,size,False,self.row,self.column)):
                        temporal = enviroment.generator.generateTemporal()
                        CODE = "/* DECLARACIÓN */\n"
                        CODE += exp.code
                        CODE += f'  {temporal} = SP + {size}; \n'
                        CODE += f'  Stack[(int) {temporal}] = {exp.temporal};\n'
                        return Retorno(TYPE_DECLARATION.INSTRUCCION,None,None,None,None,CODE,None)
                    else:
                        #Ya se notificó todo
                        return None
                elif exp.typeSingle == TYPE_DECLARATION.ARRAY or exp.typeSingle == TYPE_DECLARATION.VECTOR:
                    if enviroment.saveVariable(Symbol(exp.typeVar,self.assignation.idList[0].id.id,exp.value,exp.typeSingle,self.mutable,size,True,self.row,self.column)):
                        temporal = enviroment.generator.generateTemporal()
                        CODE = "/* DECLARACIÓN */\n"
                        CODE += exp.code
                        CODE += f'  {temporal} = SP + {size}; \n'
                        CODE += f'  Stack[(int) {temporal}] = {exp.temporal};\n'
                        return Retorno(TYPE_DECLARATION.INSTRUCCION,None,None,None,None,CODE,None)
                    else:
                        #Ya se notificó todo
                        return None
        else:
            listError.append(Error("Error: La variable no ha podido ser declarada","Local",self.row,self.column,"SEMANTICO"))