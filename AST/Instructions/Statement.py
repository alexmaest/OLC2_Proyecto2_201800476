from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Symbol.Enviroment import Enviroment
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Statement(Instruccion):
    def __init__(self, instructions):
        self.instructions = instructions
        self.newEnv = None
        self.isMain = False

    def compile(self, enviroment):
        if self.newEnv == None: self.newEnv = Enviroment(enviroment,enviroment.generator)
        if self.isMain: self.newEnv.size = 0
        returns = []
        CODE = ''
        for line in self.instructions:
            #Compilamos todas las instrucciones
            instruction = line.compile(self.newEnv)
            if instruction != None:
                CODE += instruction.code
                #Comprobamos si hay un retorno
                if instruction.typeIns != None and instruction.typeIns != TYPE_DECLARATION.CONTINUE:
                    if len(returns) == 0: returns.append(instruction)
                    else:
                        if returns[0].typeVar == instruction.typeVar and returns[0].typeSingle == instruction.typeSingle: pass
                        else: 
                            listError.append(Error("Error: El tipo de dato de la sentencia de transferencia no es el correcto","Local",self.row,self.column,"SEMANTICO"))
                            returns = []
                            CODE = ''
                            break
                else:continue
            else:continue
        #Retornamos los valores
        if len(returns) == 0:
            return Retorno(None,None,None,None,CODE,None,None)
        else:
            return Retorno(None,returns[0].typeVar,returns[0].typeSingle,None,CODE,None,returns[0].att)