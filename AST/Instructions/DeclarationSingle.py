from AST.Abstracts.Instruccion import Instruccion
from AST.Instructions.ListArraySimple import ListArraySimple
from AST.Symbol.Symbol import Symbol
from AST.Abstracts.Retorno import TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class DeclarationSingle(Instruccion):

    def __init__(self, asignation, expression, row, column):
        self.asignation = asignation
        self.expression = expression
        self.newEnv = None
        self.row = row
        self.column = column

    def compile(self, enviroment):
        content = self.asignation.compile(enviroment)
        exp = self.expression.compile(enviroment)
        if self.newEnv != None:
            enviroment = self.newEnv
        if content != None and exp != None:
            sizeEnv = enviroment.size
            if content.typeSingle == TYPE_DECLARATION.SIMPLE or content.typeSingle == TYPE_DECLARATION.VECTOR:
                if exp.typeVar == None and exp.typeSingle == TYPE_DECLARATION.VECTOR:
                    if enviroment.saveVariable(Symbol(content.typeVar, content.value[1], exp.value, content.typeSingle, content.value[0], sizeEnv)):
                        return self.createDeclaration(enviroment, exp, sizeEnv)
                elif content.typeSingle == exp.typeSingle:
                    if exp.typeVar == content.typeVar:
                        if enviroment.saveVariable(Symbol(content.typeVar, content.value[1], exp.value, content.typeSingle, content.value[0], sizeEnv)):
                            return self.createDeclaration(enviroment, exp, sizeEnv)
                    elif self.uSizeValidation(exp.typeVar,content.typeVar):
                        if enviroment.saveVariable(Symbol(TYPE_DECLARATION.USIZE,content.value[1],exp.value,content.typeSingle,content.value[0],sizeEnv)):
                            return self.createDeclaration(enviroment, exp, sizeEnv)
                        enviroment.saveVariable(Symbol(TYPE_DECLARATION.USIZE,content.value[1],exp.value,content.typeSingle,content.value[0],self.row,self.column))
                    else: listError.append(Error("Error: No se puede asignar un valor "+str(exp.typeVar)+" a una variable tipo "+str(content.typeVar),"Local",self.row,self.column,"SEMANTICO"))
                else: listError.append(Error("Error: Está tratando de asignar un valor de diferente tipo de dimensiones a las que intenta declarar","Local",self.row,self.column,"SEMANTICO"))
            else:
                #Comparar si las dimensiones a asignar son las mismas
                if exp.typeVar == content.typeVar:
                    if exp.typeSingle == TYPE_DECLARATION.ARRAY:
                        if isinstance(self.asignation.type, ListArraySimple):
                            if self.dimensionalCompare(exp.value, content.value[2]):
                                if enviroment.saveVariable(Symbol(content.typeVar, content.value[1], exp.value, content.typeSingle, content.value[0], sizeEnv)):
                                    return self.createDeclaration(enviroment, exp, sizeEnv)
                            else: listError.append(Error("Error: Está tratando de asignar una lista de diferentes dimensiones a las que intenta declarar","Local",self.row,self.column,"SEMANTICO"))
                        else:
                            if enviroment.saveVariable(Symbol(content.typeVar, content.value[1], exp.value, content.typeSingle, content.value[0], sizeEnv)):
                                return self.createDeclaration(enviroment, exp, sizeEnv)
                    elif exp.typeSingle == content.typeSingle:
                        if enviroment.saveVariable(Symbol(content.typeVar, content.value[1], exp.value, content.typeSingle, content.value[0], sizeEnv)):
                            return self.createDeclaration(enviroment, exp, sizeEnv)
                    else: listError.append(Error("Error: No se puede asignar un valor simple a una variable de varias dimensiones","Local",self.row,self.column,"SEMANTICO"))
                else: listError.append(Error("Error: No se puede asignar un valor "+str(exp.typeVar)+" a una variable tipo "+str(content.typeVar),"Local",self.row,self.column,"SEMANTICO"))
        else: listError.append(Error("Error: No se pudo asignar la variable porque su valor es nulo","Local",self.row,self.column,"SEMANTICO"))

    def createDeclaration(self, enviroment, exp, size):
        temporal = enviroment.generator.obtenerTemporal()
        CODE = '/* DECLARACIÓN */\n'
        CODE += exp.code + '\n'
        CODE += f'  {temporal} = SP + {size}; \n'
        CODE += f'  Stack[(int) {temporal}] = {exp.temporal};\n'
        return CODE

    def uSizeValidation(self, assignation, expression):
        if assignation == TYPE_DECLARATION.USIZE and expression == TYPE_DECLARATION.INTEGER:
            return True
        elif assignation == TYPE_DECLARATION.INTEGER and expression == TYPE_DECLARATION.USIZE:
            return True
        else:
            return False

    def dimensionalCompare(self, list1, list2, CODE):
        #Esperar a añadir arrays y vectores
        '''CODE += lReturn.code + '\n'
        CODE += rReturn.code + '\n'
        CODE += f'if({rReturn.temporal} != 0) goto {trueLabel};\n'
        CODE += f'{trueLabel}:\n'
        CODE += f'{temporal} = {lReturn.temporal} / {rReturn.temporal};\n'
        CODE += f'{falseLabel}:\n'''
        if len(list1) == len(list2):
            if isinstance(list1[0].value,list):
                if isinstance(list2[0],list):
                    return self.dimensionalCompare(list1[0].value,list2[0])
                else:
                    return False
            elif isinstance(list2[0],list):
                if isinstance(list1[0].value,list):
                    return self.dimensionalCompare(list1[0].value,list2[0])
                else:
                    return False
            else:
                return True
        else:
            return False

    '''
        [[1,4],[1,4],[1,4],[1,4],[1,4]]
        [[1,4],4,3,2,1]
    '''