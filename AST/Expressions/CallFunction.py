from AST.Expressions.Handler import Handler
from AST.Abstracts.Expression import Expression
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.AttAccess import AttAccess
from AST.Expressions.ParamReference import ParamReference
from AST.Instructions.DeclarationSingle import DeclarationSingle
from AST.Symbol.Enviroment import Enviroment
from AST.Error.Error import Error
from AST.Error.ErrorList import listError

class CallFunction():
    def __init__(self, id, parameters, row, column):
        self.id = id
        self.parameters = parameters
        self.row = row
        self.column = column
        self.newEnviroment = None 
        self.newFunction = None
        self.positions = []

    def compile(self,enviroment):
        #Buscar función
        #Crear entorno
        founded = enviroment.getFunction(self.id)
        newEnv = Enviroment(enviroment.getGlobal(),enviroment.generator)
        if founded != None or self.newEnviroment != None:
            #Ejecución de parametros
            #Validar referencia
            Fail = False
            if not Fail:
                CODE = f'/* LLAMADA A LA FUNCIÓN {self.id}'
                #Ejecutar instrucciones de la función
                enviroment.generator.agregarFuncion(founded.compile(newEnv))
                CODE += f'SP = SP + {enviroment.size};'
                CODE += f'{self.id}();'
                CODE += f'SP = SP - {enviroment.size};'
                return CODE
                #Retornar valor si lo tiene

            #Modificar de regreso las variables que se enviaron con referencia
            #else:
            #    listError.append(Error("Error: El número de parametros que ingresó para la función "+str(self.id)+"no son los correctos","Local",self.row,self.column,"SEMANTICO"))
        #else:
        #    listError.append(Error("Error: No se pudo encontrar la función con id "+str(self.id),"Local",self.row,self.column,"SEMANTICO"))