from AST.Abstracts.Expression import Expression
from enum import Enum

class AttAssign():
    def __init__(self, id):
        self.id = id
    
    def compile(self, enviroment):
        return self.id.compile(enviroment)