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

    def compile(self, enviroment):
        returnedValue = self.value.compile(enviroment)
        function = self.function.compile(enviroment)
        if returnedValue != None and function != None:
            if function.typeVar == TYPE_NATIVE.TO_STRING:
                if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if returnedValue.typeVar == TYPE_DECLARATION.STRING or returnedValue.typeVar == TYPE_DECLARATION.aSTRING:
                        return Retorno(None,TYPE_DECLARATION.STRING,TYPE_DECLARATION.SIMPLE,returnedValue.label,returnedValue.code,returnedValue.temporal,returnedValue.att)
                    else:
                        listError.append(Error("Error: La función to_string() solo funciona con variables tipo String o &str","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función to_string() solo funciona con variables tipo String o &str, no con arreglos ni vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.TO_OWNED:
                if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                    if returnedValue.typeVar == TYPE_DECLARATION.STRING or returnedValue.typeVar == TYPE_DECLARATION.aSTRING:
                        return Retorno(None,TYPE_DECLARATION.STRING,None,TYPE_DECLARATION.SIMPLE,returnedValue.label,returnedValue.code,returnedValue.temporal)
                    else:
                        listError.append(Error("Error: La función to_owned() solo funciona con variables tipo String o &str","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función to_owned() solo funciona con variables tipo String o &str, no con arreglos ni vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.CLONE:
                return Retorno(None,returnedValue.typeVar,None,returnedValue.typeSingle,returnedValue.label,returnedValue.code,returnedValue.temporal)
            elif function.typeVar == TYPE_NATIVE.LEN:
                if returnedValue.typeSingle == TYPE_DECLARATION.ARRAY or returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    returned = enviroment.getVariable(self.value.id)
                    temporal = enviroment.generateTemporal()
                    temporal2 = enviroment.generateTemporal()
                    temporal3 = enviroment.generateTemporal()
                    CODE = '/* NATIVA LEN() */\n'
                    CODE += f'{temporal} = {returned.relativePosition};\n'
                    CODE += f'{temporal2} = Stack[(int) {temporal}];\n'
                    CODE += f'{temporal3} = Heap[(int) {temporal2}];\n'
                    return Retorno(None,TYPE_DECLARATION.INTEGER,None,TYPE_DECLARATION.SIMPLE,None,CODE,temporal3)
                else: 
                    listError.append(Error("Error: La función len() solo funciona con vectores o arreglos","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.CAPACITY:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    returned = enviroment.getVariable(self.value.id)
                    temporal = enviroment.generateTemporal()
                    temporal2 = enviroment.generateTemporal()
                    temporal3 = enviroment.generateTemporal()
                    temporal4 = enviroment.generateTemporal()
                    CODE = '/* NATIVA CAPACITY() */\n'
                    CODE += f'{temporal} = {returned.relativePosition};\n'
                    CODE += f'{temporal2} = Stack[(int) {temporal}];\n'
                    CODE += f'{temporal3} = {temporal2} + 1;\n'
                    CODE += f'{temporal4} = Heap[(int) {temporal3}];\n'
                    return Retorno(None,TYPE_DECLARATION.INTEGER,None,TYPE_DECLARATION.SIMPLE,None,CODE,temporal4)
                else: 
                    listError.append(Error("Error: La función capacity() solo funciona con vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.REMOVE:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    indexValue = function.value.compile(enviroment)
                    if indexValue != None:
                        returned = enviroment.getVariable(self.value.id)
                        cont = enviroment.generateTemporal()
                        newPointer = enviroment.generateTemporal()
                        temporal = enviroment.generateTemporal()
                        temporal2 = enviroment.generateTemporal()
                        temporal3 = enviroment.generateTemporal()
                        temporal4 = enviroment.generateTemporal()
                        temporal5 = enviroment.generateTemporal()
                        temporal6 = enviroment.generateTemporal()
                        temporal7 = enviroment.generateTemporal()
                        temporal8 = enviroment.generateTemporal()
                        temporal9 = enviroment.generateTemporal()
                        temporal10 = enviroment.generateTemporal()
                        label = enviroment.generateLabel()
                        label2 = enviroment.generateLabel()
                        label3 = enviroment.generateLabel()
                        label4 = enviroment.generateLabel()
                        label5 = enviroment.generateLabel()
                        label6 = enviroment.generateLabel()
                        CODE = '/* NATIVA REMOVE() */\n'
                        CODE += indexValue.code
                        CODE += f'  {temporal} = {returned.relativePosition};\n'
                        CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                        CODE += f'  {temporal3} = Heap[(int) {temporal2}];\n'#length
                        CODE += f'  if ({indexValue.temporal} < {temporal3}) goto {label};\n'
                        CODE += f'  goto {label2};\n'#Error, indice mayor al length
                        CODE += f'{label}:\n'#Entra porque el indice es menor al length
                        CODE += f'  {temporal4} = {temporal2} + 2;\n'
                        CODE += f'  {temporal5} = {temporal4} + {indexValue.temporal};\n'
                        CODE += f'  {temporal6} = Heap[(int) {temporal5}];\n'#Valor eliminado
                        #Empezamos a crear un nuevo Vector quitando la posición eliminada
                        CODE += f'  {cont} = 0;\n'
                        CODE += f'  {newPointer} = HP;\n'
                        CODE += f'  {temporal7} = Heap[(int) {temporal2}];\n'#length
                        CODE += f'  HP = {temporal7} - 1;\n'
                        CODE += f'  {temporal8} = {temporal2} + 1;\n'
                        CODE += f'  {temporal9} = Heap[(int) {temporal8}];\n'#capacity
                        CODE += f'  HP = HP + 1;\n'
                        CODE += f'  HP = Heap[(int) {temporal9}];\n'
                        CODE += f'  HP = HP + 1;\n'
                        CODE += f'{label3}:\n'#Etiqueta recursiva
                        CODE += f'  if ({cont} < {temporal3}) goto {label6};\n'
                        CODE += f'  goto {label2};\n'#Termina la copia del vector
                        CODE += f'{label6}:\n'#Sigue copiando
                        CODE += f'  if ({indexValue.temporal} == {cont}) goto {label4};\n'#El indice es igual
                        CODE += f'  goto {label5};\n'#El indice no es igual
                        CODE += f'{label4}:\n'#Encuentra el valor
                        CODE += f'  {cont} = {cont} + 1;\n'
                        CODE += f'  goto {label3};\n'
                        CODE += f'{label5}:\n'#Vuelve a buscar el indice
                        CODE += f'  {temporal10} = {temporal4} + {cont};\n'
                        CODE += f'  HP = Heap[(int) {temporal10}];\n'#Valor copiado
                        CODE += f'  HP = HP + 1;\n'
                        CODE += f'  {cont} = {cont} + 1;\n'
                        CODE += f'  goto {label3};\n'
                        CODE += f'{label2}:\n'#Se sale porque el indice es mayor al length
                        CODE += f'  Stack[(int) {temporal}] = {newPointer};\n'
                        return Retorno(None,returned.typeVar,None,TYPE_DECLARATION.SIMPLE,None,CODE,temporal6)
                    else:
                        listError.append(Error("Error: El indice de la función remove() es nulo","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else: 
                    listError.append(Error("Error: La función remove() solo funciona con vectores","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.CONTAINS:
                if returnedValue.typeSingle == TYPE_DECLARATION.ARRAY or returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    returned = enviroment.getVariable(self.value.id)
                    cont = enviroment.generateTemporal()
                    newPointer = enviroment.generateTemporal()
                    temporal = enviroment.generateTemporal()
                    temporal2 = enviroment.generateTemporal()
                    temporal3 = enviroment.generateTemporal()
                    temporal4 = enviroment.generateTemporal()
                    temporal5 = enviroment.generateTemporal()
                    temporal6 = enviroment.generateTemporal()
                    label = enviroment.generateLabel()
                    label2 = enviroment.generateLabel()
                    label3 = enviroment.generateLabel()
                    label4 = enviroment.generateLabel()
                    label5 = enviroment.generateLabel()
                    CODE = '/* NATIVA CONTAINS() */\n'
                    CODE += returnedValue.code
                    CODE += f'  {temporal} = {returned.relativePosition};\n'
                    CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                    CODE += f'  {temporal3} = Heap[(int) {temporal2}];\n'#length
                    if returnedValue.typeSingle == TYPE_DECLARATION.ARRAY:
                        CODE += f'  {temporal4} = {temporal2} + 1;\n'
                    else:
                        CODE += f'  {temporal4} = {temporal2} + 2;\n'
                    CODE += f'  {cont} = 0;\n'
                    CODE += f'{label}:\n'
                    CODE += f'  if ({cont} < {temporal3}) goto {label2};\n'#Sigue buscando
                    CODE += f'  goto {label3};\n'#No se ha encontrado
                    CODE += f'{label2}:\n'
                    CODE += f'  {temporal5} = {temporal4} + {cont};\n'
                    CODE += f'  {temporal6} = Heap[(int) {temporal5}];\n'
                    CODE += f'  if ({temporal6} == {returnedValue.temporal}) goto {label4};\n'#El valor es igual
                    CODE += f'  goto {label5};\n'#El valor no es igual
                    CODE += f'{label5}:\n'
                    CODE += f'  {cont} = {cont} + 1;\n'
                    CODE += f'  goto {label};\n'
                    retorno = Retorno(None,TYPE_DECLARATION.BOOLEAN,None,TYPE_DECLARATION.SIMPLE,None,CODE,None)
                    retorno.trueLabel = label4
                    retorno.falseLabel = label3
                    return retorno
                else: 
                    listError.append(Error("Error: La función contains() solo funciona con vectores y arrays","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.PUSH:
                if returnedValue.typeSingle == TYPE_DECLARATION.VECTOR:
                    indexValue = function.value.compile(enviroment)
                    if indexValue != None:
                        if indexValue.typeVar == returnedValue.typeVar:
                            returned = enviroment.getVariable(self.value.id)
                            cont = enviroment.generateTemporal()
                            newPointer = enviroment.generateTemporal()
                            temporal = enviroment.generateTemporal()
                            temporal2 = enviroment.generateTemporal()
                            temporal3 = enviroment.generateTemporal()
                            temporal4 = enviroment.generateTemporal()
                            temporal5 = enviroment.generateTemporal()
                            temporal6 = enviroment.generateTemporal()
                            temporal7 = enviroment.generateTemporal()
                            temporalData = enviroment.generateTemporal()
                            label = enviroment.generateLabel()
                            label2 = enviroment.generateLabel()
                            label3 = enviroment.generateLabel()
                            label4 = enviroment.generateLabel()
                            label5 = enviroment.generateLabel()
                            copyVector = enviroment.generateLabel()
                            CODE = '/* NATIVA PUSH() */\n'
                            CODE += returnedValue.code
                            CODE += f'  {temporal} = {returned.relativePosition};\n'
                            CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                            CODE += f'  {temporal3} = Heap[(int) {temporal2}];\n'#length
                            CODE += f'  {temporal4} = {temporal3} + 1;\n'
                            CODE += f'  {newPointer} = HP;\n'
                            CODE += f'  HP = {temporal4};\n'#Copia length + 1
                            CODE += f'  HP = HP + 1;\n'
                            CODE += f'  {temporal5} = {temporal2} + 1;\n'
                            CODE += f'  {temporal6} = Heap[(int) {temporal5}];\n'#capacity
                            CODE += f'  {temporalData} = {temporal5} + 1;\n'
                            
                            CODE += f'  if ({temporal6} == {temporal4}) goto {label};\n'#Aumentar capacidad
                            CODE += f'  goto {label2};\n'#Mantener capacidad
                            CODE += f'{label}:\n'
                            CODE += f'  HP = {temporal6} * 2;\n'
                            CODE += f'  HP = HP + 1;\n'
                            CODE += f'  goto {copyVector};\n'
                            CODE += f'{label2}:\n'
                            CODE += f'  HP = {temporal6};\n'
                            CODE += f'  HP = HP + 1;\n'
                            CODE += f'{copyVector}:\n'
                            CODE += f'  {cont} = 0;\n'
                            CODE += f'{label5}:\n'
                            CODE += f'  if ({cont} < {temporal6}) goto {label3};\n'#Sigue iterando
                            CODE += f'  goto {label4};\n'#Terminó de copiar
                            CODE += f'{label3}:\n'
                            CODE += f'  {temporal7} = {temporalData} + {cont};\n'
                            CODE += f'  HP = Heap[(int) {temporal7}];\n'
                            CODE += f'  HP = HP + 1;\n'
                            CODE += f'  {cont} = {cont} + 1;\n'
                            CODE += f'  goto {label5};\n'
                            CODE += f'{label4}:\n'
                            CODE += f'  Stack[(int) {temporal}] = {newPointer};\n'
                            return Retorno(None,returnedValue.typeVar,None,TYPE_DECLARATION.VECTOR,None,CODE,None)
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
                        indexValue = function.value[0].compile(enviroment)
                        valueValue = function.value[1].compile(enviroment)
                        if indexValue != None and valueValue != None:
                            if indexValue.typeVar == TYPE_DECLARATION.INTEGER or indexValue.typeVar == TYPE_DECLARATION.USIZE:
                                returned = enviroment.getVariable(self.value.id)
                                cont = enviroment.generateTemporal()
                                newPointer = enviroment.generateTemporal()
                                temporal = enviroment.generateTemporal()
                                temporal2 = enviroment.generateTemporal()
                                temporal3 = enviroment.generateTemporal()
                                temporal4 = enviroment.generateTemporal()
                                temporal5 = enviroment.generateTemporal()
                                temporal6 = enviroment.generateTemporal()
                                temporal7 = enviroment.generateTemporal()
                                temporal8 = enviroment.generateTemporal()
                                temporalData = enviroment.generateTemporal()
                                label = enviroment.generateLabel()
                                label2 = enviroment.generateLabel()
                                label3 = enviroment.generateLabel()
                                label4 = enviroment.generateLabel()
                                label5 = enviroment.generateLabel()
                                label6 = enviroment.generateLabel()
                                label7 = enviroment.generateLabel()
                                copyVector = enviroment.generateLabel()
                                CODE = '/* NATIVA INSERT() */\n'
                                CODE += returnedValue.code
                                CODE += f'  {temporal} = {returned.relativePosition};\n'
                                CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                                CODE += f'  {temporal3} = Heap[(int) {temporal2}];\n'#length
                                CODE += f'  {temporal4} = {temporal3} + 1;\n'
                                CODE += f'  {newPointer} = HP;\n'
                                CODE += f'  HP = {temporal4};\n'#Copia length + 1
                                CODE += f'  HP = HP + 1;\n'
                                CODE += f'  {temporal5} = {temporal2} + 1;\n'
                                CODE += f'  {temporal6} = Heap[(int) {temporal5}];\n'#capacity
                                CODE += f'  {temporalData} = {temporal5} + 1;\n'
                                
                                CODE += f'  if ({temporal6} == {temporal4}) goto {label};\n'#Aumentar capacidad
                                CODE += f'  goto {label2};\n'#Mantener capacidad
                                CODE += f'{label}:\n'
                                CODE += f'  HP = {temporal6} * 2;\n'
                                CODE += f'  HP = HP + 1;\n'
                                CODE += f'  goto {copyVector};\n'
                                CODE += f'{label2}:\n'
                                CODE += f'  HP = {temporal6};\n'
                                CODE += f'  HP = HP + 1;\n'
                                CODE += f'{copyVector}:\n'
                                CODE += f'  {cont} = 0;\n'
                                CODE += f'{label7}:\n'
                                CODE += f'  if ({cont} < {temporal6}) goto {label3};\n'#Sigue iterando
                                CODE += f'  goto {label4};\n'#Terminó de copiar
                                CODE += f'{label3}:\n'
                                CODE += f'  if ({indexValue.temporal} == {cont}) goto {label5};\n'#Es igual, entonces añade el valor
                                CODE += f'  goto {label6};\n'#Copia los demás valores
                                CODE += f'{label5}:\n'
                                CODE += f'  HP = {indexValue.temporal};\n'
                                CODE += f'  HP = HP + 1;\n'#Añade el nuevo valor y se va a añadir el antiguo
                                CODE += f'{label6}:\n'
                                CODE += f'  {temporal7} = {temporalData} + {cont};\n'
                                CODE += f'  {temporal8} = Heap[(int) {temporal7}];\n'
                                CODE += f'  {cont} = {cont} + 1;\n'
                                CODE += f'  HP = {temporal8};\n'
                                CODE += f'  HP = HP + 1;\n'
                                CODE += f'  goto {label7};\n'
                                CODE += f'{label4}:\n'
                                CODE += f'  Stack[(int) {temporal}] = {newPointer};\n'
                                return Retorno(None,returnedValue.typeVar,None,TYPE_DECLARATION.VECTOR,None,CODE,None)
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
                        temporal = enviroment.generateTemporal()
                        temporal2 = enviroment.generateTemporal()
                        temporal3 = enviroment.generateTemporal()
                        temporal4 = enviroment.generateTemporal()
                        temporal5 = enviroment.generateTemporal()
                        cont = enviroment.generateTemporal()
                        label = enviroment.generateLabel()
                        label2 = enviroment.generateLabel()
                        label3 = enviroment.generateLabel()
                        label4 = enviroment.generateLabel()
                        label5 = enviroment.generateLabel()
                        label6 = enviroment.generateLabel()
                        CODE = '/* NATIVA CHARS() */\n'
                        CODE += returnedValue.code
                        CODE += f'  {cont} = 0;\n'
                        CODE += f'{label}:\n'
                        CODE += f'  {temporal} = {returnedValue.temporal} + {cont};\n'
                        CODE += f'  {temporal2} = Heap[(int) {temporal}];\n'
                        CODE += f'  if({temporal2} == 0) goto {label2};\n'#Termina de contar caracterer
                        CODE += f'  goto {label3};\n'#Sigue sumando
                        CODE += f'{label3}:\n'
                        CODE += f'  {cont} = {cont} + 1;\n'
                        CODE += f'  goto {label};\n'
                        CODE += f'{label2}:\n'#Empieza a generar el Arrays
                        CODE += f'  {temporal3} = HP;\n'
                        CODE += f'  Heap[(int) {temporal3}] = {cont};\n'
                        CODE += f'  HP = HP + 1;\n'
                        CODE += f'  {cont} = 0;\n'
                        CODE += f'{label4}:\n'
                        CODE += f'  {temporal4} = {returnedValue.temporal} + {cont};\n'
                        CODE += f'  {temporal5} = Heap[(int) {temporal4}];\n'
                        CODE += f'  if({temporal5} == 0) goto {label5};\n'#Termina de agregar los valores
                        CODE += f'  goto {label6};\n'#Sigue agregando
                        CODE += f'{label6}:\n'
                        CODE += f'  Heap[HP] = {temporal5};\n'
                        CODE += f'  HP = HP + 1;\n'
                        CODE += f'  {cont} = {cont} + 1;\n'
                        CODE += f'  goto {label4};\n'
                        CODE += f'{label5}:\n'
                        return Retorno(None,TYPE_DECLARATION.CHAR,None,TYPE_DECLARATION.ARRAY,None,CODE,temporal3)
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
                        temporal = enviroment.generateTemporal()
                        CODE = '/* NATIVA SQRT() */\n'
                        CODE += f'{temporal} = {singleValue};\n'
                        return Retorno(None,TYPE_DECLARATION.INTEGER,None,TYPE_DECLARATION.SIMPLE,None,CODE,temporal)
                    elif returnedValue.typeVar == TYPE_DECLARATION.FLOAT: 
                        singleValue = math.sqrt(returnedValue.value)
                        temporal = enviroment.generateTemporal()
                        CODE = '/* NATIVA SQRT() */\n'
                        CODE += f'{temporal} = {singleValue};\n'
                        return Retorno(None,TYPE_DECLARATION.FLOAT,None,TYPE_DECLARATION.SIMPLE,None,CODE,temporal)
                    else:
                        listError.append(Error("Error: La función sqtr() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función sqtr() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.ABS:
                if returnedValue.typeVar == TYPE_DECLARATION.INTEGER or returnedValue.typeVar == TYPE_DECLARATION.FLOAT: 
                    if returnedValue.typeSingle == TYPE_DECLARATION.SIMPLE:
                        returned = enviroment.getVariable(self.value.id)
                        temporal = enviroment.generateTemporal()
                        temporal2 = enviroment.generateTemporal()
                        temporal3 = enviroment.generateTemporal()
                        CODE = '/* NATIVA ABS() */\n'
                        CODE += f'{temporal} = {returned.relativePosition};\n'
                        CODE += f'{temporal2} = Stack[(int) {temporal}];\n'
                        CODE += f'  if ({temporal2} < 0) goto {label};\n'
                        CODE += f'  goto {label2};\n'
                        CODE += f'{label}:\n'
                        CODE += f'  {temporal3} = {temporal2} * -1;\n'
                        CODE += f'{label2}:\n'
                        CODE += f'  {temporal3} = {temporal2};\n'
                        return Retorno(None,TYPE_DECLARATION.INTEGER,None,TYPE_DECLARATION.SIMPLE,None,CODE,temporal3)
                    else:
                        listError.append(Error("Error: La función abs() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:
                    listError.append(Error("Error: La función abs() solo se puede ejecutar con números","Local",self.row,self.column,"SEMANTICO"))
                    return None
            elif function.typeVar == TYPE_NATIVE.NEW:
                temporal = enviroment.generateTemporal()
                label = enviroment.generateLabel()
                CODE = '/* NATIVA NEW() */\n'
                CODE += f'  {temporal} = HP;\n'
                CODE += f'  Heap[(int) {temporal}] = 0;\n'
                CODE += f'  HP = HP + 1;\n'
                CODE += f'  Heap[HP] = 10;\n'
                CODE += f'  HP = HP + 1;\n'
                CODE += f'  {cont} = 0;\n'
                CODE += f'{label}:\n'
                CODE += f'  if({cont} != 10) goto {label2};\n'
                CODE += f'  goto {label3};\n'
                CODE += f'{label2}:\n'
                CODE += f'  HP = HP + 1;\n'
                CODE += f'  {cont} = {cont} + 1;\n'
                CODE += f'  goto {label};\n'
                CODE += f'{label3}:\n'
                return Retorno(None,None,None,TYPE_DECLARATION.VECTOR,None,CODE,temporal)
            else:
                #WITH_CAPACITY
                temporal = enviroment.generateTemporal()
                label = enviroment.generateLabel()
                CODE = '/* NATIVA NEW() */\n'
                CODE += f'  {temporal} = HP;\n'
                CODE += f'  Heap[(int) {temporal}] = 0;\n'
                CODE += f'  HP = HP + 1;\n'
                CODE += f'  Heap[HP] = 10;\n'
                CODE += f'  HP = HP + 1;\n'
                CODE += f'  {cont} = 0;\n'
                CODE += f'{label}:\n'
                CODE += f'  if({cont} != 10) goto {label2};\n'
                CODE += f'  goto {label3};\n'
                CODE += f'{label2}:\n'
                CODE += f'  HP = HP + 1;\n'
                CODE += f'  {cont} = {cont} + 1;\n'
                CODE += f'  goto {label};\n'
                CODE += f'{label3}:\n'
                return Retorno(None,None,None,TYPE_DECLARATION.VECTOR,None,CODE,temporal)
        else:
            listError.append(Error("Error: No se ha podido ejecutar la función nativa","Local",self.row,self.column,"SEMANTICO"))
            return None