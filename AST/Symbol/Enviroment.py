from AST.Symbol.Symbol import Symbol
from AST.Symbol.SymbolList import listModules, listStructs, listFunctions, listVariables
class Enviroment():

    variables = []
    modules = []
    structs = []
    functions = []

    def __init__(self, previous, generator):
        self.generator = generator
        self.previous = previous
        self.variables = []
        self.modules =  []
        self.structs =  []
        self.functions = []
        self.size = 1

    def saveVariable(self, variable):
        env = self
        while (env != None):
            for single in env.variables:
                if single.id == variable.id:
                    print("Error: La Variable con id",variable.id,"ya existe")
                    return False
            env = env.previous
        self.variables.append(variable)
        listVariables.append(variable)
        self.size += 1
        print("Información: La Variable con id",variable.id,"fué agregada")
        return True
        
    def editVariable(self, id, value):
        env = self
        while (env != None):
            for single in env.variables:
                if single.id == id:
                    single.value = value
                    break
            env = env.previous

    def getVariable(self, id):
        env = self
        while(env != None):
            for single in env.variables:
                if single.id == id:
                    return single
            env = env.previous
        return None

    def saveFunction(self, id, function):
        env = self
        while (env != None):
            for single in env.functions:
                if single.id == id:
                    print("Error: La Función con id",id,"ya existe")
                    return False
            env = env.previous
        self.functions.append(function)
        listFunctions.append(function)
        print("Información: La Función con id",id,"fué agregada")
        return True
    
    def getFunction(self, id):
        env = self
        while(env != None):
            for single in env.functions:
                if single.id == id:
                    return single
            env = env.previous
        return None
    
    def getGlobal(self):
        env = self
        while(env.previous != None):
            env = env.previous
        return env

    def saveStruct(self, id, struct):
        env = self
        while (env != None):
            for single in env.structs:
                if single.id == id:
                    print("Error: El struct con id",id,"ya existe")
                    return False
            env = env.previous
        self.structs.append(struct)
        listStructs.append(struct)
        #print("Información: El struct con id",id,"fué agregado")
        return True

    def getStruct(self, id):
        env = self
        while(env != None):
            for single in env.structs:
                if single.id == id:
                    return single
            env = env.previous
        return None

    def saveModule(self, id, module):
        env = self
        while (env != None):
            for single in env.modules:
                if single.id == id:
                    print("Error: El modulo con id",id,"ya existe")
                    return False
            env = env.previous
        self.modules.append(module)
        listModules.append(module)
        #print("Información: El modulo con id",id,"fué agregado")
        return True

    def getModule(self, id):
        env = self
        while(env != None):
            for single in env.modules:
                if single.id == id:
                    return single
            env = env.previous
        return None