from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
import re

class Loop(Instruccion):
    def __init__(self, statement):
        self.isExpSentence = False
        self.statement = statement

    def compile(self, enviroment):
        breakLabel = ''
        continueLabel = ''
        returnLabel = ''
        loopLabel = enviroment.generator.generateLabel()
        returned = self.statement.compile(enviroment)
        functionCode = returned.code
        result = re.findall("BreakLabel",functionCode)
        if len(result) > 0:
            breakLabel = enviroment.generator.generateLabel()
            functionCode = functionCode.replace("BreakLabel",breakLabel)
            breakLabel = breakLabel + ':\n'
        result = re.findall("ContinueLabel",functionCode)
        if len(result) > 0:
            continueLabel = enviroment.generator.generateLabel()
            functionCode = functionCode.replace("ContinueLabel",continueLabel)
            continueLabel = continueLabel + ':\n'
        if self.isExpSentence:
            result = re.findall("ReturnLabel",functionCode)
            if len(result) > 0:
                returnLabel = enviroment.generator.generateLabel()
                functionCode = functionCode.replace("ReturnLabel",returnLabel)
                returnLabel = returnLabel + ':\n'
        CODE = '/* LOOP */\n'
        CODE += f'{loopLabel}:\n'
        CODE += continueLabel
        CODE += functionCode
        CODE += f'  goto {loopLabel};\n'
        CODE += breakLabel
        CODE += returnLabel
        return Retorno(returned.typeIns,returned.typeVar,returned.typeSingle,returned.label,CODE,returned.temporal,returned.att)