from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Symbol.Enviroment import Enviroment
from AST.Instructions.Return import Return
from AST.Instructions.Break import Break
from AST.Instructions.Match import Match
from AST.Instructions.While import While
from AST.Instructions.Loop import Loop
from AST.Instructions.Match import Match
from AST.Instructions.Assignment import Assignment
from AST.Instructions.If import If
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Statement(Instruccion):
    def __init__(self, instructions):
        self.instructions = instructions
        self.isLoopOrFunction = True
        self.isExpSentence = False
        self.insideLoop = False
        self.isMain = False
        self.newEnv = None

    def compile(self, enviroment):
        if self.newEnv == None: self.newEnv = Enviroment(enviroment,enviroment.generator)
        if self.isMain: self.newEnv.size = 0
        returns = []
        CODE = ''
        for line in self.instructions:
            #Compilamos todas las instrucciones
            if (isinstance(line,While) or isinstance(line,If) or isinstance(line,Loop) or isinstance(line,Match)) and self.isExpSentence:
                line.insideLoop = self.insideLoop
                line.isExpSentence = self.isExpSentence
            if (isinstance(line,Return) or isinstance(line,Break)) and self.isExpSentence:
                if not self.isLoopOrFunction and not self.insideLoop: line.isLoopOrFunction = False
                line.isExpSentence = self.isExpSentence
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
                            return None
                else:continue
            else:continue
        #Retornamos los valores
        if len(returns) == 0:return Retorno(None,None,None,None,CODE,None,None)
        else:return Retorno(returns[0].typeIns,returns[0].typeVar,returns[0].typeSingle,returns[0].label,CODE,returns[0].temporal,returns[0].att)