from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.CallFunction import CallFunction

class AccessTypeVector():
    def __init__(self, accessType):
        self.accessType = accessType

    def executeInstruction(self, enviroment):
            returned = self.accessType.executeInstruction(enviroment)
            if returned != None:
                return Retorno(returned.typeVar,returned.value,TYPE_DECLARATION.VECTOR)
            else:
                return None