class Generator():
    def __init__(self):
        self.generator = ''
        self.code = ''
        self.temporalCount = 0
        self.labelCount = 0

    def generateTemporal(self):
        singleTemp = 'T' + str(self.temporalCount)
        self.temporalCount += 1
        return singleTemp

    def generateLabel(self):
        singleLabel = 'L' + str(self.labelCount)
        self.labelCount += 1
        return singleLabel

    def addFunction(self,code):
        self.code += code

    def generateHeader(self):
        header = '#include <stdio.h>\n'
        header += 'float Stack[10000];\n'
        header += 'float Heap[10000];\n'
        header += 'int SP = 0;\n'
        header += 'int HP = 0;\n'
        if self.temporalCount > 0:
            header += 'float '
        for i in range(0, self.temporalCount):
            if i % 15 == 0 and i > 0:
                header += '\n'
            header += f'T{i}'
            if i < self.temporalCount - 1:
                header += ','
        if self.temporalCount > 0:
            header += ';\n\n'
        return header