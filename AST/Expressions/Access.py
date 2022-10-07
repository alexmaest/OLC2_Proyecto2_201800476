from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from AST.Symbol.Enviroment import Enviroment

class Access():
    def __init__(self, id, row, column):
        self.id = id
        self.row = row
        self.column = column

    def compile(self, enviroment):
        if self.id == '_': return None
        value = enviroment.getVariable(self.id)
        if value == None:
            listError.append(Error("Error: La variable "+str(self.id)+" no existe","Local",self.row,self.column,"SEMANTICO"))
            return None

        temporal = enviroment.generator.obtenerTemporal()
        temporal2 = enviroment.generator.obtenerTemporal()
        CODE = f'/* ACCEDIENDO A VARIABLE  {self.id} */\n'
        CODE += f'  {temporal} = SP + {value.relativePosition};\n'
        CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
        return Retorno(value.typeVar,value.value,value.typeSingle,"",CODE,temporal2)