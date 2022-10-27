from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.AccessInstruction import AccessInstruction
from AST.Expressions.Arithmetic import TYPE_OPERATION
from AST.Instructions.Modulo import Modulo
from AST.Instructions.Struct import Struct
from AST.Error.Error import Error
from AST.Symbol.SymbolList import searchInListStructsAux
from AST.Error.ErrorList import listError

class AssignmentAccessArray(Instruccion):

    def __init__(self,accessArray,expression,attributes,row,column):
        self.accessArray = accessArray
        self.expression = expression
        self.attributes = attributes
        self.isDeclaration = False
        self.row = row
        self.column = column
    
    def compile(self, enviroment):
        access = self.accessArray.compile(enviroment)
        exp = self.expression.compile(enviroment)
        if access != None and exp != None:
            exist = enviroment.getVariable(self.accessArray.id.id)
            if exist != None:
                if self.attributes == None:
                    if self.isDeclaration or exist.mutable:
                        if self.compareTypes(access,exp):
                            CODE = '/* ASIGNACION POR ACCESO */\n'
                            CODE += access.code
                            CODE += exp.code
                            CODE += f'{access.label} = {exp.temporal};\n'
                            return Retorno(None,None,None,None,CODE,None,None)
                        else:pass #Ya se dijeron los errores así que no se hace nada
                    else:listError.append(Error("Error: La Variable a la que desea acceder no es mutable","Local",self.row,self.column,"SEMANTICO"))
                else:
                    founded = self.returnAttribute(exist,access.typeVar,self.attributes,0,access.temporal,enviroment)
                    if founded != None:
                        if founded.typeVar == exp.typeVar:
                            if founded.typeSingle == exp.typeSingle:
                                temporal1 = enviroment.generator.generateTemporal()
                                CODE = '/* ASIGNACION POR ACCESO */\n'
                                CODE += founded.code
                                CODE += f'{temporal1} = Heap[(int) {founded.temporal}];\n'
                                CODE += f'Heap[(int) {temporal1}] = {exp.temporal};\n'
                                return Retorno(None,None,None,None,CODE,None,None)
                            else:listError.append(Error("Error: No se puede asignar un valor de diferentes dimensiones a las de la variable","Local",self.row,self.column,"SEMANTICO"))
                        else:listError.append(Error("Error: No se puede asignar un valor",exp.typeVar,"a un atributo tipo",founded.typeVar,"Local",self.row,self.column,"SEMANTICO"))
                    else:pass #Ya se dijeron los errores así que no se hace nada
        else:listError.append(Error("Error: La Posición de la variable que desea acceder no pudo ser modificada","Local",self.row,self.column,"SEMANTICO"))
    
    def returnAttribute(self, variable, accesstypeVar, attList, number, temporal, enviroment):
        cont = 0
        foundedStruct = searchInListStructsAux(accesstypeVar)
        if foundedStruct != None:
            for att in foundedStruct.attributes:
                if att.id == attList[number]:
                    if att.isPublic:
                        singleAtt = []
                        singleAtt.append(attList[number])
                        type = AccessInstruction(singleAtt,-1,-1)
                        type.isAux = True
                        returned = type.compile(enviroment)
                        if returned != None:
                            temporal1 = enviroment.generator.generateTemporal()
                            if returned.typeSingle == TYPE_DECLARATION.STRUCT:
                                temporal2 = enviroment.generator.generateTemporal()
                                CODE = '/* ACCEDIENDO A ATRIBUTO */\n'
                                CODE += f'  {temporal1} = {temporal} + {cont};\n'#Posición del atributo
                                CODE += f'  {temporal2} = Heap[(int) {temporal1}];\n'#Posicion del Objeto atributo
                                returned = self.returnAttribute(variable,returned.typeVar,attList,(number+1),temporal2,enviroment)
                                if returned != None:
                                    CODE += returned.code
                                    return Retorno(None,returned.typeVar,returned.typeSingle,None,CODE,returned.temporal,None)
                                else: return None
                            else:
                                CODE = '/* ACCEDIENDO A ATRIBUTO */\n'
                                CODE += f'  {temporal1} = {temporal} + {cont};\n'#Posición del atributo
                                return Retorno(None,returned.typeVar,returned.typeSingle,None,CODE,temporal1,None)
                        else: return None
                    else: 
                        listError.append(Error("Error: El atributo con id \'"+str(attList[number])+"\' no es público para asignarle valores","Local",self.row,self.column,"SEMANTICO"))
                        return None
                else:cont += 1
            listError.append(Error("Error: No se ha encontrado el atributo \'"+str(attList[number])+"\'","Local",self.row,self.column,"SEMANTICO"))
            return None
        else:
            listError.append(Error("Error: El struct al que desea acceder con id "+str(accesstypeVar)+" no existe","Local",self.row,self.column,"SEMANTICO"))
            return None
        
        'carro1[0].marca'
        '''
        position = [0]
        value = [1,2,3,4,5]

        position = [1,2,0]
        value = [[[1,2],[3,4],[5,6]],[[7,8],[9,10],[11,12]]]
        '''

    def compareTypes(self, access, exp):
        if access.typeVar == exp.typeVar:
            if access.typeSingle == exp.typeSingle:
                return True
            else: 
                listError.append(Error("Error: No se puede asignar un valor de diferentes dimensiones a las de la variable","Local",self.row,self.column,"SEMANTICO"))
                return False
        else: 
            listError.append(Error("Error: No se puede asignar un valor ",exp.typeVar," a una variable tipo",access.typeVar,"Local",self.row,self.column,"SEMANTICO"))
            return False