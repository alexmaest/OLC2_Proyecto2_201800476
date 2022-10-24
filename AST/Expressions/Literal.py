from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Abstracts.Expression import Expression

class Literal():
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.trueLabel = ''
        self.falseLabel = ''

    def compile(self,enviroment):
        CODE = ''
        if self.type == 0:
            temporal = enviroment.generator.generateTemporal()
            CODE += f'  {temporal} = {self.value};\n'
            return Retorno(None,TYPE_DECLARATION.INTEGER,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
        elif self.type == 1:
            temporal = enviroment.generator.generateTemporal()
            CODE += f'  {temporal} = {self.value};\n'
            return Retorno(None,TYPE_DECLARATION.FLOAT,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
        elif self.type == 2:
            if self.value == None:
                return Retorno(None,TYPE_DECLARATION.STRING,TYPE_DECLARATION.SIMPLE,None,None,None,None)
            temporal = enviroment.generator.generateTemporal()
            CODE += f'  {temporal} = HP;\n'
            for char in self.value:
                singleChar = ord(char)
                CODE += f'  Heap[HP] = {singleChar}; /*{char}*/\n'
                CODE += f'  HP = HP + 1;\n'
            CODE += f'  Heap[HP] = 0;\n'
            CODE += f'  HP = HP + 1;\n'
            return Retorno(None,TYPE_DECLARATION.STRING,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
        elif self.type == 3:
            if self.value == None:
                return Retorno(None,TYPE_DECLARATION.aSTRING,TYPE_DECLARATION.SIMPLE,None,None,None,None)
            temporal = enviroment.generator.generateTemporal()
            CODE += f'  {temporal} = HP;\n'
            for char in self.value:
                singleChar = ord(char)
                CODE += f'  Heap[HP] = {singleChar}; /*{char}*/\n'
                CODE += f'  HP = HP + 1;\n'
            CODE += f'  Heap[HP] = 0;\n'
            CODE += f'  HP = HP + 1;\n'
            return Retorno(None,TYPE_DECLARATION.aSTRING,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
        elif self.type == 4:
            trueLabel = enviroment.generator.generateLabel()
            falseLabel = enviroment.generator.generateLabel()
            if self.value == "True":
                CODE += f'  goto {trueLabel};\n'
            else:
                CODE += f'  goto {falseLabel};\n'
            self.trueLabel = trueLabel
            self.falseLabel = falseLabel
            return Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,None,None)
        elif self.type == 5:
            temporal = enviroment.generator.generateTemporal()
            CODE += f'  {temporal} = {ord(self.value)};\n'
            return Retorno(None,TYPE_DECLARATION.CHAR,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
        elif self.type == 6:
            temporal = enviroment.generator.generateTemporal()
            CODE += f'  {temporal} = {self.value};\n'
            return Retorno(None,TYPE_DECLARATION.USIZE,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)