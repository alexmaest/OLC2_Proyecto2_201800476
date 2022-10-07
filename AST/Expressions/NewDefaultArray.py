from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class NewDefaultArray():

    finalArray = []

    def __init__(self, value, size, row, column):
        self.value = value
        self.size = size
        self.row = row
        self.column = column
        self.finalArray = []

    def executeInstruction(self,enviroment):
        self.finalArray = []
        singleValue = self.value.executeInstruction(enviroment)
        singleSize = self.size.executeInstruction(enviroment)
        if singleValue != None and singleSize != None:
            if singleSize.typeVar == TYPE_DECLARATION.INTEGER:
                for number in range(singleSize.value):
                    self.finalArray.append(singleValue)
                return Retorno(singleValue.typeVar,self.finalArray,TYPE_DECLARATION.ARRAY)
            else:
                listError.append(Error("Error: No se ha podido crear la lista debido a que el tamaño para la lista no es un entero","Local",self.row,self.column,"SEMANTICO"))    
                return None
        else:
            listError.append(Error("Error: No se ha podido crear la lista","Local",self.row,self.column,"SEMANTICO"))  
            return None