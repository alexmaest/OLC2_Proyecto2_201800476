from AST.Abstracts.Expression import Expression
from enum import Enum

class ModInstruction():
    def __init__(self, isPublic, instruction):
        self.isPublic = isPublic
        self.instruction = instruction
    
    def compile(self, enviroment):
        self.instruction.compile(enviroment)