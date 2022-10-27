from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Expressions.AccessArray import AccessArray
from AST.Expressions.AttAccess import AttAccess
from AST.Expressions.Literal import Literal
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import tkinter
import re

from AST.Symbol.Symbol import Symbol

class Print(Instruccion):
    def __init__(self, expList, row, column):
        self.expList = expList
        self.row = row
        self.column = column
        self.text = ""

    def compile(self, enviroment):
        self.text = ""
        if len(self.expList) > 1:
            returned = self.expList[0].compile(enviroment)
            if returned != None:
                if returned.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if returned.typeVar == TYPE_DECLARATION.aSTRING or returned.typeVar == TYPE_DECLARATION.aSTRING:
                        result = re.findall('\{\}|\{\:\?\}',self.expList[0].value)
                        if len(self.expList) - 1 == len(result):
                            temporal = enviroment.generator.generateTemporal()
                            complete = self.expList[0].value
                            #Generando texto de la instrucción
                            CODE = "/* PRINT */\n"
                            CODE += f'  {temporal} = HP;\n'
                            auxResult = re.split('\{\}|\{\:\?\}',complete)
                            for i in range(len(result)):
                                self.text = ""
                                returnedSingle = self.expList[i+1].compile(enviroment)
                                if returnedSingle != None:
                                    if result[i] == '{}':
                                        if returnedSingle.typeSingle == TYPE_DECLARATION.SIMPLE:
                                            CODE += returnedSingle.code
                                            singleString = Literal(auxResult[i],2).compile(enviroment)
                                            CODE += self.printString(enviroment, singleString)       
                                            CODE += self.printValue(enviroment,returnedSingle)
                                            if(i+1)==(len(result)):
                                                singleString = Literal(auxResult[-1],2).compile(enviroment)
                                                CODE += self.printString(enviroment, singleString)       
                                            else:pass
                                        else:
                                            listError.append(Error("Error: Ha ingresado un valor que no es simple en \'{ }\' de la instrucción print","Local",self.row,self.column,"SEMANTICO"))
                                            return None
                                    else:
                                        if returnedSingle.typeSingle == TYPE_DECLARATION.ARRAY:
                                            if isinstance(self.expList[i+1],AttAccess):
                                                array = None
                                                access = False
                                                if isinstance(self.expList[i+1].expList[0].id.id,AccessArray):
                                                    access = True
                                                    array = Symbol(returnedSingle.typeVar,None,returnedSingle.typeSingle,None,returnedSingle.temporal,None,None,self.expList[i+1].expList[0].id.id.dimensions,None,None)
                                                else:array = enviroment.getVariable(self.expList[i+1].expList[0].id.id)
                                                if array != None:
                                                    temporal = enviroment.generator.generateTemporal()
                                                    temporal2 = enviroment.generator.generateTemporal()
                                                    CODE += returnedSingle.code
                                                    singleString = Literal(auxResult[i],2).compile(enviroment)
                                                    CODE += self.printString(enviroment, singleString)       
                                                    CODE += '/* IMPRIMIENDO ARRAY */\n'
                                                    if access:
                                                        CODE += f'  {temporal2} = {array.relativePosition};\n'
                                                    else:
                                                        CODE += f'  {temporal} = {array.relativePosition};\n'
                                                        CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                                                    CODE += self.printArray(enviroment, array, temporal2, 1, False)
                                                    if(i+1)==(len(result)):
                                                        singleString = Literal(auxResult[-1],2).compile(enviroment)
                                                        CODE += self.printString(enviroment, singleString)       
                                                    else:pass
                                                else:return None
                                        elif returnedSingle.typeSingle == TYPE_DECLARATION.VECTOR:
                                            if isinstance(self.expList[i+1],AttAccess):
                                                vector = enviroment.getVariable(self.expList[i+1].expList[0].id.id)
                                                if vector != None:
                                                    temporal = enviroment.generator.generateTemporal()
                                                    temporal2 = enviroment.generator.generateTemporal()
                                                    CODE += returnedSingle.code
                                                    singleString = Literal(auxResult[i],2).compile(enviroment)
                                                    CODE += self.printString(enviroment, singleString)       
                                                    CODE += '/* IMPRIMIENDO VECTOR */\n'
                                                    CODE += f'  {temporal} = {vector.relativePosition};\n'
                                                    CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                                                    CODE += self.printArray(enviroment, vector, temporal2, 1 ,True)
                                                    if(i+1)==(len(result)):
                                                        singleString = Literal(auxResult[-1],2).compile(enviroment)
                                                        CODE += self.printString(enviroment, singleString)       
                                                    else:pass
                                                else:return None
                                        elif returnedSingle.typeSingle == TYPE_DECLARATION.STRUCT:
                                            listError.append(Error("Error: No puede imprimir un struct, únicamente sus atributos","Local",self.row,self.column,"SEMANTICO"))
                                            return None
                                        else:
                                            listError.append(Error("Error: Ha ingresado un valor simple en \'{:?}\' de la instrucción print","Local",self.row,self.column,"SEMANTICO"))
                                            return None
                                else:
                                    listError.append(Error("Error: Una de las expresiones que ha ingresado en println es nula","Local",self.row,self.column,"SEMANTICO"))
                                    return None
                            CODE += f'  printf(\"%c\",(char) 10);\n'
                            return Retorno(None,None,None,None,CODE,None,None)
                        else:listError.append(Error("Error: No ha ingresado el número de expresiones correctas en función de los \'{ }\' que ha escrito","Local",self.row,self.column,"SEMANTICO"))
                    else:listError.append(Error("Error: Solo se puede imprimir una cadena como primera instrucctión de un println","Local",self.row,self.column,"SEMANTICO"))
                else:listError.append(Error("Error: Solo se puede imprimir una cadena como primera instrucctión de un println","Local",self.row,self.column,"SEMANTICO"))
            else:listError.append(Error("Error: No se pudo ejecutar la instrucción println","Local",self.row,self.column,"SEMANTICO"))
        else:
            value = self.expList[0].compile(enviroment)
            if value != None:
                if value.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if value.typeVar == TYPE_DECLARATION.STRING or value.typeVar == TYPE_DECLARATION.aSTRING:
                        CODE = "/* PRINT */\n"
                        CODE += self.printString(enviroment,value)
                        CODE += f'  printf(\"%c\",(char) 10);\n'
                        return Retorno(None,None,None,None,CODE,None,None)
                    else:listError.append(Error("Error: La instrucción println necesita \'{ }\' para imprimir literales que no sean cadenas","Local",self.row,self.column,"SEMANTICO"))
                else:listError.append(Error("Error: La instrucción println necesita \'{:?}\' para imprimir arrays o vectores","Local",self.row,self.column,"SEMANTICO"))
            else:listError.append(Error("Error: No se pudo ejecutar la instrucción println","Local",self.row,self.column,"SEMANTICO"))

    def printValue(self, enviroment, value):
        CODE = ''
        if value.typeVar == TYPE_DECLARATION.INTEGER or value.typeVar == TYPE_DECLARATION.USIZE: 
            CODE = f'  printf(\"%d\",(int) {value.temporal});\n'
        elif value.typeVar == TYPE_DECLARATION.FLOAT:
            CODE = f'  printf(\"%f\",(float) {value.temporal});\n'
        elif value.typeVar == TYPE_DECLARATION.CHAR:
            CODE = f'  printf(\"%c\",(char) {value.temporal});\n'
        elif value.typeVar == TYPE_DECLARATION.BOOLEAN:
            CODE = self.printBool(enviroment, value)
        else: #STRING y aSTRING
            CODE = self.printString(enviroment, value)
        return CODE

    def printString(self, enviroment, value):
        temporal = enviroment.generator.generateTemporal()
        caracter = enviroment.generator.generateTemporal()
        cycleLabel = enviroment.generator.generateLabel()
        exitLabel = enviroment.generator.generateLabel()
        CODE = value.code
        CODE += f'  {temporal} = {value.temporal};\n'
        CODE += f'{cycleLabel}: \n'
        CODE += f'  {caracter} = Heap[(int) {temporal}];\n'
        CODE += f'  if({caracter} == 0) goto {exitLabel};\n'
        CODE += f'  printf(\"%c\",(char) {caracter});\n'
        CODE += f'  {temporal} = {temporal} + 1;\n'
        CODE += f'  goto {cycleLabel};\n'
        CODE += f'{exitLabel}: \n'
        return CODE

    def printBool(self, enviroment, value):
        temporal = enviroment.generator.generateTemporal()
        trueLabel = enviroment.generator.generateLabel()
        falseLabel = enviroment.generator.generateLabel()
        exitLabel = enviroment.generator.generateLabel()
        CODE = value.code
        CODE += f'  {temporal} = {value.temporal};\n'
        CODE += f'  if({temporal} == 1) goto {trueLabel};\n'
        CODE += f'  goto {falseLabel};\n'
        CODE += f'{trueLabel}:\n'
        CODE += f'  printf(\"%c\",(char) 84); /*T*/\n'
        CODE += f'  printf(\"%c\",(char) 114); /*r*/\n'
        CODE += f'  printf(\"%c\",(char) 117); /*u*/\n'
        CODE += f'  printf(\"%c\",(char) 101); /*e*/\n'
        CODE += f'  goto {exitLabel};\n'
        CODE += f'{falseLabel}:\n'
        CODE += f'  printf(\"%c\",(char) 70); /*F*/\n'
        CODE += f'  printf(\"%c\",(char) 97); /*a*/\n'
        CODE += f'  printf(\"%c\",(char) 108); /*l*/\n'
        CODE += f'  printf(\"%c\",(char) 115); /*s*/\n'
        CODE += f'  printf(\"%c\",(char) 101); /*e*/\n'
        CODE += f'{exitLabel}:\n'
        return CODE

    def printArray(self, enviroment, array, temporal, number, isVector):
        temporal3 = enviroment.generator.generateTemporal()
        temporal4 = enviroment.generator.generateTemporal()
        temporal5 = enviroment.generator.generateTemporal()
        temporal6 = enviroment.generator.generateTemporal()
        temporal7 = enviroment.generator.generateTemporal()
        label = enviroment.generator.generateLabel()
        label2 = enviroment.generator.generateLabel()
        label3 = enviroment.generator.generateLabel()
        label4 = enviroment.generator.generateLabel()
        CODE = ''
        if number != len(array.dimensions):
            CODE += f'  {temporal3} = Heap[(int) {temporal}];\n'
            CODE += f'  printf(\"%c\",(char) 91);\n'
            CODE += f'  {temporal4} = 0;\n'
            CODE += f'{label}:\n'
            CODE += f'  if({temporal4} != {temporal3}) goto {label2};\n'
            CODE += f'  goto {label3};\n'
            CODE += f'{label2}:\n'
            if isVector: CODE += f'  {temporal5} = {temporal4} + 2;\n'
            else: CODE += f'  {temporal5} = {temporal4} + 1;\n'
            CODE += f'  {temporal6} = {temporal5} + {temporal};\n'
            CODE += f'  {temporal7} = Heap[(int) {temporal6}];\n'
            CODE += self.printArray(enviroment, array, temporal7, (number+1), False)
            CODE += f'  {temporal4} = {temporal4} + 1;\n'
            CODE += f'  if({temporal4} == {temporal3}) goto {label3};\n'
            CODE += f'  goto {label4};\n'
            CODE += f'{label4}:\n'
            CODE += f'  printf(\"%c\",(char) 44);\n'
            CODE += f'  goto {label};\n'
            CODE += f'{label3}:\n'
            CODE += f'  printf(\"%c\",(char) 93);\n'
        else:
            CODE += f'  {temporal3} = Heap[(int) {temporal}];\n'
            CODE += f'  printf(\"%c\",(char) 91);\n'
            CODE += f'  {temporal4} = 0;\n'
            CODE += f'{label}:\n'
            CODE += f'  if({temporal4} != {temporal3}) goto {label2};\n'
            CODE += f'  goto {label3};\n'
            CODE += f'{label2}:\n'
            if isVector: CODE += f'  {temporal5} = {temporal4} + 2;\n'
            else: CODE += f'  {temporal5} = {temporal4} + 1;\n'
            CODE += f'  {temporal6} = {temporal5} + {temporal};\n'
            CODE += f'  {temporal7} = Heap[(int) {temporal6}];\n'
            CODE += self.printValue(enviroment,Retorno(None,array.typeVar,array.typeSingle,None,"",temporal7,None))
            CODE += f'  {temporal4} = {temporal4} + 1;\n'
            CODE += f'  if({temporal4} == {temporal3}) goto {label3};\n'
            CODE += f'  goto {label4};\n'
            CODE += f'{label4}:\n'
            CODE += f'  printf(\"%c\",(char) 44);\n'
            CODE += f'  goto {label};\n'
            CODE += f'{label3}:\n'
            CODE += f'  printf(\"%c\",(char) 93);\n'
        return CODE