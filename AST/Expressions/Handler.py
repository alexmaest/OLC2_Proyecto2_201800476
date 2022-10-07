from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.Literal import Literal

class Handler():
    def __init__(self, typeVar, value, typeSingle):
        self.typeVar = typeVar
        self.value = value
        self.typeSingle = typeSingle

    def compile(self,enviroment):
        singleValue = Literal(self.typeVar,self.value)
        return singleValue.compile(enviroment)