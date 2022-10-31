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

    def compile(self,enviroment):
        #Buscar función
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
                count = 0
                if self.isMain:
                    newEnv.isMain = True
                    founded.statement.isMain = True
                else:pass
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
                                            singleValue = self.parameters[count].compile(enviroment)
                                            singleHandler = Handler(singleValue.typeIns,singleValue.typeVar,singleValue.typeSingle,singleValue.label,singleValue.code,singleValue.temporal,singleValue.att)
                                            singleHandler.dimensions = exist.dimensions
                                            singleParam = DeclarationSingle(param,singleHandler,self.row,self.column)   
                                            singleParam.newEnv = newEnv
                                            singleParam.isParam = True
                                            singleParam.oldSize = enviroment.size
                                            singleParam.isReference = True
                                            returned = singleParam.compile(newEnv)
                                            if returned != None: PARAM_CODE += returned.code
                                            else: return None
                                            count+=1
                                        else:
                                            singleValue = self.parameters[count].compile(enviroment)
                                            singleHandler = Handler(singleValue.typeIns,singleValue.typeVar,singleValue.typeSingle,singleValue.label,singleValue.code,singleValue.temporal,singleValue.att)
                                            singleHandler.dimensions = exist.dimensions
                                            singleParam = DeclarationSingle(param,singleHandler,self.row,self.column)   
                                            singleParam.newEnv = newEnv
                                            singleParam.isParam = True
                                            singleParam.oldSize = enviroment.size
                                            returned = singleParam.compile(newEnv)
                                            if returned != None: PARAM_CODE += returned.code
                                            else: return None
                                            count+=1
                                    else:
                                        listError.append(Error("Error: Se esperaba una referencia diferente de la variable que ingresó como parametro","Local",self.row,self.column,"SEMANTICO"))
                                        Fail = True
                                        break
                                else:
                                    if not param.reference:
                                        singleValue = self.parameters[count].compile(enviroment)
                                        singleHandler = Handler(singleValue.typeIns,singleValue.typeVar,singleValue.typeSingle,singleValue.label,singleValue.code,singleValue.temporal,singleValue.att)
                                        singleHandler.dimensions = exist.dimensions
                                        singleParam = DeclarationSingle(param,singleHandler,self.row,self.column)   
                                        singleParam.newEnv = newEnv
                                        singleParam.isParam = True
                                        singleParam.oldSize = enviroment.size
                                        returned = singleParam.compile(newEnv)
                                        if returned != None: PARAM_CODE += returned.code
                                        else: return None
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
                        returned = singleParam.compile(newEnv)
                        if returned != None: PARAM_CODE += returned.code
                        else: return None
                        count+=1
                
                if not Fail:
                    #Generar codigo de la función
                    CODE = ''
                    returnedValue = None
                    if not self.isMain:
                        CODE = f'/* LLAMADA A LA FUNCIÓN {self.id} */\n'
                        if len(founded.parameters) > 0: CODE += PARAM_CODE
                        CODE += f'  SP = SP + {enviroment.size};\n'
                        CODE += f'  {self.id}();\n'
                        CODE += f'  SP = SP - {enviroment.size};\n'
                        founded.statement.newEnv = newEnv
                        returnedValue = founded.statement.compile(newEnv)
                    else:
                        returnedValue = founded.statement.compile(newEnv)
                    
                    #Retornar valor si lo tiene
                    callTypeVar = None
                    callTypeSingle = None
                    returnTemporal = None
                    callAtt = None
                    if returnedValue.typeVar != None and founded.type != None:
                        typeReturned = founded.type.compile(newEnv)
                        if typeReturned != None:
                            if returnedValue.typeVar == typeReturned.typeVar:
                                if returnedValue.typeSingle == typeReturned.typeSingle:
                                    temporal = enviroment.generator.generateTemporal()
                                    returnTemporal = enviroment.generator.generateTemporal()
                                    callTypeVar = returnedValue.typeVar
                                    callTypeSingle = returnedValue.typeSingle
                                    callAtt = returnedValue.att
                                    CODE += f'  {temporal} = SP + {enviroment.size};\n'
                                    CODE += f'  {returnTemporal} = Stack[(int){temporal}];\n'
                                else: 
                                    listError.append(Error("Error: El tipo de dimensión para la función "+str(founded.id)+" no es valido con el valor que intenta retornar","Local",self.row,self.column,"SEMANTICO"))
                                    return None
                            else: 
                                listError.append(Error("Error: El tipo de dato para la función "+str(founded.id)+" no es valido con el valor que intenta retornar","Local",self.row,self.column,"SEMANTICO"))
                                return None
                        else: 
                            listError.append(Error("Error: El tipo de dato declarado para la función "+str(founded.id)+" no es valido","Local",self.row,self.column,"SEMANTICO"))
                            return None
                    elif returnedValue.typeVar != None and founded.type == None:
                        listError.append(Error("Error: No puede retornar valores en la función "+str(self.id)+" tipo void","Local",self.row,self.column,"SEMANTICO"))
                        return None
                    elif returnedValue.typeVar == None and founded.type != None:
                        listError.append(Error("Error: Debe de retonar algún valor en esta función","Local",self.row,self.column,"SEMANTICO"))
                        return None
                    else: pass #ya se validó todo

                    #Agregar código de la función generada
                    self.generateFunction(founded,enviroment,returnedValue.code)

                    #Retorno de la llamada
                    return Retorno(None,callTypeVar,callTypeSingle,None,CODE,returnTemporal,callAtt)

            else: listError.append(Error("Error: El número de parametros que ingresó para la función "+str(self.id)+"no son los correctos","Local",self.row,self.column,"SEMANTICO"))
        else: listError.append(Error("Error: No se pudo encontrar la función con id "+str(self.id),"Local",self.row,self.column,"SEMANTICO"))

    def generateFunction(self, function, enviroment, functionCode):
        if not function.generated:
            result = re.findall("ReturnLabel",functionCode)
            returnLabel = ''
            if len(result) > 0:
                returnLabel = enviroment.generator.generateLabel()
                functionCode = functionCode.replace("ReturnLabel",returnLabel)
                returnLabel = returnLabel + ':\n'
            else:pass
            CODE = f'void {function.id}(){{\n'
            CODE += functionCode
            CODE += returnLabel
            CODE += '  return;\n'
            CODE += '}\n\n'
            enviroment.generator.addFunction(CODE)
            function.generated = True
        else:pass #La función ya se ha generado anteriormente