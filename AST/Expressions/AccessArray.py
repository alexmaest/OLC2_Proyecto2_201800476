from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class AccessArray():
    def __init__(self, id, listAccess, row, column):
        self.id = id
        self.listAccess = listAccess
        self.row = row
        self.column = column
        self.dimensions = 0

    def compile(self,enviroment):
        singleId = self.id.compile(enviroment)
        if singleId != None:
            if singleId.typeSingle == TYPE_DECLARATION.ARRAY or singleId.typeSingle == TYPE_DECLARATION.VECTOR:
                label = enviroment.generator.generateLabel()
                temporal = enviroment.generator.generateTemporal()
                temporal2 = enviroment.generator.generateTemporal()
                CODE = '/* ACCESO A ARRAY */\n'
                CODE += f'{temporal} = SP + {singleId.relativePosition};\n'
                CODE += f'{temporal2} = Stack[(int) {temporal}];\n'
                if len(singleId.value) >= len(self.listAccess):
                    returned = self.returnValue(singleId,self.compileValues(enviroment),temporal2,enviroment)
                    CODE += returned.code
                    CODE = CODE.replace('ArrayLabel',label)
                    CODE += f'{label}:\n'
                    return Retorno(TYPE_DECLARATION.VALOR,returned.typeVar,None,TYPE_DECLARATION.SIMPLE,returned.label,CODE,returned.temporal)
                else:
                    listError.append(Error("Error: La lista no posee esa cantidad de dimensiones","Local",self.row,self.column,"SEMANTICO"))
                    return None
            else:
                listError.append(Error("Error: La variable no es una lista","Local",self.row,self.column,"SEMANTICO"))
                return None
        else:
            return None

    def returnValue(self, exp, expList, temporal, enviroment):
        obtained = expList.pop(0)
        temporal1 = enviroment.generator.generateTemporal()
        temporal2 = enviroment.generator.generateTemporal()
        temporal3 = enviroment.generator.generateTemporal()
        temporal4 = enviroment.generator.generateTemporal()
        CODE = '/* ACCEDIENDO A POSICION */\n'
        CODE += f'{temporal1} = Heap[(int) {temporal}]; /* TAMAÑO DE ARRAY */\n'
        CODE += f' if ({obtained.temporal} > {temporal1}) goto ArrayLabel;\n'
        CODE += f'{temporal2} = {temporal} + 1;\n'
        CODE += f'{temporal3} = {temporal2} + {obtained.temporal};\n'
        CODE += f'{temporal4} = Heap[(int) {temporal3}];\n'
        if(len(expList)> 0):
            result = self.returnValue(expList,temporal4,enviroment)
            CODE += result.code
            return Retorno(TYPE_DECLARATION.VALOR,exp.typeVar,None,TYPE_DECLARATION.SIMPLE,result.label,CODE,result.temporal)
        else:
            return Retorno(TYPE_DECLARATION.VALOR,exp.typeVar,None,TYPE_DECLARATION.SIMPLE,'Heap[(int) {temporal3}]',CODE,temporal4)

        '''
        position = [0]
        value = [1]

        position = [1,2,0]
        value = [[[1,2],[3,4],[5,6]],[[7,8],[9,10],[11,12]]]
        '''

    def getId(self):
        return self.id

    def compileValues(self, enviroment):
        values = []
        for exp in self.listAccess:
            single = exp.compile(enviroment)
            values.append(single)
            if single.typeVar != TYPE_DECLARATION.INTEGER and single.typeVar != TYPE_DECLARATION.USIZE:
                return []
            else: pass
        return values