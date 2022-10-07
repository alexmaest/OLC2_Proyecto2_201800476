class Generator():
    def __init__(self):
        self.generator = ""
        self.code = ""
        self.externCode = ""
        self.temporal = 0
        self.label = 0

    def obtenerTemporal(self):
        temp = "T"+self.temporal.__str__()
        self.temporal += 1
        return temp

    def obtenerEtiqueta(self):
        et = "L"+self.label.__str__()
        self.label += 1
        return et

    def agregarFuncion(self,code):
        self.externCode += code

    def generarEncabezado(self):
        encabezado = """ 
#include <stdio.h>
float Stack[10000];
float Heap[10000];
int SP = 0;
int HP = 0;\n"""
        if self.temporal > 0:
            encabezado += "float "
        for i in range(0, self.temporal):
            if i % 15 == 0 and i > 0:
                encabezado += "\n"
            encabezado += f"T{i}"
            if i < self.temporal - 1:
                encabezado += ","
        if self.temporal > 0:
            encabezado += "; \n\n"
        return encabezado

    def agregarInstruccion(self,code):
        #print(code)
        self.code += code + '\n'

    def generarMain(self):
        code = self.generarEncabezado()
        code += "int main(){ \n" \
                  f"{self.code} \n" \
                  f"return 0;" \
                  "\n}\n"
        code += self.externCode
        return code