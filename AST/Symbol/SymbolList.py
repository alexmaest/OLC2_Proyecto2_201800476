listModules = []
listStructs = []
listFunctions = []
listVariables = []

def addModule(module):
    global listModules
    listModules.append(module)

def addStruct(struct):
    global listStructs
    listStructs.append(struct)

def addFunction(function):
    global listFunctions
    listFunctions.append(function)

def addVariable(variable):
    global listVariables
    listVariables.append(variable)

def getModuleList():
    return listModules

def getStructList():
    return listStructs

def getFunctionList():
    return listFunctions

def getVariableList():
    return listVariables

def setModuleList(list):
    global listModules
    listModules = list

def setStructList(list):
    global listStructs
    listStructs = list

def setFunctionList(list):
    global listFunctions
    listFunctions = list

def setVariableList(list):
    global listVariables
    listVariables = list