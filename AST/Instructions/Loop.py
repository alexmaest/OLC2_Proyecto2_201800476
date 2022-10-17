from AST.Abstracts.Instruccion import Instruccion
from AST.Abstracts.Retorno import Retorno, TYPE_DECLARATION
import re

class Loop(Instruccion):
    def __init__(self, statement):
        self.statement = statement

    def compile(self, enviroment):
        loopLabel = enviroment.generator.generateLabel()
        returned = self.statement.compile(enviroment)
        breakLabel = ''
        continueLabel = ''
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
        CODE = '/* LOOP */\n'
        CODE += f'{loopLabel}:\n'
        CODE += continueLabel
        CODE += returned.code
        CODE += f'  goto {loopLabel};\n'
        CODE += breakLabel
        return Retorno(returned.typeIns,returned.typeVar,returned.value,returned.typeSingle,None,CODE,None)