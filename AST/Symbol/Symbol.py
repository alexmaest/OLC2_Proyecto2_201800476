from AST.Abstracts.Expression import Expression
from enum import Enum

class Symbol():
    def __init__(self, typeVar, id, typeSingle, mutable, relativePosition, isReference, att, dimensions, row, column):
        self.typeVar = typeVar
        self.id = id
        self.typeSingle = typeSingle
        self.mutable = mutable
        self.relativePosition = relativePosition
        self.isReference = isReference
        self.att = att
        self.dimensions = dimensions
        self.row = row
        self.column = column