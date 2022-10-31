from typing import TYPE_CHECKING
from AST.Abstracts.Expression import Expression
from AST.Expressions.Access import Access
from AST.Expressions.AccessInstruction import AccessInstruction
from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Expressions.AccessArray import AccessArray
from AST.Expressions.AttAssign import AttAssign
from AST.Expressions.CallNative import CallNative
from AST.Expressions.Handler import Handler
from AST.Instructions.Native import Native
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from AST.Symbol.SymbolList import searchInListStructsAux
from enum import Enum

class AttAccess():
    def __init__(self, expList, row, column):
        self.expList = expList
        self.dimensions = []
        self.row = row
        self.column = column
        self.trueLabel = ''
        self.falseLabel = ''
    
    def compile(self, enviroment):
        exist = None
        if isinstance(self.expList[0],AttAssign):
            if isinstance(self.expList[0].id.id,AccessArray):
                exist = self.expList[0].id.id.compile(enviroment)
                self.dimensions = self.expList[0].id.id.dimensions
            else:
                exist = enviroment.getVariable(self.expList[0].id.id)
        else: 
            exist = self.expList[0].compile(enviroment)
        if exist != None:
            if isinstance(self.expList[0].id.id,AccessArray):
                singleId = exist
            else:
                if self.trueLabel != '' and self.falseLabel != '':
                    self.expList[0].id.trueLabel = self.trueLabel
                    self.expList[0].id.falseLabel = self.falseLabel
                else:pass
                singleId = self.expList[0].id.compile(enviroment)
            if len(self.expList) == 1:
                #Se retornan Variables que sean normales, arrays, vectores y structs
                return singleId
            else:
                #Se retornan atributos de structs
                if isinstance(self.expList[0].id.id,AccessArray):
                    return self.returnAttribute(exist,exist.typeVar,self.expList,1,exist.temporal,enviroment)
                else:
                    temporal = enviroment.generator.generateTemporal()
                    exist = self.expList[0].id.compile(enviroment)
                    returned = self.returnAttribute(exist,exist.typeVar,self.expList,1,exist.temporal,enviroment,self.expList[0].id.id)
                    if returned != None:                    
                        CODE = f'  {temporal} = Heap[(int) {exist.temporal}];\n'
                        CODE += returned.code
                        return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)
                    return None
        else:listError.append(Error("Error: La variable "+str(self.expList[0].id.id)+" no existe","Local",self.row,self.column,"SEMANTICO"))
    
    def returnAttribute(self, variable, accesstypeVar, attList, number, temporal, enviroment,id):
        foundedStruct = searchInListStructsAux(accesstypeVar)
        singleHandler = Handler(variable.typeIns,variable.typeVar,variable.typeSingle,variable.label,variable.code,variable.temporal,variable.att)
        singleHandler.id = id
        if isinstance(attList[number].id,CallNative):
            callNativeFunction = Native(singleHandler,attList[number].id,self.row,self.column)
            return callNativeFunction.compile(enviroment)
        else:
            cont = 0
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