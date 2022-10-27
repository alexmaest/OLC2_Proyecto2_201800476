from AST.Abstracts.Instruccion import Instruccion
from AST.Expressions.AttAccess import AttAccess
from AST.Error.Error import Error
from AST.Error.ErrorList import listError
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION

class Match(Instruccion):
    def __init__(self, expression, statement, row, column):
        self.expression = expression
        self.isExpSentence = False
        self.statement = statement
        self.row = row
        self.column = column

    def compile(self, enviroment):
        singleExp = self.expression.compile(enviroment)
        if singleExp != None:
            #Validación si se encuentra el caso '_'
            founded = False
            if self.isExpSentence: 
                self.statement.isLoopOrFunction = False
                self.statement.isExpSentence = True
            for arm in self.statement.instructions:
                armExps = arm.getExpressions()
                for singleArmExp in armExps:
                    if isinstance(singleArmExp,AttAccess):
                        if singleArmExp.expList[0].id.id == '_' and self.statement.instructions[-1] == arm:
                            founded = True
            fail = False
            returned = None
            if founded:
                exitLabel = enviroment.generator.generateLabel()
                CODE = '/* MATCH */\n'
                CODE += singleExp.code
                falseLabel = ''
                default = False
                for arm in self.statement.instructions:
                    armExps = arm.getExpressions()
                    trueLabels = ''
                    for singleArmExp in armExps:
                        if isinstance(singleArmExp,AttAccess):
                            if singleArmExp.expList[0].id.id  == '_':
                                default = True
                                if self.isExpSentence: 
                                    arm.isLoopOrFunction = False
                                    arm.isExpSentence = True
                                instructions = arm.compile(enviroment)
                                CODE += f'{falseLabel}:\n'
                                CODE += instructions.code
                            else:
                                if self.isExpSentence: 
                                    singleArmExp.isLoopOrFunction = False
                                    singleArmExp.isExpSentence = True
                                returned = singleArmExp.compile(enviroment)
                                if returned != None:
                                    if singleExp.typeVar == returned.typeVar:
                                        if singleExp.typeSingle == returned.typeSingle:
                                            if falseLabel != '': CODE += f'{falseLabel}:\n'
                                            trueLabel = enviroment.generator.generateLabel()
                                            falseLabel = enviroment.generator.generateLabel()
                                            CODE += returned.code
                                            CODE += f'   if({singleExp.temporal} == {returned.temporal}) goto {trueLabel};\n'
                                            CODE += f'   goto {falseLabel};\n'
                                            trueLabels += f'{trueLabel}:\n'
                                        else:
                                            listError.append(Error("Error: El valor que desea comparar no posee las dimensiones correctas","Local",self.row,self.column,"SEMANTICO"))
                                            fail = True
                                            break
                                    else:
                                        listError.append(Error("Error: El valor que desea comparar no posee el tipo correcto","Local",self.row,self.column,"SEMANTICO"))
                                        fail = True
                                        break
                                else:
                                    listError.append(Error("Error: El valor del brazo es nulo","Local",self.row,self.column,"SEMANTICO"))
                                    fail = True
                                    break
                        else:
                            if self.isExpSentence: 
                                singleArmExp.isLoopOrFunction = False
                                singleArmExp.isExpSentence = True
                            returned = singleArmExp.compile(enviroment)
                            if returned != None:
                                if singleExp.typeVar == returned.typeVar:
                                    if singleExp.typeSingle == returned.typeSingle:
                                        if falseLabel != '': CODE += f'{falseLabel}:\n'
                                        trueLabel = enviroment.generator.generateLabel()
                                        falseLabel = enviroment.generator.generateLabel()
                                        CODE += returned.code
                                        CODE += f'   if({singleExp.temporal} == {returned.temporal}) goto {trueLabel};\n'
                                        CODE += f'   goto {falseLabel};\n'
                                        trueLabels += f'{trueLabel}:\n'
                                    else:
                                        listError.append(Error("Error: El valor que desea comparar no posee las dimensiones correctas","Local",self.row,self.column,"SEMANTICO"))
                                        fail = True
                                        break
                                else:
                                    listError.append(Error("Error: El valor que desea comparar no posee el tipo correcto","Local",self.row,self.column,"SEMANTICO"))
                                    fail = True
                                    break
                            else:
                                listError.append(Error("Error: El valor del brazo es nulo","Local",self.row,self.column,"SEMANTICO"))
                                fail = True
                                break
                    if not default:
                        if self.isExpSentence: 
                            arm.isLoopOrFunction = False
                            arm.isExpSentence = True
                        instructions = arm.compile(enviroment)
                        CODE += trueLabels
                        CODE += instructions.code
                        CODE += f'   goto {exitLabel};\n'
                CODE += f'{exitLabel}:\n'
                if fail: return None
                else: return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)
            else:listError.append(Error("Error: El brazo '_' debe de ser el último de la sentencia match","Local",self.row,self.column,"SEMANTICO"))
        else:listError.append(Error("Error: No se ha podido ejecutar la sentencia match porque su valor a comparar es nulo","Local",self.row,self.column,"SEMANTICO"))