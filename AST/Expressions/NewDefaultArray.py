from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class NewDefaultArray():

    dimensions = []

    def __init__(self, value, size, row, column):
        self.value = value
        self.size = size
        self.row = row
        self.column = column
        self.dimensions = []
        self.isVector = False

    def compile(self,enviroment):
        self.dimensions = []
        singleValue = self.value.compile(enviroment)
        singleSize = self.size.compile(enviroment)
        if singleValue != None and singleSize != None:
            if singleSize.typeVar == TYPE_DECLARATION.INTEGER:
                pointer = enviroment.generator.generateTemporal()
                CODE = ''
                if self.isVector:
                    CODE += '/* CREANDO VECTOR */\n'
                    CODE += f'  {pointer} = HP;\n'
                    CODE += f'  Heap[(int){pointer}] = {singleSize.value};\n'
                    CODE += f'  HP = HP + 1;\n'
                    CODE += f'  Heap[HP] = {singleSize.value + 2};\n'
                    CODE += f'  HP = HP + 1;\n'
                else:
                    CODE += '/* CREANDO ARRAY */\n'
                    CODE += f'  {pointer} = HP;\n'
                    CODE += f'  Heap[(int){pointer}] = {len(self.listExp)};\n'
                    CODE += f'  HP = HP + 1;\n'
                references = []
                for i in range(singleSize.value):
                    temporal = enviroment.generator.generateTemporal()
                    CODE += f'  {temporal} = HP;\n'
                    CODE += f'  HP = HP + 1;\n'
                    references.append(temporal)
                self.dimensions.append(len(self.listExp))
                for number in range(singleSize.value):
                    singleValue = self.value.compile(enviroment)
                    if singleValue.typeSingle == TYPE_DECLARATION.ARRAY:
                        self.dimensions.extend(singleValue.value)
                    CODE += singleValue.code
                    CODE += f'  Heap[(int){references[number]}] = {singleValue.temporal};\n'
                return Retorno(TYPE_DECLARATION.VALOR,singleValue.typeVar,self.dimensions,TYPE_DECLARATION.ARRAY,"",CODE,pointer)
            else:
                listError.append(Error("Error: No se ha podido crear la lista debido a que el tamaño para la lista no es un entero","Local",self.row,self.column,"SEMANTICO"))    
                return None
        else:
            listError.append(Error("Error: No se ha podido crear la lista","Local",self.row,self.column,"SEMANTICO"))  
            return None