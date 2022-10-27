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
            if self.value != None:
                temporal = enviroment.generator.generateTemporal()
                CODE += f'  {temporal} = {self.value};\n'
                return Retorno(None,TYPE_DECLARATION.INTEGER,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
            else:
                return Retorno(None,TYPE_DECLARATION.INTEGER,TYPE_DECLARATION.SIMPLE,None,None,None,None)
        elif self.type == 1:
            if self.value != None:
                temporal = enviroment.generator.generateTemporal()
                CODE += f'  {temporal} = {self.value};\n'
                return Retorno(None,TYPE_DECLARATION.FLOAT,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
            else:
                return Retorno(None,TYPE_DECLARATION.FLOAT,TYPE_DECLARATION.SIMPLE,None,None,None,None)
        elif self.type == 2:
            if self.value != None:
                temporal = enviroment.generator.generateTemporal()
                CODE += f'  {temporal} = HP;\n'
                for char in self.value:
                    singleChar = ord(char)
                    CODE += f'  Heap[HP] = {singleChar}; /*{char}*/\n'
                    CODE += f'  HP = HP + 1;\n'
                CODE += f'  Heap[HP] = 0;\n'
                CODE += f'  HP = HP + 1;\n'
                return Retorno(None,TYPE_DECLARATION.STRING,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
            else:
                return Retorno(None,TYPE_DECLARATION.STRING,TYPE_DECLARATION.SIMPLE,None,None,None,None)
        elif self.type == 3:
            if self.value != None:
                temporal = enviroment.generator.generateTemporal()
                CODE += f'  {temporal} = HP;\n'
                for char in self.value:
                    singleChar = ord(char)
                    CODE += f'  Heap[HP] = {singleChar}; /*{char}*/\n'
                    CODE += f'  HP = HP + 1;\n'
                CODE += f'  Heap[HP] = 0;\n'
                CODE += f'  HP = HP + 1;\n'
                return Retorno(None,TYPE_DECLARATION.aSTRING,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
            else:
                return Retorno(None,TYPE_DECLARATION.aSTRING,TYPE_DECLARATION.SIMPLE,None,None,None,None)
        elif self.type == 4:
            if self.value != None:
                temporal = enviroment.generator.generateTemporal()
                if self.trueLabel != '' and self.value == True:
                    CODE += f'  goto {self.trueLabel};\n'
                elif self.falseLabel != '' and self.value == False:
                    CODE += f'  goto {self.falseLabel};\n'
                else:
                    if self.value == True:
                        CODE += f'  {temporal} = 1;\n'
                    else:
                        CODE += f'  {temporal} = 0;\n'
                value = Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
                value.trueLabel = self.trueLabel
                value.falseLabel = self.falseLabel
                return value
            else:
                return Retorno(None,TYPE_DECLARATION.BOOLEAN,TYPE_DECLARATION.SIMPLE,None,None,None,None)
        elif self.type == 5:
            if self.value != None:
                temporal = enviroment.generator.generateTemporal()
                CODE += f'  {temporal} = {ord(self.value)};\n'
                return Retorno(None,TYPE_DECLARATION.CHAR,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
            else:
                return Retorno(None,TYPE_DECLARATION.CHAR,TYPE_DECLARATION.SIMPLE,None,None,None,None)
        elif self.type == 6:
            if self.value != None:
                temporal = enviroment.generator.generateTemporal()
                CODE += f'  {temporal} = {self.value};\n'
                return Retorno(None,TYPE_DECLARATION.USIZE,TYPE_DECLARATION.SIMPLE,None,CODE,temporal,None)
            else:
                return Retorno(None,TYPE_DECLARATION.USIZE,TYPE_DECLARATION.SIMPLE,None,None,None,None)