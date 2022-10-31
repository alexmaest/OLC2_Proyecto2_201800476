from Grammar.parser import startParser, getGlobalEnv
from AST.Error.ErrorList import getErrorList
from AST.Reports.ReportDBExist import *
from AST.Reports.ReportSymbol import *
from AST.Reports.ReportError import *
from AST.Reports.ReportDB import *
from AST.Symbol.SymbolList import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import tkinter as t

def searchFile():
    try:
        win = Tk()
        win.geometry("1x1")
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select a File", filetypes=(("Rust files", "*.rs*"), ("All files", "*.*")))
        f = open(filename, "r")
        editorBox.delete('1.0', END)
        editorBox.insert(END,f.read())
        f.close()
        win.destroy()
        messagebox.showinfo("Información","Carga de archivo realizada correctamente")
    except:
        messagebox.showinfo("Información","Hubo un problema con la carga del archivo, intente nuevamente")

def errorReport():
    list = getErrorList()
    ReportError(list)

def symbolReport():
    mList = getModuleList()
    sList = getStructList()
    fList = getFunctionList()
    vList = getVariableList()
    ReportSymbol(mList,fList,sList,vList)

def dbExistReport():
    globalEnv = getGlobalEnv()
    ReportDBExist(globalEnv.modules)

def dbReport():
    globalEnv = getGlobalEnv()
    ReportDB(globalEnv.modules)

def start():
    editorTempText = editorBox.get("1.0", "end-1c")
    consoleBox.delete('1.0', END)
    startParser(editorTempText,consoleBox)

v = t.Tk()
v.geometry("1170x720")
v.resizable(False, False)
v.title("DB-RUST Interpeter")

tabControl = ttk.Notebook(v)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Inicio')
tabControl.add(tab2, text ='Reportes')
tabControl.add(tab3, text ='Acerca De')
tabControl.pack(expand = 1, fill ="both")

#TAB 1
editorBox = Text(tab1, fg="#96e0ff", bg ="#171717", height=24, width=166, font = "Arial 10")
editorBox.place(x=0, y=65)
consoleBox = Text(tab1, fg="#969696", bg ="black", height=13, width=146)
consoleBox.place(x=0, y=470)
t.Label(tab1, text="", width=200, height=4, bg = "#333333").place(x=0, y=0)
t.Label(tab1, text="DB RUST", fg="#fcba03", width=7, height=1, bg = "#333333", font = "Helvetica 18 bold italic").place(x=30, y=15)
t.Button(tab1, text="▶", width=2, font = "Helvetica 12 bold",fg="#ffffff", bg='#1d8a5c', command=start).place(x=980, y=15)
t.Button(tab1, text="Cargar archivo", width=12, font = "Arial 12",fg="#ffffff", bg='#333333', command=searchFile).place(x=1010, y=15)
t.Label(tab1, text="Terminal", width=130, fg="#969696", bg = "black", font = "Helvetica 12").place(x=0, y=450)
t.Label(tab1, text = "                                   2022 - Proyecto 2 de Organización de Lenguajes y Compiladores 2", width=260, fg="#ffffff", bg = "#1486ff").place(x=0, y=675)

#TAB 2
t.Label(tab2, text="", width=200, height=400, bg = "#171717").place(x=0, y=60)
t.Label(tab2, text="", width=200, height=4, bg = "#333333").place(x=0, y=0)
t.Label(tab2, text="", width=157, height=36, bg = "black").place(x=30, y=100)
t.Label(tab2, text="Tabla de simbolos", width=20, fg="#969696", bg = "black", font = "Helvetica 12").place(x=80, y=270)
t.Button(tab2, text="Generar", width=12, font = "Arial 12",fg="#ffffff", bg='#333333', command=symbolReport).place(x=115, y=320)
t.Label(tab2, text="Tabla de bases de datos existentes", width=30, fg="#969696", bg = "black", font = "Helvetica 12").place(x=320, y=270)
t.Button(tab2, text="Generar", width=12, font = "Arial 12",fg="#ffffff", bg='#333333', command=dbExistReport).place(x=400, y=320)
t.Label(tab2, text="Tablas de bases de datos", width=20, fg="#969696", bg = "black", font = "Helvetica 12").place(x=670, y=270)
t.Button(tab2, text="Generar", width=12, font = "Arial 12",fg="#ffffff", bg='#333333', command=dbReport).place(x=700, y=320)
t.Label(tab2, text="Reporte de errores", width=20, fg="#969696", bg = "black", font = "Helvetica 12").place(x=900, y=270)
t.Button(tab2, text="Generar", width=12, font = "Arial 12",fg="#ffffff", bg='#333333', command=errorReport).place(x=935, y=320)
t.Label(tab2, text="REPORTES", fg="#fcba03", width=10, height=1, bg = "#333333", font = "Helvetica 18 bold italic").place(x=20, y=15)
t.Label(tab2, text = "                                   2022 - Proyecto 2 de Organización de Lenguajes y Compiladores 2", width=260, fg="#ffffff", bg = "#1486ff").place(x=0, y=675)

