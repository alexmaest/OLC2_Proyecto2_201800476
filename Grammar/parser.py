from AST.Abstracts.Retorno import TYPE_DECLARATION, Retorno
from AST.Expressions.AccessTypeArray import AccessTypeArray
from AST.Expressions.AccessTypeVector import AccessTypeVector
from AST.Expressions.ModInstruction import ModInstruction
from AST.Expressions.CallFunction import CallFunction
from AST.Expressions.CallStruct import CallStruct
from AST.Expressions.ParamReference import ParamReference
from AST.Expressions.CallNative import CallNative, TYPE_NATIVE
from AST.Expressions.ForIterative import ForIterative
from AST.Expressions.Literal import Literal
from AST.Expressions.Access import Access
from AST.Expressions.AccessArray import AccessArray
from AST.Expressions.AccessInstruction import AccessInstruction
from AST.Expressions.ModAccess import ModAccess
from AST.Expressions.AttAccess import AttAccess
from AST.Expressions.AttAssign import AttAssign
from AST.Expressions.AttDeclaration import AttDeclaration
from AST.Expressions.AttCall import AttCall
from AST.Expressions.NewArray import NewArray
from AST.Expressions.NewDefaultArray import NewDefaultArray
from AST.Expressions.NewVector import NewVector
from AST.Expressions.Arithmetic import Arithmetic, TYPE_OPERATION
from AST.Expressions.ArithmeticPow import ArithmeticPow
from AST.Expressions.Relational import TYPE_RELATIONAL, Relational
from AST.Expressions.Logic import TYPE_LOGICAL, Logic
from AST.Instructions.Assignment import Assignment
from AST.Instructions.AssignmentSimple import AssignmentSimple
from AST.Instructions.Declaration import Declaration
from AST.Instructions.DeclarationSingle import DeclarationSingle
from AST.Instructions.ListArraySimple import ListArraySimple
from AST.Instructions.AssignmentAccessArray import AssignmentAccessArray
from AST.Instructions.Statement import Statement
from AST.Instructions.Modulo import Modulo
from AST.Instructions.Struct import Struct
from AST.Instructions.Function import Function
from AST.Instructions.Native import Native
from AST.Instructions.Cast import Cast
from AST.Instructions.Print import Print
from AST.Instructions.If import If
from AST.Instructions.Match import Match
from AST.Instructions.Arm import Arm
from AST.Instructions.Loop import Loop
from AST.Instructions.While import While
from AST.Instructions.For import For
from AST.Instructions.Break import Break
from AST.Instructions.Continue import Continue
from AST.Instructions.Return import Return
from AST.Expressions.Handler import Handler
from AST.Symbol.Generator import Generator
from AST.Symbol.Enviroment import Enviroment
from AST.Symbol.Symbol import Symbol
from Grammar.lexer import tokens

