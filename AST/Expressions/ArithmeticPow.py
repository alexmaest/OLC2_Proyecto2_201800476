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

    def compile(self, enviroment):
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        if self.type == True:
            if lReturn.typeVar == TYPE_DECLARATION.INTEGER and rReturn.typeVar == TYPE_DECLARATION.INTEGER:
                CODE = '/* POW */\n'
                CODE = ''''''
                return Retorno(None,TYPE_DECLARATION.INTEGER,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
            else:
                listError.append(Error("Error: La función pow() solo funciona con ambas expresiones enteras","Local",self.row,self.column,"SEMANTICO"))
        else:
            if lReturn.typeVar == TYPE_DECLARATION.FLOAT and rReturn.typeVar == TYPE_DECLARATION.FLOAT:
                CODE = '/* POW */\n'
                CODE = ''''''
                return Retorno(None,TYPE_DECLARATION.FLOAT,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
            else:
                listError.append(Error("Error: La función powf() solo funciona con ambas expresiones decimales","Local",self.row,self.column,"SEMANTICO"))
