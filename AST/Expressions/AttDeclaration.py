from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class AttDeclaration():

    def __init__(self, isPublic, id, type):
        self.isPublic = isPublic
        self.id = id
        self.type = type

    def compile(self,enviroment):
        return self.type.compile(enviroment)