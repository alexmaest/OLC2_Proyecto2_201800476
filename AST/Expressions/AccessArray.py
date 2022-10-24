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
        singleId = enviroment.getVariable(self.id.id)
        if singleId != None:
            if singleId.typeSingle == TYPE_DECLARATION.ARRAY or singleId.typeSingle == TYPE_DECLARATION.VECTOR:
                temporal = enviroment.generator.generateTemporal()
                temporal2 = enviroment.generator.generateTemporal()
                label = enviroment.generator.generateLabel()
                label2 = enviroment.generator.generateLabel()
                single = self.compileValues(enviroment)
                if single != None:
                    returned = self.returnValue(singleId,single,temporal2,enviroment,0)
                    CODE = '/* ACCESO A ARRAY */\n'
                    CODE += f'  {temporal} = SP + {singleId.relativePosition};\n'
                    CODE += f'  {temporal2} = Stack[(int) {temporal}];\n'
                    CODE += returned.code
                    CODE += f'  goto {label};\n'
                    CODE = CODE.replace('IndexOutLabel',label2)
                    CODE += f'{label2}:\n'
                    CODE += self.printIndexOut()
                    CODE += f'{label}:\n'
                    return Retorno(None,returned.typeVar,returned.typeSingle,None,CODE,returned.temporal)
                else:listError.append(Error("Error: No se ha podido acceder al array o vector","Local",self.row,self.column,"SEMANTICO"))
            else:listError.append(Error("Error: La variable no es una lista","Local",self.row,self.column,"SEMANTICO"))
        else:return None

    def returnValue(self, exp, expList, temporal, enviroment, dimension):
        dimension += 1
        obtained = expList.pop(0)
        temporal1 = enviroment.generator.generateTemporal()
        temporal2 = enviroment.generator.generateTemporal()
        temporal3 = enviroment.generator.generateTemporal()
        temporal4 = enviroment.generator.generateTemporal()
        CODE = '/* ACCEDIENDO A POSICION */\n'
        CODE += f'{temporal1} = Heap[(int) {temporal}]; /* TAMAÑO DE ARRAY */\n'
        CODE += f' if ({obtained.temporal} >= {temporal1}) goto IndexOutLabel;\n'
        CODE += f'{temporal2} = {temporal} + 1;\n'
        CODE += f'{temporal3} = {temporal2} + {obtained.temporal};\n'
        CODE += f'{temporal4} = Heap[(int) {temporal3}];\n'
        if(len(expList)> 0):
            result = self.returnValue(expList,temporal4,enviroment,dimension)
            CODE += result.code
            return Retorno(None,exp.typeVar,TYPE_DECLARATION.ARRAY,result.label,CODE,result.temporal)
        else:
            if dimension == 1:return Retorno(None,exp.typeVar,TYPE_DECLARATION.SIMPLE,'Heap[(int) {temporal3}]',CODE,temporal4)
            else:return Retorno(None,exp.typeVar,TYPE_DECLARATION.ARRAY,'Heap[(int) {temporal3}]',CODE,temporal4)

        '''
        position = [0]
        value = [1]

        position = [1,2,0]
        value = [[[1,2],[3,4],[5,6]],[[7,8],[9,10],[11,12]]]
        '''

    def compileValues(self, enviroment):
        values = []
        for exp in self.listAccess:
            single = exp.compile(enviroment)
            if single != None:
                if single.typeVar != TYPE_DECLARATION.INTEGER and single.typeVar != TYPE_DECLARATION.USIZE:
                    listError.append(Error("Error: El indice con el que desea acceder al arreglo o vector no es tipo entero o usize","Local",self.row,self.column,"SEMANTICO"))
                    return None
                else:values.append(single)
            else:
                listError.append(Error("Error: El indice con el que desea acceder al arreglo o vector es nulo","Local",self.row,self.column,"SEMANTICO"))
                return None
        return values
    
    def printIndexOut(self):
        CODE = '/* ERROR: INDICE FUERA DE LIMITES */\n'
        CODE += 'printf("%c",(char) 66);  //B\n'
        CODE += 'printf("%c",(char) 111); //o\n' 
        CODE += 'printf("%c",(char) 117); //u\n' 
        CODE += 'printf("%c",(char) 110); //n\n' 
        CODE += 'printf("%c",(char) 100); //d\n'
        CODE += 'printf("%c",(char) 115); //s\n' 
        CODE += 'printf("%c",(char) 69);  //E\n' 
        CODE += 'printf("%c",(char) 114); //r\n' 
        CODE += 'printf("%c",(char) 114); //r\n'
        CODE += 'printf("%c",(char) 111); //o\n'
        CODE += 'printf("%c",(char) 114); //r\n'
        CODE += 'printf("%c",(char) 10);\n'
        return CODE

    def getId(self):
        return self.id