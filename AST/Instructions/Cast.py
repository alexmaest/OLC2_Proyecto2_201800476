from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Abstracts.Instruccion import Instruccion
from AST.Symbol.Symbol import Symbol
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Cast(Instruccion):

    def __init__(self, exp, type, row, column):
        self.exp = exp
        self.type = type
        self.row = row
        self.column = column

    CASTING = [
        [TYPE_DECLARATION.INTEGER, TYPE_DECLARATION.FLOAT, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.CHAR, TYPE_DECLARATION.USIZE],
        [TYPE_DECLARATION.INTEGER, TYPE_DECLARATION.FLOAT, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.STRING, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.aSTRING, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.INTEGER, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.BOOLEAN, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.INTEGER, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.CHAR, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.INTEGER, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL]
    ]

    def executeInstruction(self, enviroment):
        singleExp = self.exp.executeInstruction(enviroment)
        singleType = self.type.executeInstruction(enviroment)
        if singleExp != None and singleType != None:
            returned = self.CASTING[singleExp.typeVar.value[0]][singleType.typeVar.value[0]]
            if returned != TYPE_DECLARATION.NULL:
                #Integer
                if singleExp.typeVar == TYPE_DECLARATION.INTEGER and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    return Retorno(returned, singleExp.value,singleExp.typeSingle)
                elif singleExp.typeVar == TYPE_DECLARATION.INTEGER and singleType.typeVar == TYPE_DECLARATION.FLOAT:
                    return Retorno(returned, float(singleExp.value),singleExp.typeSingle)
                elif singleExp.typeVar == TYPE_DECLARATION.INTEGER and singleType.typeVar == TYPE_DECLARATION.CHAR:
                    return Retorno(returned, chr(singleExp.value),singleExp.typeSingle)
                #Float
                if singleExp.typeVar == TYPE_DECLARATION.FLOAT and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    return Retorno(returned, int(singleExp.value),singleExp.typeSingle)
                elif singleExp.typeVar == TYPE_DECLARATION.FLOAT and singleType.typeVar == TYPE_DECLARATION.FLOAT:
                    return Retorno(returned, singleExp.value,singleExp.typeSingle)
                #String
                elif singleExp.typeVar == TYPE_DECLARATION.STRING and singleType.typeVar == TYPE_DECLARATION.STRING:
                    return Retorno(returned, str(singleExp.value),singleExp.typeSingle)
                #aString
                elif singleExp.typeVar == TYPE_DECLARATION.aSTRING and singleType.typeVar == TYPE_DECLARATION.aSTRING:
                    return Retorno(returned, str(singleExp.value),singleExp.typeSingle)
                #Boolean
                elif singleExp.typeVar == TYPE_DECLARATION.BOOLEAN and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    if singleExp.value == True:
                        return Retorno(returned, 1,singleExp.typeSingle)
                    else:
                        return Retorno(returned, 0,singleExp.typeSingle)
                elif singleExp.typeVar == TYPE_DECLARATION.BOOLEAN and singleType.typeVar == TYPE_DECLARATION.BOOLEAN:
                    return Retorno(returned, bool(singleExp.value),singleExp.typeSingle)
                #Char
                elif singleExp.typeVar == TYPE_DECLARATION.CHAR and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    return Retorno(returned, ord(singleExp.value),singleExp.typeSingle)
                else: 
                    #TYPE_DECLARATION.CHAR and TYPE_DECLARATION.CHAR:
                    return Retorno(returned, singleExp.value,singleExp.typeSingle)
            else:
                listError.append(Error("Error: No se puede realizar un casteo entre "+str(singleExp.typeVar)+" y "+str(singleType.typeVar),"Local",self.row,self.column,"SEMANTICO"))
        else:
            listError.append(Error("Error: El casteo no ha podido ser realizado","Local",self.row,self.column,"SEMANTICO"))