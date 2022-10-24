from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class Access():
    def __init__(self, id, row, column):
        self.id = id
        self.row = row
        self.column = column

    def compile(self, enviroment):
        if self.id == '_': return None
        value = enviroment.getVariable(self.id)
        if value != None:
            temporal = enviroment.generator.generateTemporal()
            temporal2 = enviroment.generator.generateTemporal()
            CODE = f'/* ACCEDIENDO A VARIABLE {self.id} */\n'
            CODE += f'  {temporal} = SP + {value.relativePosition};\n'
            CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
            if value.isReference:
                temporal3 = enviroment.generator.generateTemporal()
                CODE += f'  {temporal3} = Stack[(int) {temporal2}];\n'
                return Retorno(None,value.typeVar,value.typeSingle,None,CODE,temporal3,value.att)
            else:return Retorno(None,value.typeVar,value.typeSingle,None,CODE,temporal2,value.att)
        else:listError.append(Error("Error: La variable "+str(self.id)+" no existe","Local",self.row,self.column,"SEMANTICO"))