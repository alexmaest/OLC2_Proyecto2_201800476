from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class NewArray():

    def __init__(self, listExp, row, column):
        self.listExp = listExp
        self.dimensions = []
        self.row = row
        self.column = column
        self.isVector = False

    def compile(self,enviroment):
        pointer = enviroment.generator.generateTemporal()
        typeDimension = None
        typeArray = None
        CODE = ''
        #Generamos código si es vector
        if self.isVector:
            CODE += '/* CREANDO VECTOR */\n'
            CODE += f'  {pointer} = HP;\n'
            CODE += f'  Heap[(int){pointer}] = {len(self.listExp)};\n'
            CODE += f'  HP = HP + 1;\n'
            CODE += f'  Heap[HP] = {len(self.listExp) + 2};\n'
            CODE += f'  HP = HP + {len(self.listExp) + 3};\n'
        else:
        #Generamos código si es array
            CODE += '/* CREANDO ARRAY */\n'
            CODE += f'  {pointer} = HP;\n'
            CODE += f'  Heap[(int){pointer}] = {len(self.listExp)};\n'
            CODE += f'  HP = HP + {len(self.listExp) + 1};\n'
        self.dimensions.append(len(self.listExp))
        
        #Compilamos expresiones
        for i in range(len(self.listExp)):
            exp = self.listExp[i].compile(enviroment)
            if exp != None:
                if typeArray == None and typeDimension == None:
                    temporal = enviroment.generator.generateTemporal()
                    typeArray = exp.typeVar
                    typeDimension = exp.typeSingle
                    CODE += exp.code
                    if self.isVector: CODE += f'  {temporal} = {pointer} + {i+2};\n'
                    else: CODE += f'  {temporal} = {pointer} + {i+1};\n'
                    CODE += f'  Heap[(int) {temporal}] = {exp.temporal};\n'
                    if typeDimension == TYPE_DECLARATION.ARRAY:
                        self.dimensions.extend(self.listExp[i].dimensions)
                        lenDimension = self.listExp[i].dimensions
                else:
                    if exp.typeVar == typeArray:
                        if exp.typeSingle == typeDimension:
                            if typeDimension == TYPE_DECLARATION.ARRAY:
                                if lenDimension == self.listExp[i].dimensions:
                                    temporal = enviroment.generator.generateTemporal()
                                    CODE += exp.code
                                    if self.isVector: CODE += f'  {temporal} = {pointer} + {i+2};\n'
                                    else: CODE += f'  {temporal} = {pointer} + {i+1};\n'
                                    CODE += f'  Heap[(int) {temporal}] = {exp.temporal};\n'
                                else:
                                    listError.append(Error("Error: No se ha podido crear la lista debido a que todas las expresiones no son de la misma longitud","Local",self.row,self.column,"SEMANTICO"))    
                                    return None
                            else:
                                temporal = enviroment.generator.generateTemporal()
                                CODE += exp.code
                                if self.isVector: CODE += f'  {temporal} = {pointer} + {i+2};\n'
                                else: CODE += f'  {temporal} = {pointer} + {i+1};\n'
                                CODE += f'  Heap[(int){temporal}] = {exp.temporal};\n'
                        else:
                            listError.append(Error("Error: No se ha podido crear la lista debido a que todas las expresiones no son de la misma dimensión","Local",self.row,self.column,"SEMANTICO"))    
                            return None
                    else:
                        listError.append(Error("Error: No se ha podido crear la lista debido a que todas las expresiones no son del mismo tipo","Local",self.row,self.column,"SEMANTICO"))    
                        return None
            else:return None
        return Retorno(None,typeArray,TYPE_DECLARATION.ARRAY,None,CODE,pointer,None)