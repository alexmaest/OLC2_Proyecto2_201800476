from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from enum import Enum

class TYPE_NATIVE(Enum):
    #Nativas
    TO_STRING = 0,
    TO_OWNED = 1,
    CLONE = 2,
    LEN = 3,
    CAPACITY = 4,
    REMOVE = 5,
    CONTAINS = 6,
    PUSH = 7,
    INSERT = 8,
    CHARS = 9,
    SQRT = 10,
    ABS = 11,
    #Creacion de Arrays
    NEW = 12,
    WITH_CAPACITY = 13

class CallNative():
    def __init__(self, exp, type, row, column):
        self.exp = exp
        self.type = type
        self.row = row
        self.column = column

    def compile(self,enviroment):
        returnedValue = None
        if self.exp != None and self.type != 8:
            if self.type == 5 or self.type == 7:
                returnedValue = self.exp
            else:
                returnedValue = self.exp.compile(enviroment).value
        elif self.type == 8:
            if len(self.exp) == 2:
                returnedValue = []
                returnedValue.append(self.exp[0])
                returnedValue.append(self.exp[1])
            else:
                listError.append(Error("Error: Solo se aceptan 2 parametros en la función insert()","Local",self.row,self.column,"SEMANTICO"))
                return None
        
        if self.type == 0:
            return Retorno(returnedValue,TYPE_NATIVE.TO_STRING,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 1:
            return Retorno(returnedValue,TYPE_NATIVE.TO_OWNED,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 2:
            return Retorno(returnedValue,TYPE_NATIVE.CLONE,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 3:
            return Retorno(returnedValue,TYPE_NATIVE.LEN,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 4:
            return Retorno(returnedValue,TYPE_NATIVE.CAPACITY,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 5:
            return Retorno(returnedValue,TYPE_NATIVE.REMOVE,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 6:
            return Retorno(returnedValue,TYPE_NATIVE.CONTAINS,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 7:
            return Retorno(returnedValue,TYPE_NATIVE.PUSH,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 8:
            return Retorno(returnedValue,TYPE_NATIVE.INSERT,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 9:
            return Retorno(returnedValue,TYPE_NATIVE.CHARS,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 10:
            return Retorno(returnedValue,TYPE_NATIVE.SQRT,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 11:
            return Retorno(returnedValue,TYPE_NATIVE.ABS,TYPE_DECLARATION.NULL,None,None,None,None)
        elif self.type == 12:
            return Retorno(returnedValue,TYPE_NATIVE.NEW,TYPE_DECLARATION.NULL,None,None,None,None)
        else:
            return Retorno(returnedValue,TYPE_NATIVE.WITH_CAPACITY,TYPE_DECLARATION.NULL,None,None,None,None)