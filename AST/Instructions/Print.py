from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Expressions.Literal import Literal
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import tkinter
import re

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
                        result = re.findall('\{\}|\{\:\?\}',returned.value)
                        if len(self.expList) - 1 == len(result):
                            temporal = enviroment.generator.generateTemporal()
                            complete = returned.value
                            #Generando texto de la instrucción
                            CODE = "/* PRINT */\n"
                            CODE += f'  {temporal} = HP;\n'
                            auxResult = re.split('\{\}',complete)
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
                                        else:
                                            listError.append(Error("Error: Ha ingresado un valor que no es simple en \'{ }\' de la instrucción print","Local",self.row,self.column,"SEMANTICO"))
                                            break
                                    else:
                                        if returnedSingle.typeSingle == TYPE_DECLARATION.ARRAY:
                                            self.printArray(returnedSingle.value)
                                            complete = re.sub('\{\:\?\}',self.text, complete, 1)
                                        elif returnedSingle.typeSingle == TYPE_DECLARATION.VECTOR:
                                            self.printArray(returnedSingle.value[1])
                                            complete = re.sub('\{\:\?\}',self.text, complete, 1)
                                        elif returnedSingle.typeSingle == TYPE_DECLARATION.STRUCT:
                                            listError.append(Error("Error: No puede imprimir un struct, únicamente sus atributos","Local",self.row,self.column,"SEMANTICO"))
                                            break
                                        else:
                                            listError.append(Error("Error: Ha ingresado un valor simple en \'{:?}\' de la instrucción print","Local",self.row,self.column,"SEMANTICO"))
                                            break
                                else:
                                    listError.append(Error("Error: Una de las expresiones que ha ingresado en println es nula","Local",self.row,self.column,"SEMANTICO"))
                                    break
                            CODE += f'  printf(\"%c\",(char) 10);\n'
                            return Retorno(TYPE_DECLARATION.INSTRUCCION,None,None,None,None,CODE,None)
                        else:
                            listError.append(Error("Error: No ha ingresado el número de expresiones correctas en función de los \'{ }\' que ha escrito","Local",self.row,self.column,"SEMANTICO"))
                    else:
                        listError.append(Error("Error: Solo se puede imprimir una cadena como primera instrucctión de un println","Local",self.row,self.column,"SEMANTICO"))
                else:
                    listError.append(Error("Error: Solo se puede imprimir una cadena como primera instrucctión de un println","Local",self.row,self.column,"SEMANTICO"))
            else:
                listError.append(Error("Error: No se pudo ejecutar la instrucción println","Local",self.row,self.column,"SEMANTICO"))
        else:
            value = self.expList[0].compile(enviroment)
            if value != None:
                if value.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if value.typeVar == TYPE_DECLARATION.STRING or value.typeVar == TYPE_DECLARATION.aSTRING:
                        CODE = "/* PRINT */\n"
                        CODE += self.printString(enviroment,value)
                        return Retorno(TYPE_DECLARATION.INSTRUCCION,None,None,None,None,CODE,None)
                    else:
                        listError.append(Error("Error: La instrucción println necesita \'{ }\' para imprimir literales que no sean cadenas","Local",self.row,self.column,"SEMANTICO"))
                else:
                    listError.append(Error("Error: La instrucción println necesita \'{:?}\' para imprimir arrays o vectores","Local",self.row,self.column,"SEMANTICO"))
            else:
                listError.append(Error("Error: No se pudo ejecutar la instrucción println","Local",self.row,self.column,"SEMANTICO"))

    def printValue(self, enviroment, value):
        CODE = ''
        if value.typeVar == TYPE_DECLARATION.INTEGER or value.typeVar == TYPE_DECLARATION.USIZE: 
            CODE = f'  printf(\"%d\",(int) {value.temporal});\n'
        elif value.typeVar == TYPE_DECLARATION.STRING or value.typeVar == TYPE_DECLARATION.aSTRING:
            singleString = Literal(value.value,2).compile(enviroment)
            CODE = self.printString(enviroment, singleString)
        elif value.typeVar == TYPE_DECLARATION.FLOAT:
            CODE = f'  printf(\"%f\",(float) {value.temporal});\n'
        elif value.typeVar == TYPE_DECLARATION.CHAR:
            CODE = f'  printf(\"%c\",(char) {value.temporal});\n'
        else:
            singleString = Literal(value.value,2).compile(enviroment)
            CODE = self.printString(enviroment, singleString)
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
        CODE += exitLabel + ": \n"
        return CODE

    def printArray(self, array):
        self.text += "["
        for i in range(len(array)):
            if isinstance(array[i].value,list):
                if (i+1) == len(array):
                    if array[i].typeSingle == TYPE_DECLARATION.VECTOR:
                        self.printArray(array[i].value[1])
                    else:
                        self.printArray(array[i].value)
                else:
                    if array[i].typeSingle == TYPE_DECLARATION.VECTOR:
                        self.printArray(array[i].value[1])
                        self.text += ","
                    else:
                        self.printArray(array[i].value)
                        self.text += ","
            else:
                if (i+1) == len(array):
                    self.text += str(array[i].value)
                else: self.text += str(array[i].value) + ", "
        self.text += "]"