# Parsing precedence rules
precedence = (
    ('nonassoc', 'AS', 'IN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'AD'), 
    ('left', 'DIF', 'IGUALI', 'MENORI', 'MAYORI', 'MENOR', 'MAYOR'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('nonassoc', 'RPAR' , 'LPAR'),
    ('right', 'UMENOS')
)

def p_init(t):
    'init : instrucciones_g'
    t[0] = t[1]

def p_instrucciones_g(t):
    '''instrucciones_g : instrucciones_g instruccion_g
    | instruccion_g'''
    if t.slice[1].type == 'instrucciones_g':
        t[1].append(t[2])
        t[0] = t[1]
    else: t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion_g : modulo
    | struct
    | funcion'''
    t[0] = t[1]

def p_instrucciones_l(t):
    '''instrucciones_l : instrucciones_l instruccion_l
    | instruccion_l'''
    if t.slice[1].type == 'instrucciones_l':
        t[1].append(t[2])
        t[0] = t[1]
    else: t[0] = [t[1]]

def p_instruccion_l(t):
    '''instruccion_l : print PCOMA
    | declaracion PCOMA
    | asignacion PCOMA
    | llamada PCOMA
    | expstruct PCOMA
    | ID PUNTO exp_native PCOMA
    | sentencia
    | transferencia
    | transferencia PCOMA'''
    if len(t.slice) > 2:
        if t.slice[2].type == 'PUNTO': t[0] = Native(Access(t[1],t.lineno(1), t.lexpos(1)),t[3],t.lineno(1), t.lexpos(1))
        else: t[0] = t[1]
    else: t[0] = t[1]

def p_funcion(t):
    '''funcion : FN ID LPAR lista_parametros RPAR ARROW tipo_var statement
    | FN ID LPAR lista_parametros RPAR statement
    | FN ID LPAR RPAR ARROW tipo_var statement
    | FN ID LPAR RPAR statement'''
    if t.slice[4].type == 'lista_parametros':
        if t.slice[6].type == 'ARROW': t[0] = Function(t[2],t[4],t[7],t[8],t.lineno(1), t.lexpos(1))
        else: t[0] = Function(t[2],t[4],None,t[6],t.lineno(1), t.lexpos(1))
    else:
        if t.slice[5].type == 'ARROW': t[0] = Function(t[2],[],t[6],t[7],t.lineno(1), t.lexpos(1))
        else: t[0] = Function(t[2],[],None,t[5],t.lineno(1), t.lexpos(1))

def p_modulo(t):
    'modulo : MOD ID mod_statement'
    t[0] = Modulo(t[2],t[3],t.lineno(1), t.lexpos(1))

def p_mod_statement(t):
    '''mod_statement : LLLAV instrucciones_mod RLLAV
    | LLLAV RLLAV'''
    if t.slice[2].type == 'instrucciones_mod': t[0] = Statement(t[2])
    else: t[0] = Statement([])

def p_instrucciones_mod(t):
    '''instrucciones_mod : instrucciones_mod instruccion_mod
    | instruccion_mod'''
    if t.slice[1].type == 'instrucciones_mod':
        t[1].append(t[2])
        t[0] = t[1]
    else: t[0] = [t[1]]

def p_instruccion_mod(t):
    '''instruccion_mod : PUB modulo
    | PUB struct
    | PUB funcion
    | modulo
    | struct
    | funcion'''
    if t.slice[1].type == 'PUB': t[0] = ModInstruction(True,t[2])
    else: t[0] = ModInstruction(False,t[1])

def p_struct(t):
    '''struct : STRUCT ID LLLAV lista_var RLLAV
    | STRUCT ID LLLAV RLLAV'''
    if t.slice[4].type == 'lista_var': t[0] = Struct(t[2],t[4],t.lineno(1), t.lexpos(1))
    else: t[0] = Struct(t[2],[],t.lineno(1), t.lexpos(1))

def p_sentencia(t):
    '''sentencia : if
    | match
    | loop
    | while
    | for'''
    t[0] = t[1]

def p_if(t):
    'if : IF exp statement else'
    t[0] = If(t[2],t[3],t[4],t.lineno(1), t.lexpos(1))

def p_else(t):
    '''else : ELSE statement
    | ELSE if
    | epsilon'''
    if t.slice[1].type == 'ELSE': t[0] = t[2]

def p_epsilon(t):
    'epsilon :'
    t[0] = None

def p_match(t):
    'match : MATCH exp match_statement'
    t[0] = Match(t[2],t[3],t.lineno(1), t.lexpos(1))

def p_match_statement(t):
    '''match_statement : LLLAV lista_brazos RLLAV
    | LLLAV RLLAV'''
    if t.slice[2].type == 'RLLAV': t[0] = Statement([])
    else: t[0] = Statement(t[2])

def p_lista_brazos(t):
    '''lista_brazos : lista_brazos brazo
    | brazo'''
    if t.slice[1].type == 'lista_brazos':
        t[1].append(t[2])
        t[0] = t[1]
    else: t[0] = [t[1]]

def p_brazo(t):
    '''brazo : lista_exp_brazos ARROW2 instruccion_match COMA
    | lista_exp_brazos ARROW2 statement COMA
    | lista_exp_brazos ARROW2 statement'''
    t[0] = Arm(t[1],t[3])

def p_lista_exp_brazos(t):
    '''lista_exp_brazos : lista_exp_brazos ORSINGLE exp
    | exp'''
    if t.slice[1].type == 'lista_exp_brazos':
        t[1].append(t[3])
        t[0] = t[1]
    else: t[0] = [t[1]]

def p_instruction_match(t):
    '''instruccion_match : print
    | llamada
    | asignacion
    | sentencia
    | transferencia'''
    t[0] = t[1]

def p_loop(t):
    'loop : LOOP statement'
    t[0] = Loop(t[2])

def p_while(t):
    'while : WHILE exp statement'
    t[0] = While(t[2],t[3],t.lineno(1), t.lexpos(1))

def p_for(t):
    'for : FOR ID IN foriterative statement'
    t[0] = For(t[2],t[4],t[5],t.lineno(1), t.lexpos(1))

def p_foriterative(t):
    '''foriterative : exp PUNTO PUNTO exp
    | exp'''
    if len(t.slice) > 2:
        if t.slice[2].type == 'PUNTO': t[0] = ForIterative(t[1],t[4])
        else: t[0] = t[1]        
    else: t[0] = t[1]

def p_transferencia(t):
    '''transferencia : CONTINUE
    | BREAK
    | BREAK auxexp
    | RETURN
    | RETURN auxexp
    | auxexp'''
    if t.slice[1].type == 'CONTINUE': t[0] = Continue()
    elif t.slice[1].type == 'BREAK':
        if len(t.slice) > 2: t[0] = Break(t[2],t.lineno(1), t.lexpos(1))
        else: t[0] = Break(None,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'RETURN':
        if len(t.slice) > 2: t[0] = Return(t[2],t.lineno(1), t.lexpos(1))
        else: t[0] = Return(None,t.lineno(1), t.lexpos(1))
    else: t[0] = t[1]

def p_statement(t):
    '''statement : LLLAV instrucciones_l RLLAV
    | LLLAV RLLAV'''
    if t.slice[2].type == 'RLLAV': t[0] = Statement([])
    else: t[0] = Statement(t[2])

def p_lista_var(t):
    '''lista_var : lista_var COMA PUB ID DPUNTOS tipo_var
    | lista_var COMA ID DPUNTOS tipo_var
    | PUB ID DPUNTOS tipo_var
    | ID DPUNTOS tipo_var'''
    if t.slice[1].type == 'lista_var':
        if t.slice[3].type == 'PUB':
            t[1].append(AttDeclaration(True,t[4],t[6]))
            t[0] = t[1]
        else:
            t[1].append(AttDeclaration(False,t[3],t[5]))
            t[0] = t[1]
    else:
        if t.slice[1].type == 'PUB': t[0] = [AttDeclaration(True,t[2],t[4])]
        else: t[0] = [AttDeclaration(False,t[1],t[3])]

def p_lista_parametros(t):
    '''lista_parametros : lista_parametros COMA asignacion_simple
    | asignacion_simple'''
    if t.slice[1].type == 'lista_parametros':
        t[1].append(t[3])
        t[0] = t[1]
    else: t[0] = [t[1]]

def p_declaracion(t):
    '''declaracion : LET asignacion_simple IGUAL auxexp
    | LET MUT asignacion
    | LET asignacion'''
    if t.slice[2].type == 'asignacion_simple': t[0] = DeclarationSingle(t[2],t[4],t.lineno(1), t.lexpos(1))
    elif t.slice[2].type == 'MUT': t[0] = Declaration(True,t[3],t.lineno(1), t.lexpos(1))
    else: t[0] = Declaration(False,t[2],t.lineno(1), t.lexpos(1))

def p_asignacion(t):
    '''asignacion : ID IGUAL auxexp
    | ID lista_assign2 IGUAL auxexp
    | ID lista_arr IGUAL auxexp
    | ID lista_arr lista_assign2 IGUAL auxexp'''
    if t.slice[2].type == 'IGUAL': t[0] = Assignment([AttAssign(Access(t[1],t.lineno(1), t.lexpos(1)))],t[3],t.lineno(1), t.lexpos(1))
    else: 
        if t.slice[3].type == 'IGUAL': 
            if t.slice[2].type == 'lista_assign2': 
                single = []
                single.append(AttAssign(Access(t[1],t.lineno(1), t.lexpos(1))))
                for valor in t[2]:
                    single.append(valor)
                t[0] = Assignment(single,t[4],t.lineno(1), t.lexpos(1))
            else:
                t[0] = AssignmentAccessArray(AccessArray(Access(t[1],t.lineno(1), t.lexpos(1)),t[2],t.lineno(1), t.lexpos(1)),t[4],None,t.lineno(1), t.lexpos(1))
        else: t[0] = AssignmentAccessArray(AccessArray(Access(t[1],t.lineno(1), t.lexpos(1)),t[2],t.lineno(1), t.lexpos(1)),t[5],t[3],t.lineno(1), t.lexpos(1))

def p_lista_assign2(t):
    '''lista_assign2 : lista_assign2 PUNTO ID
    | PUNTO ID'''
    if t.slice[1].type == 'lista_assign2':
        t[1].append(AttAssign(t[3]))
        t[0] = t[1]
    else: t[0] = [AttAssign(t[2])]

def p_lista_assign(t):
    '''lista_assign : lista_assign PUNTO ID
    | ID'''
    if t.slice[1].type == 'lista_assign':
        t[1].append(AttAssign(t[3]))
        t[0] = t[1]
    else: t[0] = [AttAssign(Access(t[1],t.lineno(1), t.lexpos(1)))]

def p_lista_acc(t):
    '''lista_acc : lista_acc PUNTO ID
    | lista_acc PUNTO exp_native
    | auxacc'''
    if t.slice[1].type == 'lista_acc':
        t[1].append(AttAssign(t[3]))
        t[0] = t[1]
    else: t[0] = [AttAssign(Access(t[1],t.lineno(1), t.lexpos(1)))]

def p_auxacc(t):
    '''auxacc : exparr
    | ID'''
    t[0] = t[1]

def p_lista_arr(t):
    '''lista_arr : lista_arr LCOR auxexp RCOR
    | LCOR auxexp RCOR'''
    if t.slice[1].type == 'lista_arr': 
        t[1].append(t[3])
        t[0] = t[1]
    else: t[0] = [t[2]]

def p_lista_exp(t):
    '''lista_exp : lista_exp COMA auxexp
    | auxexp'''
    if t.slice[1].type == 'lista_exp':
        t[1].append(t[3])
        t[0] = t[1]
    else: t[0] = [t[1]]

def p_asignacion_simple(t):
    '''asignacion_simple : ID DPUNTOS tipo_var
    | MUT ID DPUNTOS tipo_var
    | ID DPUNTOS ANDSINGLE tipo_var
    | MUT ID DPUNTOS ANDSINGLE tipo_var
    | ID DPUNTOS ANDSINGLE MUT tipo_var
    | MUT ID DPUNTOS ANDSINGLE MUT tipo_var'''
    if t.slice[1].type == 'ID':
        if t.slice[3].type == 'tipo_var': t[0] = AssignmentSimple(False,t[1],t[3],False)
        elif t.slice[4].type == 'tipo_var': t[0] = AssignmentSimple(True,t[1],t[4],True)
        else : t[0] = AssignmentSimple(True,t[1],t[5],True)
    else:
        if t.slice[4].type == 'tipo_var': t[0] = AssignmentSimple(True,t[2],t[4],False)
        elif t.slice[5].type == 'tipo_var': t[0] = AssignmentSimple(True,t[2],t[5],True)
        else : t[0] = AssignmentSimple(True,t[2],t[6],True)

def p_lista_arr2(t):
    '''lista_arr2 : LCOR tipo_var PCOMA exp RCOR'''
    t[0] = ListArraySimple(t[2],t[4])

def p_auxexp(t):
    '''auxexp : expstruct
    | exp'''
    t[0] = t[1]

def p_exp(t):
    '''exp : LPAR exp RPAR
    | expmath
    | expop
    | exprel
    | exparr
    | newarray
    | expvec
    | exparam
    | exppow
    | expcast
    | lista_acc
    | llamada
    | sentencia
    | valores
    | exp PUNTO exp_native'''
    if t.slice[1].type == 'LPAR': t[0] = t[2]
    elif t.slice[1].type == 'expmath': t[0] = t[1]
    elif t.slice[1].type == 'expop': t[0] = t[1]
    elif t.slice[1].type == 'exprel': t[0] = t[1]
    elif t.slice[1].type == 'exparr': t[0] = t[1]
    elif t.slice[1].type == 'newarray': t[0] = t[1]
    elif t.slice[1].type == 'expvec': t[0] = t[1]
    elif t.slice[1].type == 'exparam': t[0] = t[1]
    elif t.slice[1].type == 'exppow': t[0] = t[1]
    elif t.slice[1].type == 'expcast': t[0] = t[1]
    elif t.slice[1].type == 'lista_acc': t[0] = AttAccess(t[1],t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'llamada': t[0] = t[1]
    elif t.slice[1].type == 'sentencia': t[0] = t[1]
    elif t.slice[1].type == 'valores': t[0] = t[1]
    elif t.slice[1].type == 'exp':
        if len(t.slice) > 2:
            if t.slice[2].type == 'PUNTO': t[0] = Native(t[1],t[3],t.lineno(1), t.lexpos(1))
            else: t[0] = t[1]
        else: t[0] = t[1]

def p_expmath(t):
    """expmath : exp MAS exp
    | exp MENOS exp
    | exp MULTIPLICACION exp
    | exp DIVISION exp
    | exp MODULO exp
    | MENOS exp %prec UMENOS"""
    if t.slice[1].type == 'MENOS': t[0] = Arithmetic(t[2], TYPE_OPERATION.RESTA, None, True,t.lineno(1), t.lexpos(1))
    else:
        if t.slice[2].type == 'MAS': t[0] = Arithmetic(t[1], TYPE_OPERATION.SUMA, t[3], False,t.lineno(1), t.lexpos(1))
        elif t.slice[2].type == 'MENOS': t[0] = Arithmetic(t[1], TYPE_OPERATION.RESTA, t[3], False,t.lineno(1), t.lexpos(1))
        elif t.slice[2].type == 'MULTIPLICACION': t[0] = Arithmetic(t[1], TYPE_OPERATION.MULTIPLICACION, t[3], False,t.lineno(1), t.lexpos(1))
        elif t.slice[2].type == 'MODULO': t[0] = Arithmetic(t[1], TYPE_OPERATION.MODULO, t[3], False,t.lineno(1), t.lexpos(1))
        else: t[0] = Arithmetic(t[1], TYPE_OPERATION.DIVISION, t[3], False,t.lineno(1), t.lexpos(1))

def p_exppow(t):
    '''exppow : I64 DPUNTOS DPUNTOS POW LPAR exp COMA exp RPAR
    | F64 DPUNTOS DPUNTOS POWF LPAR exp COMA exp RPAR'''
    if t.slice[1].type == 'I64': t[0] = ArithmeticPow(True,t[6],t[8],t.lineno(1), t.lexpos(1))
    else: t[0] = ArithmeticPow(False,t[6],t[8],t.lineno(1), t.lexpos(1))

def p_explog(t):
    '''expop : exp AND exp
    | exp OR exp
    | AD exp'''
    if t.slice[1].type == 'AD': t[0] = Logic(t[2], TYPE_LOGICAL.NOT, Handler(TYPE_DECLARATION.BOOLEAN,False,TYPE_DECLARATION.SIMPLE),t.lineno(1), t.lexpos(1))
    else:
        if t.slice[2].type == 'AND': t[0] = Logic(t[1], TYPE_LOGICAL.AND, t[3],t.lineno(1), t.lexpos(1))
        else: t[0] = Logic(t[1], TYPE_LOGICAL.OR, t[3],t.lineno(1), t.lexpos(1))

def p_expcast(t):
    'expcast : exp AS tipo_var'
    t[0] = Cast(t[1],t[3],t.lineno(1), t.lexpos(1))

def p_exprel(t):
    '''exprel : exp IGUALI exp
    | exp DIF exp
    | exp MAYOR exp
    | exp MENOR exp
    | exp MAYORI exp
    | exp MENORI exp'''
    if t.slice[2].type == 'IGUALI': t[0] = Relational(t[1],TYPE_RELATIONAL.IGUALI,t[3],t.lineno(1), t.lexpos(1))
    elif t.slice[2].type == 'DIF': t[0] = Relational(t[1],TYPE_RELATIONAL.DIF,t[3],t.lineno(1), t.lexpos(1))
    elif t.slice[2].type == 'MAYOR': t[0] = Relational(t[1],TYPE_RELATIONAL.MAYOR,t[3],t.lineno(1), t.lexpos(1))
    elif t.slice[2].type == 'MENOR': t[0] = Relational(t[1],TYPE_RELATIONAL.MENOR,t[3],t.lineno(1), t.lexpos(1))
    elif t.slice[2].type == 'MAYORI': t[0] = Relational(t[1],TYPE_RELATIONAL.MAYORI,t[3],t.lineno(1), t.lexpos(1))
    else: t[0] = Relational(t[1],TYPE_RELATIONAL.MENORI,t[3],t.lineno(1), t.lexpos(1))

def p_expstruct(t):
    '''expstruct : lista_classtype LLLAV lista_att RLLAV
    | lista_classtype LLLAV RLLAV
    | lista_classtype DPUNTOS DPUNTOS llamada'''
    if t.slice[3].type == 'lista_att': t[0] = CallStruct(AccessInstruction(t[1],t.lineno(1), t.lexpos(1)),t[3],t.lineno(1), t.lexpos(1))
    else:
        if t.slice[2].type == 'LLLAV': t[0] = CallStruct(AccessInstruction(t[1],t.lineno(1), t.lexpos(1)),[],t.lineno(1), t.lexpos(1))
        else: t[0] = ModAccess(t[1],t[4],t.lineno(1), t.lexpos(1))

def p_lista_struct(t):
    '''lista_att : lista_att COMA ID DPUNTOS auxexp
    | ID DPUNTOS auxexp'''
    if t.slice[1].type == 'lista_att':
        t[1].append(AttCall(t[3],t[5]))
        t[0] = t[1]
    else: t[0] = [AttCall(t[1],t[3])]

def p_exparam(t):
    '''exparam : MUT ID
    | MUT valores
    | ANDSINGLE MUT ID
    | ANDSINGLE MUT valores'''
    if t.slice[1].type == 'MUT': t[0] = ParamReference(True, Access(t[2],t.lineno(1), t.lexpos(1)), False)
    else: t[0] = ParamReference(True, Access(t[3],t.lineno(1), t.lexpos(1)), True)

def p_exparr(t):
    '''exparr : ID lista_arr'''
    t[0] = AccessArray(Access(t[1],t.lineno(1), t.lexpos(1)),t[2],t.lineno(1), t.lexpos(1))

def p_expvec(t):
    '''expvec : VEC AD newarray
    | VECTOR DPUNTOS DPUNTOS exp_natarr'''
    if t.slice[2].type == 'AD': t[0] = NewVector(t[3])
    else: t[0] = NewVector(Native(Handler(None,None,None),t[4],t.lineno(1), t.lexpos(1)))

def p_newarray(t):
    '''newarray : LCOR lista_exp RCOR
    | LCOR auxexp PCOMA exp RCOR'''
    if t.slice[2].type == 'lista_exp': t[0] = NewArray(t[2],t.lineno(1), t.lexpos(1))
    else: t[0] = NewDefaultArray(t[2],t[4],t.lineno(1), t.lexpos(1))

def p_valores(t):
    '''valores : ENTERO
    | DECIMAL
    | CADENA
    | BOOLEANO
    | CARACTER'''
    if t.slice[1].type == 'ENTERO': t[0] = Literal(t[1],0)
    elif t.slice[1].type == 'DECIMAL': t[0] = Literal(t[1],1)
    elif t.slice[1].type == 'CADENA': t[0] = Literal(t[1],3)
    elif t.slice[1].type == 'BOOLEANO': t[0] = Literal(t[1],4)
    else: t[0] = Literal(t[1],5)

def p_tipo_var(t):
    '''tipo_var : I64
    | F64
    | STRING
    | ANDSINGLE aSTR
    | BOOL
    | CHAR
    | USIZE
    | lista_arr2
    | LCOR tipo_var RCOR
    | lista_classtype
    | VECTOR MENOR tipo_var MAYOR
    | VECTOR MENOR lista_classtype MAYOR'''
    if t.slice[1].type == 'I64' : t[0] = Literal(None,0)
    elif t.slice[1].type == 'F64' : t[0] = Literal(None,1)
    elif t.slice[1].type == 'STRING' : t[0] = Literal(None,2)
    elif t.slice[1].type == 'ANDSINGLE' : t[0] = Literal(None,3)
    elif t.slice[1].type == 'BOOL' : t[0] = Literal(None,4)
    elif t.slice[1].type == 'CHAR' : t[0] = Literal(None,5)
    elif t.slice[1].type == 'USIZE' : t[0] = Literal(None,6)
    elif t.slice[1].type == 'lista_classtype' : t[0] = AccessInstruction(t[1],t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'lista_arr2' : t[0] = t[1]
    elif t.slice[1].type == 'LCOR' : t[0] = AccessTypeArray(t[2],t.lineno(1), t.lexpos(1))
    else: 
        if t.slice[3].type == 'tipo_var' :
            t[0] = AccessTypeVector(t[3])
        else:
            t[0] = AccessTypeVector(AccessInstruction(t[3],t.lineno(1), t.lexpos(1)))

def p_lista_classtype(t):
    '''lista_classtype : lista_classtype DPUNTOS DPUNTOS ID
    | ID'''
    if t.slice[1].type == 'lista_classtype':
        t[1].append(t[4])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_llamada(t):
    '''llamada : ID LPAR RPAR
    | ID LPAR lista_exp RPAR'''
    if t.slice[3].type == 'RPAR': t[0] = CallFunction(t[1],[],t.lineno(1), t.lexpos(1))
    else: t[0] = CallFunction(t[1],t[3],t.lineno(1), t.lexpos(1))

def p_exp_native(t):
    '''exp_native : TOSTRING LPAR RPAR
    | TOOWNED LPAR RPAR
    | CLONE LPAR RPAR
    | LEN LPAR RPAR
    | CAPACITY LPAR RPAR
    | REMOVE LPAR auxexp RPAR
    | CONTAINS LPAR ANDSINGLE auxexp RPAR
    | PUSH LPAR auxexp RPAR
    | INSERT LPAR lista_exp RPAR
    | CHARS LPAR RPAR
    | SQRT LPAR RPAR
    | ABS LPAR RPAR'''
    if t.slice[1].type == 'TOSTRING': t[0] = CallNative(None,0,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'TOOWNED': t[0] = CallNative(None,1,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'CLONE': t[0] = CallNative(None,2,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'LEN': t[0] = CallNative(None,3,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'CAPACITY': t[0] = CallNative(None,4,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'REMOVE': t[0] = CallNative(t[3],5,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'CONTAINS': t[0] = CallNative(t[4],6,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'PUSH': t[0] = CallNative(t[3],7,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'INSERT': t[0] = CallNative(t[3],8,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'CHARS': t[0] = CallNative(None,9,t.lineno(1), t.lexpos(1))
    elif t.slice[1].type == 'SQRT': t[0] = CallNative(None,10,t.lineno(1), t.lexpos(1))
    else: t[0] = CallNative(None,11,t.lineno(1), t.lexpos(1))

def p_exp_natarr(t):
    '''exp_natarr : NEW LPAR RPAR
    | WITHCAPACITY LPAR exp RPAR'''
    if t.slice[1].type == 'NEW': t[0] = CallNative(None,12,t.lineno(1), t.lexpos(1))
    else: t[0] = CallNative(t[3],13,t.lineno(1), t.lexpos(1))

def p_print(t):
    'print : PRINT AD LPAR lista_exp RPAR'
    t[0] = Print(t[4],t.lineno(1), t.lexpos(1))

def p_error(t):
    print(t)
    print("Syntax error at: ", t.value)

import Grammar.ply.yacc as yacc
parser = yacc.yacc()
globalEnv = None

def startParser(text,console):
    content = parser.parse(text)
    if text != '':
        global globalEnv
        globalGen = Generator()
        globalEnv = Enviroment(None,globalGen)
        for instruction in content:
            if isinstance(instruction, Modulo) or isinstance(instruction, Struct) or isinstance(instruction, Function):
                instruction.compile(globalEnv)
        founded = globalEnv.getFunction('main')
        if founded != None:
            returnedMain = CallFunction('main',[],0,0)
            returnedMain.isMain = True
            returnedMain.compile(globalEnv)
            print(globalGen.generateHeader())
            print(globalGen.code)
        else:
            print("Error: No fué encontrada una función main")
            #except:
            #    print("Error: La instrucción no se puede ejecutar de forma global")

def getGlobalEnv():
    global globalEnv
    return globalEnv