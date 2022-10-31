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

    def compile(self, enviroment):
        singleExp = self.exp.compile(enviroment)
        singleType = self.type.compile(enviroment)
        if singleExp != None and singleType != None:
            returned = self.CASTING[singleExp.typeVar.value[0]][singleType.typeVar.value[0]]
            if returned != TYPE_DECLARATION.NULL:
                temporal = enviroment.generator.generateTemporal()
                CODE = '/* CASTEO */\n'
                CODE += singleExp.code
                #Integer
                if singleExp.typeVar == TYPE_DECLARATION.INTEGER and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    CODE += f'  {temporal} = (int){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                elif singleExp.typeVar == TYPE_DECLARATION.INTEGER and singleType.typeVar == TYPE_DECLARATION.FLOAT:
                    CODE += f'  {temporal} = (float){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                elif singleExp.typeVar == TYPE_DECLARATION.INTEGER and singleType.typeVar == TYPE_DECLARATION.CHAR:
                    CODE += f'  {temporal} = (char){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                #Usize
                elif singleExp.typeVar == TYPE_DECLARATION.USIZE and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    CODE += f'  {temporal} = (int){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                elif singleExp.typeVar == TYPE_DECLARATION.INTEGER and singleType.typeVar == TYPE_DECLARATION.USIZE:
                    CODE += f'  {temporal} = (int){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                #Float
                if singleExp.typeVar == TYPE_DECLARATION.FLOAT and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    CODE += f'  {temporal} = (int){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                elif singleExp.typeVar == TYPE_DECLARATION.FLOAT and singleType.typeVar == TYPE_DECLARATION.FLOAT:
                    CODE += f'  {temporal} = (float){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                #String
                elif singleExp.typeVar == TYPE_DECLARATION.STRING and singleType.typeVar == TYPE_DECLARATION.STRING:
                    CODE += f'  {temporal} = {singleExp.temporal};//Casteo de string a string se omite\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                #aString
                elif singleExp.typeVar == TYPE_DECLARATION.aSTRING and singleType.typeVar == TYPE_DECLARATION.aSTRING:
                    CODE += f'  {temporal} = {singleExp.temporal};//Casteo de string a &str se omite\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                #Boolean
                elif singleExp.typeVar == TYPE_DECLARATION.BOOLEAN and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    CODE += f'  {temporal} = (int){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                elif singleExp.typeVar == TYPE_DECLARATION.BOOLEAN and singleType.typeVar == TYPE_DECLARATION.BOOLEAN:
                    CODE += f'  {temporal} = {singleExp.temporal};//Casteo de boolean a boolean solo se omite\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                #Char
                elif singleExp.typeVar == TYPE_DECLARATION.CHAR and singleType.typeVar == TYPE_DECLARATION.INTEGER:
                    CODE += f'  {temporal} = (int){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
                else: 
                    #TYPE_DECLARATION.CHAR and TYPE_DECLARATION.CHAR:
                    CODE += f'  {temporal} = (char){singleExp.temporal};\n'
                    return Retorno(None,returned,singleExp.typeSingle,singleExp.label,CODE,temporal,singleExp.att)
            else:listError.append(Error("Error: No se puede realizar un casteo entre "+str(singleExp.typeVar)+" y "+str(singleType.typeVar),"Local",self.row,self.column,"SEMANTICO"))
        else:listError.append(Error("Error: El casteo no ha podido ser realizado","Local",self.row,self.column,"SEMANTICO"))