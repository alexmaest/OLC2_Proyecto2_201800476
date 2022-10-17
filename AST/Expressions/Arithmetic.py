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
        [TYPE_DECLARATION.USIZE, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL, TYPE_DECLARATION.NULL],
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
                if typeResult == TYPE_DECLARATION.INTEGER or typeResult == TYPE_DECLARATION.USIZE or typeResult == TYPE_DECLARATION.FLOAT or typeResult == TYPE_DECLARATION.STRING:
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
        CODE = ''
        temporal = enviroment.generator.generateTemporal()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        if typeResult == TYPE_DECLARATION.INTEGER or typeResult == TYPE_DECLARATION.USIZE or typeResult == TYPE_DECLARATION.FLOAT:
            CODE += lReturn.code + '\n'
            CODE += rReturn.code + '\n'
            CODE += f'{temporal} = {lReturn.temporal} + {rReturn.temporal};\n'
            return Retorno(TYPE_DECLARATION.VALOR,typeResult,lReturn.value + rReturn.value,TYPE_DECLARATION.SIMPLE,None,CODE,temporal)
        else:
            CODE += lReturn.code + '\n'
            CODE += rReturn.code + '\n'
            CODE += f'{temporal} = HP;\n'
            CODE += Literal(lReturn,2).compile(enviroment)
            CODE += Literal(rReturn,2).compile(enviroment)
            CODE += f'Heap[HP] = 0;\n'
            CODE += f'HP = HP + 1;\n'
            return Retorno(TYPE_DECLARATION.VALOR,typeResult,str(lReturn.value) + str(rReturn.value),TYPE_DECLARATION.SIMPLE,None,CODE,temporal)

    def operateSub(self, enviroment, typeResult, singleReturn):
        CODE = ''
        if singleReturn != None:
            temporal = enviroment.generator.generateTemporal()
            temporal2 = enviroment.generator.generateTemporal()
            lReturn = self.lExp.compile(enviroment)
            rReturn = self.rExp.compile(enviroment)
            CODE += singleReturn.code + '\n'
            CODE += f'{temporal} = -1;\n'
            CODE += f'{temporal2} = {singleReturn.temporal} * {temporal};\n'
            return Retorno(TYPE_DECLARATION.VALOR,typeResult,singleReturn.value * -1, TYPE_DECLARATION.SIMPLE,None,CODE,temporal2)
        else:
            temporal = enviroment.generator.generateTemporal()
            lReturn = self.lExp.compile(enviroment)
            rReturn = self.rExp.compile(enviroment)
            CODE += lReturn.code + '\n'
            CODE += rReturn.code + '\n'
            CODE += f'{temporal} = {lReturn.temporal} - {rReturn.temporal};\n'
            return Retorno(TYPE_DECLARATION.VALOR,typeResult,lReturn.value - rReturn.value,TYPE_DECLARATION.SIMPLE,None,CODE,temporal)

    def operateMul(self, enviroment, typeResult):
        CODE = ''
        temporal = enviroment.generator.generateTemporal()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        CODE += lReturn.code + '\n'
        CODE += rReturn.code + '\n'
        CODE += f'{temporal} = {lReturn.temporal} * {rReturn.temporal};\n'
        return Retorno(TYPE_DECLARATION.VALOR,typeResult, lReturn.value * rReturn.value,TYPE_DECLARATION.SIMPLE,None,CODE,temporal)

    def operateDiv(self, enviroment, typeResult):
        CODE = '/* VALIDACION DE DIVISION ENTRE 0 */\n'
        temporal = enviroment.generator.generateTemporal()
        trueLabel = enviroment.generator.generateLabel()
        falseLabel = enviroment.generator.generateLabel()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        if typeResult == TYPE_DECLARATION.INTEGER or TYPE_DECLARATION.USIZE:
            CODE += lReturn.code + '\n'
            CODE += rReturn.code + '\n'
            CODE += f'if({rReturn.temporal} != 0) goto {trueLabel};\n'
            CODE += f'{trueLabel}:\n'
            CODE += f'{temporal} = {lReturn.temporal} / {rReturn.temporal};\n'
            CODE += f'{falseLabel}:\n'
            if rReturn.value == 0:
                listError.append(Error("Error: No se puede dividir entre cero","Local",self.row,self.column,"SEMANTICO"))
                return None
            return Retorno(TYPE_DECLARATION.VALOR,typeResult,int(lReturn.value / rReturn.value),TYPE_DECLARATION.SIMPLE,None,CODE,temporal)
        else:
            CODE += lReturn.code + '\n'
            CODE += rReturn.code + '\n'
            CODE += f'if({rReturn.temporal} != 0.0): goto {trueLabel};\n'
            CODE += f'{trueLabel}:\n'
            CODE += f'{temporal} = {lReturn.temporal} / {rReturn.temporal};\n'
            CODE += f'{falseLabel}:\n'
            if rReturn.value == 0.0:
                listError.append(Error("Error: No se puede dividir entre cero","Local",self.row,self.column,"SEMANTICO"))
                return None
            return Retorno(TYPE_DECLARATION.VALOR,typeResult,float(lReturn.value / rReturn.value),TYPE_DECLARATION.SIMPLE,None,CODE,temporal)

    def operateMod(self, enviroment, typeResult):
        CODE = ''
        temporal = enviroment.generator.generateTemporal()
        lReturn = self.lExp.compile(enviroment)
        rReturn = self.rExp.compile(enviroment)
        CODE += lReturn.code + '\n'
        CODE += rReturn.code + '\n'
        CODE += f'{temporal} = {lReturn.temporal} % {rReturn.temporal};\n'
        return Retorno(TYPE_DECLARATION.VALOR,typeResult,lReturn.value % rReturn.value,TYPE_DECLARATION.SIMPLE,None,CODE,temporal)