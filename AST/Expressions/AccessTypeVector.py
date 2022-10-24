from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.CallFunction import CallFunction

class AccessTypeVector():
    def __init__(self, accessType):
        self.accessType = accessType

    def compile(self, enviroment):
        returned = self.accessType.compile(enviroment)
        if returned != None:return Retorno(None,returned.typeVar,TYPE_DECLARATION.VECTOR,None,returned.code,None)
        else:return None