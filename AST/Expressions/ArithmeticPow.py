from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import math

class ArithmeticPow():

    def __init__(self, type, lExp, rExp, row, column):
        self.type = type
        self.lExp = lExp
        self.rExp = rExp
        self.row = row
        self.column = column

    def executeInstruction(self, enviroment):
        lReturn = self.lExp.executeInstruction(enviroment)
        rReturn = self.rExp.executeInstruction(enviroment)
        if self.type == True:
            if lReturn.typeVar == TYPE_DECLARATION.INTEGER and rReturn.typeVar == TYPE_DECLARATION.INTEGER:
                return Retorno(TYPE_DECLARATION.INTEGER,int(math.pow(lReturn.value,rReturn.value)),TYPE_DECLARATION.SIMPLE)
            else:
                listError.append(Error("Error: La función pow() solo funciona con ambas expresiones enteras","Local",self.row,self.column,"SEMANTICO"))
        else:
            if lReturn.typeVar == TYPE_DECLARATION.FLOAT and rReturn.typeVar == TYPE_DECLARATION.FLOAT:
                return Retorno(TYPE_DECLARATION.FLOAT,float(math.pow(lReturn.value,rReturn.value)),TYPE_DECLARATION.SIMPLE)
            else:
                listError.append(Error("Error: La función powf() solo funciona con ambas expresiones decimales","Local",self.row,self.column,"SEMANTICO"))
