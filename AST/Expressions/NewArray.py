from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class NewArray():

    finalArray = []

    def __init__(self, listExp, row, column):
        self.listExp = listExp
        self.row = row
        self.column = column
        self.finalArray = []

    def executeInstruction(self,enviroment):
        self.finalArray = []
        typeArray = None
        typeDimension = None
        lenDimension = None
        for singleExp in self.listExp:
            exp = singleExp.executeInstruction(enviroment)
            if exp != None:
                if typeArray == None and typeDimension == None:
                    typeArray = exp.typeVar
                    typeDimension = exp.typeSingle
                    self.finalArray.append(exp)
                    if typeDimension == TYPE_DECLARATION.ARRAY:
                        lenDimension = len(exp.value)
                else:
                    if exp.typeVar == typeArray:
                        if exp.typeSingle == typeDimension:
                            if typeDimension == TYPE_DECLARATION.ARRAY:
                                if lenDimension == len(exp.value):
                                    self.finalArray.append(exp)
                                else:
                                    listError.append(Error("Error: No se ha podido crear la lista debido a que todas las expresiones no son de la misma longitud","Local",self.row,self.column,"SEMANTICO"))    
                                    return None
                            else:
                                self.finalArray.append(exp)
                        else:
                            listError.append(Error("Error: No se ha podido crear la lista debido a que todas las expresiones no son de la misma dimensión","Local",self.row,self.column,"SEMANTICO"))    
                            return None
                    else:
                        listError.append(Error("Error: No se ha podido crear la lista debido a que todas las expresiones no son del mismo tipo","Local",self.row,self.column,"SEMANTICO"))    
                        return None
            else:
                return None
        return Retorno(typeArray,self.finalArray,TYPE_DECLARATION.ARRAY)