from enum import Enum

class TYPE_DECLARATION(Enum):
    #Tipos de retornos
    INSTRUCCION = 15
    VALOR = 16
    #Tipos de variables
    INTEGER = 0,
    FLOAT = 1,
    STRING = 2,
    aSTRING = 3,
    BOOLEAN = 4,
    CHAR = 5,
    USIZE = 6,
    NULL = 7,
    #Tipos de 'dimensiones' de variables
    SIMPLE = 8,
    ARRAY = 9,
    VECTOR = 10,
    STRUCT = 11,
    #Tipos de transferencia
    BREAK = 12,
    RETURN = 13,
    CONTINUE = 14

class Retorno():
    def __init__(self, typeIns, typeVar, value, typeSingle, label, code, temporal):
        self.typeIns = typeIns
        self.typeVar = typeVar
        self.value = value
        self.typeSingle = typeSingle
        self.label = label
        self.code = code
        self.temporal = temporal
        self.trueLabel = ''
        self.falseLabel = ''
    
    def getValue(self):
        return self.value