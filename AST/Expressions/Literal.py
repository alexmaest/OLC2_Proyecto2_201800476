from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Abstracts.Expression import Expression

class Literal():
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def compile(self,enviroment):
        CODE = ""
        if self.type == 0:
            temporal = enviroment.generator.obtenerTemporal()
            CODE += f'  {temporal} = {self.value};'
            return Retorno(TYPE_DECLARATION.INTEGER,self.value,TYPE_DECLARATION.SIMPLE,"",CODE,temporal)
        elif self.type == 1:
            temporal = enviroment.generator.obtenerTemporal()
            CODE += f'  {temporal} = {self.value};'
            return Retorno(TYPE_DECLARATION.FLOAT,self.value,TYPE_DECLARATION.SIMPLE,"",CODE,temporal)
        elif self.type == 2:
            temporal = enviroment.generator.obtenerTemporal()
            CODE += f'  {temporal} = HP;\n'
            for char in self.value:
                singleChar = ord(char)
                CODE += f'  Heap[HP] = {singleChar};\n'
                CODE += f'  HP = HP + 1;\n'
            CODE += f'  Heap[HP] = 0;\n'
            CODE += f'  HP = HP + 1;\n'
            return Retorno(TYPE_DECLARATION.STRING,self.value,TYPE_DECLARATION.SIMPLE,"",CODE,temporal)
        elif self.type == 3:
            temporal = enviroment.generator.obtenerTemporal()
            CODE += f'  {temporal} = HP;\n'
            for char in self.value:
                singleChar = ord(char)
                CODE += f'  Heap[HP] = {singleChar};\n'
                CODE += f'  HP = HP + 1;\n'
            CODE += f'  Heap[HP] = 0;\n'
            CODE += f'  HP = HP + 1;\n'
            return Retorno(TYPE_DECLARATION.aSTRING,self.value,TYPE_DECLARATION.SIMPLE,"",CODE,temporal)
        elif self.type == 4:
            temporal = enviroment.generator.obtenerTemporal()
            if self.value == "True":
                CODE += f'  {temporal} = 1;\n'
            else:
                CODE += f'  {temporal} = 0;\n'
            return Retorno(TYPE_DECLARATION.BOOLEAN,self.value,TYPE_DECLARATION.SIMPLE,"",CODE,temporal)
        elif self.type == 5:
            temporal = enviroment.generator.obtenerTemporal()
            CODE += f'  {temporal} = {ord(self.value)};'
            return Retorno(TYPE_DECLARATION.CHAR,self.value,TYPE_DECLARATION.SIMPLE,"",CODE,temporal)
        elif self.type == 6:
            temporal = enviroment.generator.obtenerTemporal()
            CODE += f'  {temporal} = {self.value};'
            return Retorno(TYPE_DECLARATION.USIZE,self.value,TYPE_DECLARATION.SIMPLE,"",CODE,temporal)