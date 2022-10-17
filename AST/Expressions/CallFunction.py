from AST.Abstracts.Expression import Expression
from AST.Expressions.Handler import Handler
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
from AST.Expressions.AttAccess import AttAccess
from AST.Expressions.ParamReference import ParamReference
from AST.Instructions.DeclarationSingle import DeclarationSingle
from AST.Symbol.Enviroment import Enviroment
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
import re

class CallFunction():
    def __init__(self, id, parameters, row, column):
        self.id = id
        self.parameters = parameters
        self.row = row
        self.column = column
        self.newEnviroment = None 
        self.newFunction = None
        self.isMain = False
        self.positions = []

    def compile(self,enviroment):
        #Buscar función
        self.positions = []
        Fail = False
        founded = None
        newEnv = None
        #Crear entorno
        if self.newEnviroment != None:
            founded = self.newFunction
            newEnv = Enviroment(self.newEnviroment,enviroment.generator)
        else:
            founded = enviroment.getFunction(self.id)
            newEnv = Enviroment(enviroment.getGlobal(),enviroment.generator)
        if founded != None or self.newEnviroment != None:
            #Ejecución de parametros
            if len(self.parameters) == len(founded.parameters):
                if self.isMain:
                    newEnv.isMain = True
                    founded.statement.isMain = True
                else:pass
                count = 0
                PARAM_CODE = '/* PARAMETROS */\n'
                for param in founded.parameters:
                    if isinstance(self.parameters[count], AttAccess) or isinstance(self.parameters[count], ParamReference):
                        exist = None
                        if isinstance(self.parameters[count], AttAccess):
                            exist = enviroment.getVariable(self.parameters[count].expList[0].id.id)
                        else:
                            exist = enviroment.getVariable(self.parameters[count].id.id)
                        if exist != None:
                            if exist.mutable == param.mutable:
                                #Validar referencia
                                if not isinstance(self.parameters[count], AttAccess):
                                    if self.parameters[count].reference == param.reference:
                                        if param.reference:
                                            self.positions.append(count)
                                            singleValue = self.parameters[count].compile(enviroment)
                                            referenceVar = enviroment.getVariable(self.parameters[count].id.id)
                                            singleParam = DeclarationSingle(param,Handler(singleValue.typeIns,singleValue.typeVar,referenceVar,singleValue.typeSingle,singleValue.label,singleValue.code,singleValue.temporal),self.row,self.column)   
                                            singleParam.newEnv = newEnv
                                            singleParam.isParam = True
                                            singleParam.oldSize = enviroment.size
                                            singleParam.isReference = True
                                            PARAM_CODE += singleParam.compile(newEnv).code          
                                            count+=1
                                        else:
                                            singleValue = self.parameters[count].compile(enviroment)
                                            singleParam = DeclarationSingle(param,Handler(singleValue.typeIns,singleValue.typeVar,singleValue.value,singleValue.typeSingle,singleValue.label,singleValue.code,singleValue.temporal),self.row,self.column)   
                                            singleParam.newEnv = newEnv
                                            singleParam.isParam = True
                                            singleParam.oldSize = enviroment.size
                                            PARAM_CODE += singleParam.compile(newEnv).code          
                                            count+=1
                                    else:
                                        listError.append(Error("Error: Se esperaba una referencia diferente de la variable que ingresó como parametro","Local",self.row,self.column,"SEMANTICO"))
                                        Fail = True
                                        break
                                else:
                                    if not param.reference:
                                        singleValue = self.parameters[count].compile(enviroment)
                                        singleParam = DeclarationSingle(param,Handler(singleValue.typeIns,singleValue.typeVar,singleValue.value,singleValue.typeSingle,singleValue.label,singleValue.code,singleValue.temporal),self.row,self.column)   
                                        singleParam.newEnv = newEnv
                                        singleParam.isParam = True
                                        singleParam.oldSize = enviroment.size
                                        PARAM_CODE += singleParam.compile(newEnv).code          
                                        count+=1
                                    else:
                                        listError.append(Error("Error: Se esperaba una referencia diferente de la variable que ingresó como parametro","Local",self.row,self.column,"SEMANTICO"))
                                        Fail = True
                                        break
                            else:
                                listError.append(Error("Error: La mutabilidad de la variable que ingresó como parametro es diferente a la declarada","Local",self.row,self.column,"SEMANTICO"))
                                Fail = True
                                break
                        else:
                            listError.append(Error("Error: La variable que ingresó como parametro no existe","Local",self.row,self.column,"SEMANTICO"))
                            Fail = True
                            break
                    else:
                        singleParam = DeclarationSingle(param,self.parameters[count],self.row,self.column)
                        singleParam.newEnv = newEnv
                        singleParam.isParam = True
                        singleParam.oldSize = enviroment.size
                        PARAM_CODE += singleParam.compile(newEnv).code     
                        count+=1
                
                if not Fail:
                    #Generar codigo de la función
                    CODE = ''
                    if not self.isMain:
                        CODE = f'/* LLAMADA A LA FUNCIÓN {self.id} */\n'
                        if len(founded.parameters) > 0:
                            CODE += PARAM_CODE
                        CODE += f'  SP = SP + {enviroment.size};\n'
                        CODE += f'  {self.id}();\n'
                        CODE += f'  SP = SP - {enviroment.size};\n'
                        founded.statement.newEnv = newEnv
                        returnedValue = founded.statement.compile(newEnv)
                        self.generateFunction(founded,enviroment,returnedValue.code)
                    else:
                        returnedValue = founded.statement.compile(newEnv)
                        self.generateFunction(founded,enviroment,returnedValue.code)
                    
                    #Retornar valor si lo tiene
                    callTypeVar = None
                    callTypeSingle = None
                    returnTemporal = None
                    callTypeIns = TYPE_DECLARATION.INSTRUCCION
                    if returnedValue.typeIns == TYPE_DECLARATION.VALOR:
                        if returnedValue != None and founded.type != None:
                            if returnedValue.typeSingle != TYPE_DECLARATION.BREAK and returnedValue.typeSingle != TYPE_DECLARATION.CONTINUE:
                                typeReturned = founded.type.compile(newEnv)
                                if typeReturned != None:
                                    callTypeIns = TYPE_DECLARATION.VALOR
                                    callTypeVar = returnedValue.typeVar
                                    callTypeSingle = returnedValue.typeSingle
                                    temporal = enviroment.generator.generateTemporal()
                                    returnTemporal = enviroment.generator.generateTemporal()
                                    CODE += f'  {temporal} = SP + {enviroment.size};\n'
                                    CODE += f'  {returnTemporal} = Stack[(int){temporal}];\n'
                                else: listError.append(Error("Error: La función "+str(founded.id)+" no puede retornar un valor porque no tiene un tipo de valor declarado","Local",self.row,self.column,"SEMANTICO"))
                            else: listError.append(Error("Error: Una función no puede retornar una sentencia break sin expresión o continue","Local",self.row,self.column,"SEMANTICO"))
                        elif returnedValue != None and founded.type == None:
                            listError.append(Error("Error: No puede retornar valores en la función "+str(self.id)+" tipo void","Local",self.row,self.column,"SEMANTICO"))
                        elif returnedValue == None and founded.type != None:
                            listError.append(Error("Error: Debe de retonar algún valor en esta función","Local",self.row,self.column,"SEMANTICO"))
                        else: pass #ya se validó todo
                    else: pass #ya se validó todo

                    #Modificar de regreso las variables que se enviaron con referencia
                    for number in self.positions:
                        returned = founded.statement.newEnv.getVariable(founded.parameters[number].id)
                        if returned != None:
                            if isinstance(self.parameters[number], AttAccess):
                                exist = enviroment.editVariable(self.parameters[number].id, returned.value)
                            else:
                                exist = enviroment.editVariable(self.parameters[number].id.id, returned.value)
                    return Retorno(callTypeIns,callTypeVar,returnedValue.value,callTypeSingle,None,CODE,returnTemporal)
            else:
                listError.append(Error("Error: El número de parametros que ingresó para la función "+str(self.id)+"no son los correctos","Local",self.row,self.column,"SEMANTICO"))
        else:
            listError.append(Error("Error: No se pudo encontrar la función con id "+str(self.id),"Local",self.row,self.column,"SEMANTICO"))

    def generateFunction(self, function, enviroment, functionCode):
        if not function.generated:
            returnLabel = ''
            result = re.findall("ReturnLabel",functionCode)
            if len(result) > 0:
                returnLabel = enviroment.generator.generateLabel()
                functionCode = functionCode.replace("ReturnLabel",returnLabel)
                returnLabel = returnLabel + ':\n'
            CODE = f'void {function.id}(){{\n'
            CODE += functionCode
            CODE += returnLabel
            CODE += '  return;\n'
            CODE += '}\n\n'
            enviroment.generator.addFunction(CODE)
            function.generated = True
        else:
            #La función ya se ha generado anteriormente
            pass