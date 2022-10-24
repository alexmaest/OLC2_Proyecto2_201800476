from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class AttCall():

    def __init__(self, id, expression):
        self.id = id
        self.expression = expression

    def compile(self,enviroment):
        return self.expression.compile(enviroment)