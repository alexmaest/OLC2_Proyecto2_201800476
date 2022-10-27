from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class AssignmentSimple(Instruccion):

    def __init__(self,mutable,id,type,reference):
        self.mutable = mutable
        self.id = id
        self.type = type
        self.reference = reference
    
    def compile(self, enviroment):
        typeVar = self.type.compile(enviroment)
        if typeVar != None:
            if typeVar.typeSingle == TYPE_DECLARATION.VECTOR:
                content = []
                content.append(self.mutable)
                content.append(self.id)
                content.append(self.reference)
                content.append(typeVar.typeVar)
                return Retorno(None,content,TYPE_DECLARATION.VECTOR,None,None,None,None)
            elif typeVar.typeSingle == TYPE_DECLARATION.ARRAY:
                content = []
                content.append(self.mutable)
                content.append(self.id)
                content.append(self.reference)
                content.append(typeVar.typeVar)
                return Retorno(None,content,TYPE_DECLARATION.ARRAY,None,None,None,None)
            elif typeVar.typeSingle == TYPE_DECLARATION.STRUCT:
                content = []
                content.append(self.mutable)
                content.append(self.id)
                content.append(self.reference)
                content.append(typeVar.typeVar)
                return Retorno(None,content,TYPE_DECLARATION.STRUCT,None,None,None,None)
            else:
                content = []
                content.append(self.mutable)
                content.append(self.id)
                content.append(self.reference)
                content.append(typeVar.typeVar)
                return Retorno(None,content,TYPE_DECLARATION.SIMPLE,None,None,None,None)