info = """Rust es un lenguaje de programación que está tomando fuerza en los últimos años,
este cuenta con muchas características que lo hacen un lenguaje muy completo y de gran uso
para el desarrollo de servidores backend. Rust se caracteriza por el uso de módulos lo que
permite guardar bloques de códigos con una lógica específica.

La idea del proyecto es que se desarrolle un simulador de bases de datos a través de los
módulos que ofrece Rust, donde un módulo padre representa una base de datos y sus módulos
hijos representan las tablas. Dentro de estas tablas existirán funciones para toda la
interacción de los datos, ya sea iniciar la tabla, insertar un dato, obtener un dato por
un atributo en específico, etc. No todas las tablas tendrán las mismas funciones, estas
pueden cambiar para tener diferentes interacciones con los datos."""

datos = """Marvin Alexis Estrada Florian
3007201810101
201800476"""

#TAB 3
t.Label(tab3, text="", width=200, height=400, bg = "#171717").place(x=0, y=60)
t.Label(tab3, text="", width=200, height=4, bg = "#333333").place(x=0, y=0)
t.Label(tab3, text="", width=157, height=36, bg = "black").place(x=30, y=100)
t.Label(tab3, text="ACERCA DE", fg="#fcba03", width=10, height=1, bg = "#333333", font = "Helvetica 18 bold italic").place(x=20, y=15)
t.Label(tab3, text="Acerca de la aplicación", width=20, fg="#fcba03", bg = "black", font = "Helvetica 12 italic").place(x=40, y=160)
t.Label(tab3, text=info, width=75, fg="#FFFFFF", bg = "black", font = "Helvetica 12", anchor="e", justify=LEFT).place(x=30, y=200)
t.Label(tab3, text="Datos del estudiante", width=19, fg="#fcba03", bg = "black", font = "Helvetica 12 italic").place(x=36, y=430)
t.Label(tab3, text=datos, width=23, fg="#FFFFFF", bg = "black", font = "Helvetica 12", anchor="e", justify=LEFT).place(x=46, y=460)
t.Label(tab3, text = "                                   2022 - Proyecto 2 de Organización de Lenguajes y Compiladores 2", width=260, fg="#ffffff", bg = "#1486ff").place(x=0, y=675)

v.mainloop()

#startParser(text,consoleBox)

for single in getErrorList():
    print(single.description)

'''
  printf("-----------------------------HEAP-----------------------------");
  printf("%c",(char) 10);
  printf("%d",(int) Heap[23]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[22]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[21]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[20]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[19]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[18]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[17]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[16]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[15]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[14]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[13]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[12]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[11]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[10]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[9]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[8]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[7]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[6]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[5]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[4]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[3]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[2]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[1]);
  printf("%c",(char) 10);
  printf("%d",(int) Heap[0]);
  printf("%c",(char) 10);
  printf("-----------------------------STACK-----------------------------");
  printf("%c",(char) 10);
  printf("%d",(int) Stack[23]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[22]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[21]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[20]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[19]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[18]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[17]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[16]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[15]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[14]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[13]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[12]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[11]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[10]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[9]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[8]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[7]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[6]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[5]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[4]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[3]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[2]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[1]);
  printf("%c",(char) 10);
  printf("%d",(int) Stack[0]);
  printf("%c",(char) 10);
'''