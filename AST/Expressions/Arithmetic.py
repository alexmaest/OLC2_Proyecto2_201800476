from enum import Enum
from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.Literal import Literal
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class TYPE_OPERATION(Enum):
    SUMA = 1,
    RESTA = 2,
    MULTIPLICACION = 3,
    DIVISION = 4,
    MAYOR = 5,
    MENOR = 6,
    MAYORIGUAL = 7,
    MENORIGUAL = 8,
    DIFERENTE = 9,
    IGUALIGUAL = 10,
    AND = 11,
    OR = 12,
    NOT = 13,
    MODULO = 14

class Arithmetic():

    def __init__(self, lExp, type, rExp, single, row, column):
        self.lExp = lExp
        self.type = type
        self.rExp = rExp
        self.single = single
        self.row = row
        self.column = column

    SUMA = [
        [TYPE_DECLARATION.INTEGER, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.USIZE, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.FLOAT, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.STRING, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.USIZE, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.USIZE, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL]
    ]

    OTHER = [
        [TYPE_DECLARATION.INTEGER, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.USIZE, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.FLOAT, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.USIZE, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.USIZE, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
        [TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL]
    ]

    def compile(self, enviroment):
        lReturn = None
        rReturn = None
        singleReturn = None

        if self.single:
            singleReturn = self.lExp.compile(enviroment)
        else:
            lReturn = self.lExp.compile(enviroment)
            rReturn = self.rExp.compile(enviroment)
        if lReturn != None and rReturn != None or singleReturn != None:
            if self.type == TYPE_OPERATION.SUMA:
                typeResult = Arithmetic.SUMA[lReturn.typeVar.value[0]][rReturn.typeVar.value[0]]
                if typeResult == TYPE_DECLARATION.INTEGER or typeResult == TYPE_DECLARATION.USIZE or typeResult == TYPE_DECLARATION.FLOAT or typeResult == TYPE_DECLARATION.STRING  or typeResult == TYPE_DECLARATION.aSTRING:
                    return self.operateSum(enviroment, typeResult)
                else:
                    listError.append(Error("Error: No se puede operar "+str(lReturn.typeVar)+" con "+str(rReturn.typeVar),"Local",self.row,self.column,"SEMANTICO"))
                    return None

            elif self.type == TYPE_OPERATION.RESTA:
                if self.single:
                    return self.operateSub(enviroment, singleReturn.typeVar, singleReturn)
                else:
                    typeResult = Arithmetic.OTHER[lReturn.typeVar.value[0]][rReturn.typeVar.value[0]]
                    if typeResult == TYPE_DECLARATION.INTEGER or typeResult == TYPE_DECLARATION.USIZE or typeResult == TYPE_DECLARATION.FLOAT:
                        return self.operateSub(enviroment, typeResult, None)
                    else:
                        listError.append(Error("Error: No se puede operar "+str(lReturn.typeVar)+" con "+str(rReturn.typeVar),"Local",self.row,self.column,"SEMANTICO"))
                        return None
            
            elif self.type == TYPE_OPERATION.MULTIPLICACION:
                typeResult = Arithmetic.OTHER[lReturn.typeVar.value[0]][rReturn.typeVar.value[0]]
                if typeResult == TYPE_DECLARATION.INTEGER or typeResult == TYPE_DECLARATION.USIZE or typeResult == TYPE_DECLARATION.FLOAT:
                    return self.operateMul(enviroment,typeResult)
                else:
                    listError.append(Error("Error: No se puede operar "+str(lReturn.typeVar)+" con "+str(rReturn.typeVar),"Local",self.row,self.column,"SEMANTICO"))
                    return None
            
            elif self.type == TYPE_OPERATION.DIVISION:
                typeResult = Arithmetic.OTHER[lReturn.typeVar.value[0]][rReturn.typeVar.value[0]]
                if typeResult == TYPE_DECLARATION.INTEGER or typeResult == TYPE_DECLARATION.USIZE or typeResult == TYPE_DECLARATION.FLOAT:
                    return self.operateDiv(enviroment, typeResult)
                else:
                    listError.append(Error("Error: No se puede operar "+str(lReturn.typeVar)+" con "+str(rReturn.typeVar),"Local",self.row,self.column,"SEMANTICO"))
                    return None
          
            else:
                #MODULO
                if lReturn.typeVar == TYPE_DECLARATION.INTEGER and rReturn.typeVar == TYPE_DECLARATION.INTEGER:
                    return self.operateMod(enviroment,TYPE_DECLARATION.INTEGER)
                elif lReturn.typeVar == TYPE_DECLARATION.FLOAT and rReturn.typeVar == TYPE_DECLARATION.FLOAT:
                    return self.operateMod(enviroment,TYPE_DECLARATION.FLOAT)
                else:
                    listError.append(Error(f"Error: No se puede realizar la operación modulo con "+str(lReturn.typeVar)+" y "+str(rReturn.typeVar),"Local",self.row,self.column,"SEMANTICO"))
                    return None
        else:
            return None

    def operateSum(self, enviroment, typeResult):
        CODE = '/* SUMA */\n'
        temporal = enviroment.generator.generateTemporal()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        if typeResult == TYPE_DECLARATION.INTEGER or typeResult == TYPE_DECLARATION.USIZE or typeResult == TYPE_DECLARATION.FLOAT:
            CODE += lReturn.code
            CODE += rReturn.code
            CODE += f'  {temporal} = {lReturn.temporal} + {rReturn.temporal};\n'
            return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
        else:
            temporal2 = enviroment.generator.generateTemporal()
            temporal3 = enviroment.generator.generateTemporal()
            temporal4 = enviroment.generator.generateTemporal()
            temporal5 = enviroment.generator.generateTemporal()
            label = enviroment.generator.generateLabel()
            label2 = enviroment.generator.generateLabel()
            label3 = enviroment.generator.generateLabel()
            label4 = enviroment.generator.generateLabel()
            label5 = enviroment.generator.generateLabel()
            label6 = enviroment.generator.generateLabel()
            CODE += lReturn.code
            CODE += rReturn.code
            CODE += f'  {temporal} = HP;'
            CODE += f'  {temporal2} = {lReturn.temporal};'
            CODE += f'{label}:\n'
            CODE += f'  {temporal3} = Heap[(int) {temporal2}];'
            CODE += f'  if({temporal3} != 0) goto {label2};\n'
            CODE += f'  goto {label3};\n'
            CODE += f'{label2}:\n'
            CODE += f'  Heap[HP] = {temporal3};'
            CODE += f'  HP = HP + 1;\n'
            CODE += f'  {temporal2} = {temporal2} + 1;\n'
            CODE += f'  goto {label};\n'
            CODE += f'{label3}:\n'
            CODE += f'  {temporal4} = {rReturn.temporal};'
            CODE += f'{label4}:\n'
            CODE += f'  {temporal5} = Heap[(int) {temporal4}];'
            CODE += f'  if({temporal5} != 0) goto {label5};\n'
            CODE += f'  goto {label6};\n'
            CODE += f'{label5}:\n'
            CODE += f'  Heap[HP] = {temporal5};'
            CODE += f'  HP = HP + 1;\n'
            CODE += f'  {temporal4} = {temporal4} + 1;\n'
            CODE += f'  goto {label4};\n'
            CODE += f'{label6}:\n'
            CODE += f'  Heap[HP] = 0;'
            CODE += f'  HP = HP + 1;\n'
            return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)

    def operateSub(self, enviroment, typeResult, singleReturn):
        CODE = '/* RESTA */\n'
        if singleReturn != None:
            temporal = enviroment.generator.generateTemporal()
            temporal2 = enviroment.generator.generateTemporal()
            CODE += singleReturn.code
            CODE += f'  {temporal} = -1;\n'
            CODE += f'  {temporal2} = {singleReturn.temporal} * {temporal};\n'
            return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal2,None)
        else:
            temporal = enviroment.generator.generateTemporal()
            lReturn = self.lExp.compile(enviroment)
            rReturn = self.rExp.compile(enviroment)
            CODE += lReturn.code
            CODE += rReturn.code
            CODE += f'  {temporal} = {lReturn.temporal} - {rReturn.temporal};\n'
            return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)

    def operateMul(self, enviroment, typeResult):
        temporal = enviroment.generator.generateTemporal()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        CODE = '/* MULTIPLICACIÓN */\n'
        CODE += lReturn.code
        CODE += rReturn.code
        CODE += f'  {temporal} = {lReturn.temporal} * {rReturn.temporal};\n'
        return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)

    def operateDiv(self, enviroment, typeResult):
        CODE = '/* DIVISION */\n'
        temporal = enviroment.generator.generateTemporal()
        trueLabel = enviroment.generator.generateLabel()
        falseLabel = enviroment.generator.generateLabel()
        exitLabel = enviroment.generator.generateLabel()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        if typeResult == TYPE_DECLARATION.INTEGER or TYPE_DECLARATION.USIZE:
            CODE += lReturn.code
            CODE += rReturn.code
            CODE += '/* VALIDACION DE DIVISION ENTRE 0 */\n'
            CODE += f'  if({rReturn.temporal} != 0) goto {trueLabel};\n'
            CODE += f'  goto {falseLabel};\n'
            CODE += f'{trueLabel}:\n'
            CODE += f'  {temporal} = {lReturn.temporal} / {rReturn.temporal};\n'
            CODE += f'  goto {exitLabel};\n'
            CODE += f'{falseLabel}:\n'
            CODE += f'  printf("%c",(char) 77); //M\n'
            CODE += f'  printf("%c",(char) 97); //a\n'
            CODE += f'  printf("%c",(char) 116); //t\n'
            CODE += f'  printf("%c",(char) 104); //h\n'
            CODE += f'  printf("%c",(char) 69); //E\n'
            CODE += f'  printf("%c",(char) 114); //r\n'
            CODE += f'  printf("%c",(char) 114); //r\n'
            CODE += f'  printf("%c",(char) 111); //o\n'
            CODE += f'  printf("%c",(char) 114); //r\n'
            CODE += f'  printf("%c",(char) 10);\n'
            CODE += f'{exitLabel}:\n'
            return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
        else:
            CODE += lReturn.code
            CODE += rReturn.code
            CODE += '/* VALIDACION DE DIVISION ENTRE 0 */\n'
            CODE += f'  if({rReturn.temporal} != 0.0) goto {trueLabel};\n'
            CODE += f'  goto {falseLabel};\n'
            CODE += f'{trueLabel}:\n'
            CODE += f'  {temporal} = {lReturn.temporal} / {rReturn.temporal};\n'
            CODE += f'  goto {exitLabel};\n'
            CODE += f'{falseLabel}:\n'
            CODE += f'  printf("%c",(char) 77); //M\n'
            CODE += f'  printf("%c",(char) 97); //a\n'
            CODE += f'  printf("%c",(char) 116); //t\n'
            CODE += f'  printf("%c",(char) 104); //h\n'
            CODE += f'  printf("%c",(char) 69); //E\n'
            CODE += f'  printf("%c",(char) 114); //r\n'
            CODE += f'  printf("%c",(char) 114); //r\n'
            CODE += f'  printf("%c",(char) 111); //o\n'
            CODE += f'  printf("%c",(char) 114); //r\n'
            CODE += f'{exitLabel}:\n'
            return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal)

    def operateMod(self, enviroment, typeResult):
        CODE = '/* MODULO */\n'
        temporal = enviroment.generator.generateTemporal()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        CODE += lReturn.code
        CODE += rReturn.code
        CODE += f'  {temporal} = (int){lReturn.temporal} % (int){rReturn.temporal};\n'
        return Retorno(None,typeResult,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)