reserved = {
    'pub' : 'PUB',
    'mod' : 'MOD',
    'struct' : 'STRUCT',
    'mut' : 'MUT',
    'fn' : 'FN',
    'if' : 'IF',
    'else' : 'ELSE',
    'match' : 'MATCH',
    'loop' : 'LOOP',
    'while' : 'WHILE',
    'for' : 'FOR',
    'in' : 'IN',
    'println' : 'PRINT',
    'break' : 'BREAK',
    'return' : 'RETURN',
    'continue' : 'CONTINUE',
    'let' : 'LET',
    'i64' : 'I64',
    'f64' : 'F64',
    'bool' : 'BOOL',
    'char' : 'CHAR',
    'str' : 'aSTR',
    'String' : 'STRING',
    'usize' : 'USIZE',
    'as' : 'AS',
    'Vec' : 'VECTOR',
    'vec' : 'VEC',
    'to_string' : 'TOSTRING',
    'chars' : 'CHARS',
    'clone' : 'CLONE',
    'len' : 'LEN',
    'remove' : 'REMOVE',
    'contains' : 'CONTAINS',
    'new' : 'NEW',
    'with_capacity' : 'WITHCAPACITY',
    'to_owned' : 'TOOWNED',
    'capacity' : 'CAPACITY',
    'push' : 'PUSH',
    'insert' : 'INSERT',
    'abs' : 'ABS',
    'sqrt' : 'SQRT',
    'pow' : 'POW',
    'powf' : 'POWF'
}

tokens = [
    'ID','ENTERO','CADENA','DECIMAL','BOOLEANO','CARACTER',
    'MAS','MENOS','MULTIPLICACION','DIVISION','MODULO','MAYOR','MENOR','MAYORI','MENORI','IGUALI','DIF','OR','AND',
    'IGUAL','LCOR','RCOR','LPAR','RPAR','LLLAV','RLLAV','PUNTO','COMA','PCOMA','DPUNTOS','AD','ARROW','ARROW2','ORSINGLE','ANDSINGLE'
] + list(reserved.values())

t_MAS    = r'[\+]'
t_MENOS   = r'[\-]'
t_MULTIPLICACION   = r'[\*]'
t_DIVISION  = r'[\/]'
t_MODULO  = r'[\%]'
t_IGUAL  = r'[\=]'
t_LPAR  = r'[\(]'
t_RPAR  = r'[\)]'
t_LLLAV  = r'[\{]'
t_RLLAV  = r'[\}]'
t_LCOR  = r'[\[]'
t_RCOR  = r'[\]]'
t_COMA = r'[\,]'
t_PUNTO = r'[\.]'
t_PCOMA = r'[\;]'
t_DPUNTOS = r'[\:]'
t_AD = r'[\!]'
t_ARROW = r'[\-][\>]'
t_ARROW2 = r'[\=][\>]'
t_MAYOR = r'[\>]'
t_MENOR = r'[\<]'
t_MAYORI = r'[\>][\=]'
t_MENORI = r'[\<][\=]'
t_IGUALI = r'[\=][\=]'
t_DIF = r'[\!][\=]'
t_ORSINGLE = r'[\|]'
t_ANDSINGLE = r'[\&]'

def t_BOOLEANO(t):
    r'(true|false)'
    if t.value == 'true': t.value = True
    else: t.value = False
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    if t.value.lower() == 'main':
        t.value = t.value.lower()
    else:pass
    return t

def t_CADENA(t):
    r'[\"][^\"]*[\"]'
    try:
        t.value = t.value[1:-1]
    except ValueError:
        print("Error: No se ha podido reconocer la cadena", t.value)
        t.value = "Error"
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error: El decimal es demasiado grande", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Error: El entero es demasiado grande", t.value)
        t.value = 0
    return t

def t_CARACTER(t):
    r'[\'][^\'\n]*[\']'
    try:
        t.value = t.value[1:-1]
    except ValueError:
        print("Error: El valor no es un caracter", t.value)
        t.value = "Error"
    return t

def t_OR(t):
    r'[\|][\|]'
    return t

def t_AND(t):
    r'[\&][\&]'
    return t

def t_COMENTARIO(t):
    r'[\/][\/].*'
    t.lexer.lineno += 1

def t_COMENTARIO_G(t):
    r'\/\*[^\/]*\*\/'
    t.lexer.lineno += 1

t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Error: El lexema no es aceptado por el lenguaje", t.value[0])
    t.lexer.skip(1)

import Grammar.ply.lex as lex
lexer = lex.lex()