from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Symbol.Enviroment import Enviroment
from AST.Expressions.CallNative import CallNative, TYPE_NATIVE
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import math

class Native(Instruccion):
    def __init__(self, value, function, row, column):
        self.value = value
        self.function = function
        self.row = row
        self.column = column

    def executeInstruction(self, enviroment):
        returnedValue = self.value.executeInstruction(enviroment)
        function = self.function.executeInstruction(enviroment)
        if returnedValue != None and function != None:
            if function.typeVar == TYPE_NATIVE.TO_STRING:
                if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if returnedValue.typeVar == TYPE_DECLARATION.STRING or returnedValue.typeVar == TYPE_DECLARATION.aSTRING:
                        return Retorno(TYPE_DECLARATION.STRING,returnedValue.value,TYPE_DECLARATION.SIMPLE)
                    else:
                        listError.append(Error("Error: La función to_string() solo funciona con variables tipo String o &str","Local",self.row,self.column,"SEMANTICO"))
                        return Retorno(TYPE_DECLARATION.NULL,None,TYPE_DECLARATION.SIMPLE)
                else:
                    listError.append(Error("Error: La función to_string() solo funciona con variables tipo String o &str, no con arreglos ni vectores","Local",self.row,self.column,"SEMANTICO"))
                    return Retorno(TYPE_DECLARATION.NULL,None,TYPE_DECLARATION.SIMPLE)
            elif function.typeVar == TYPE_NATIVE.TO_OWNED:
                if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if returnedValue.typeVar == TYPE_DECLARATION.STRING or returnedValue.typeVar == TYPE_DECLARATION.aSTRING:
                        return Retorno(TYPE_DECLARATION.STRING,returnedValue.value,TYPE_DECLARATION.SIMPLE)
                    else:
                        listError.append(Error("Error: La función to_owned() solo funciona con variables tipo String o &str","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función to_owned() solo funciona con variables tipo String o &str, no con arreglos ni vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.CLONE:
                return Retorno(returnedValue.typeVar,returnedValue.value,returnedValue.typeSingle)
            elif function.typeVar == TYPE_NATIVE.LEN:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    return Retorno(TYPE_DECLARATION.INTEGER,len(returnedValue.value[1]),TYPE_DECLARATION.SIMPLE)
                elif returnedValue.typeSingle == TYPE_DECLARATION.ARRAY:
                    return Retorno(TYPE_DECLARATION.INTEGER,len(returnedValue.value),TYPE_DECLARATION.SIMPLE)
                else: 
                    listError.append(Error("Error: La función len() solo funciona con vectores o arreglos","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.CAPACITY:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    return Retorno(TYPE_DECLARATION.INTEGER,returnedValue.value[0],TYPE_DECLARATION.SIMPLE)
                else: 
                    listError.append(Error("Error: La función capacity() solo funciona con vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.REMOVE:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    indexValue = function.value.executeInstruction(enviroment)
                    if indexValue != None:
                        saveValue = returnedValue.value[1][indexValue.value]
                        del returnedValue.value[1][indexValue.value]
                        return Retorno(TYPE_DECLARATION.INTEGER,saveValue.value,TYPE_DECLARATION.SIMPLE)
                    else:
                        listError.append(Error("Error: El indice de la función remove() es nulo","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else: 
                    listError.append(Error("Error: La función remove() solo funciona con vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.CONTAINS:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    Found = False
                    for single in returnedValue.value[1]:
                        if function.value == single.value:
                            Found = True
                    return Retorno(TYPE_DECLARATION.BOOLEAN,Found,TYPE_DECLARATION.SIMPLE)
                elif returnedValue.typeSingle == TYPE_DECLARATION.ARRAY:
                    Found = False
                    for single in returnedValue.value:
                        if function.value == single.value:
                            Found = True
                    return Retorno(TYPE_DECLARATION.BOOLEAN,Found,TYPE_DECLARATION.SIMPLE)
                else: 
                    listError.append(Error("Error: La función contains() solo funciona con vectores y arrays","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.PUSH:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    indexValue = function.value.executeInstruction(enviroment)
                    if indexValue != None:
                        if indexValue.typeVar == returnedValue.typeVar:
                            returnedValue.value[1].append(indexValue)
                            if len(returnedValue.value[1]) == returnedValue.value[0]:
                                    returnedValue.value[0] = returnedValue.value[0] * 2
                            return Retorno(returnedValue.typeVar,returnedValue.value,TYPE_DECLARATION.VECTOR)
                        else:
                            listError.append(Error("Error: El elemento que desea agregar a la lista no posee el mismo tipo de esta","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    else:
                        listError.append(Error("Error: El indice de la función push() es nulo","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else: 
                    listError.append(Error("Error: La función push() solo funciona con vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.INSERT:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    if len(function.value) == 2:
                        indexValue = function.value[0].executeInstruction(enviroment)
                        valueValue = function.value[1].executeInstruction(enviroment)
                        if indexValue != None and valueValue != None:
                            if indexValue.typeVar == TYPE_DECLARATION.INTEGER or indexValue.typeVar == TYPE_DECLARATION.USIZE:
                                returnedValue.value[1].insert(indexValue.value,valueValue)
                                if len(returnedValue.value[1]) == returnedValue.value[0]:
                                    returnedValue.value[0] = returnedValue.value[0] * 2
                                return Retorno(returnedValue.typeVar,returnedValue.value,TYPE_DECLARATION.VECTOR)
                            else:
                                listError.append(Error("Error: El indice de la función insert() no es un entero","Local",self.row,self.column,"SEMANTICO"))
                                return None
                        else:
                            listError.append(Error("Error: Uno o ambos indices de la función insert() son nulos","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    else:
                        listError.append(Error("Error: La función insert() tiene la cantidad de parametros incorrectos","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else: 
                    listError.append(Error("Error: La función insert() solo funciona con vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.CHARS:
                if returnedValue.typeVar == TYPE_DECLARATION.STRING or returnedValue.typeVar == TYPE_DECLARATION.aSTRING: 
                    if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                        charArray = [char for char in returnedValue.value] 
                        return Retorno(returnedValue.typeVar,charArray,TYPE_DECLARATION.ARRAY)
                    else:
                        listError.append(Error("Error: La función chars() solo se puede ejecutar con cadenas","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función chars() solo se puede ejecutar con cadenas","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.SQRT:
                if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if returnedValue.typeVar == TYPE_DECLARATION.INTEGER:
                        singleValue = math.sqrt(returnedValue.value)
                        return Retorno(returnedValue.typeVar,int(singleValue),TYPE_DECLARATION.SIMPLE)
                    elif returnedValue.typeVar == TYPE_DECLARATION.FLOAT: 
                        singleValue = math.sqrt(returnedValue.value)
                        return Retorno(returnedValue.typeVar,float(singleValue),TYPE_DECLARATION.SIMPLE)
                    else:
                        listError.append(Error("Error: La función sqtr() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función sqtr() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.ABS:
                if returnedValue.typeVar == TYPE_DECLARATION.INTEGER or returnedValue.typeVar == TYPE_DECLARATION.FLOAT: 
                    if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                        return Retorno(returnedValue.typeVar,abs(returnedValue.value),TYPE_DECLARATION.SIMPLE)
                    else:
                        listError.append(Error("Error: La función abs() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función abs() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.NEW:
                return Retorno(None,10,TYPE_DECLARATION.VECTOR)
            else:
                #WITH_CAPACITY
                return Retorno(None,function.value,TYPE_DECLARATION.VECTOR)
        else:
            listError.append(Error("Error: No se ha podido ejecutar la función nativa","Local",self.row,self.column,"SEMANTICO"))
            return None