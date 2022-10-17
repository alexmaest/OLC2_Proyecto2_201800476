from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Symbol.Enviroment import Enviroment

class Statement(Instruccion):
    def __init__(self, instructions):
        self.instructions = instructions
        self.newEnv = None
        self.isMain = False

    def compile(self, enviroment):
        if self.newEnv == None:
            self.newEnv = Enviroment(enviroment,enviroment.generator)
        else:pass
        if self.isMain:
            self.newEnv.size = 0
        else:pass
        CODE = ''
        returnTypeIns = TYPE_DECLARATION.INSTRUCCION
        returnTypeVar = None
        returnValue = None
        returnTypeSingle = None
        returnTemporal = None
        for line in self.instructions:
            instruction = line.compile(self.newEnv)
            if instruction != None:
                CODE += instruction.code
                if instruction.typeIns == TYPE_DECLARATION.VALOR:
                    returnTypeIns = instruction.typeIns
                    returnTypeVar = instruction.typeVar
                    returnValue = instruction.value
                    returnTypeSingle = instruction.typeSingle
                    returnTemporal = instruction.temporal
                else:continue
            else:continue
        return Retorno(returnTypeIns,returnTypeVar,returnValue,returnTypeSingle,None,CODE,returnTemporal)