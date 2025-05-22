# Etapa 1 del análisis léxico: cargar archivos
with open('Intrinseca.pas', 'r') as archivo:
    texto = archivo.read()

# Lista de separadores y especiales
separadores = [' ', '\t', '\n']
especiales = "{}:;,+-*/=()[]<>.'\""

palabras_reservadas = {
    'program', 'begin', 'end', 'var', 'integer', 'real', 'boolean', 'char', 'string',
    'if', 'then', 'else', 'while', 'do', 'for', 'to', 'downto', 'repeat', 'until',
    'function', 'procedure', 'and', 'or', 'not', 'div', 'mod', 'true', 'false',
    'writeln', 'readln', 'write', 'read'
}

# Lista adicional para funciones matemáticas intrínsecas
funciones_intrinsecas = {'sin', 'cos', 'tan'}

# Etapa 2 del análisis léxico: quitar comentarios tipo (* ... *)
def quitar_comentarios(texto):
    resultado = ''
    i = 0
    estado = 'Z'  # Z: fuera comentario, COM: dentro comentario
    while i < len(texto):
        if estado == 'Z':
            if texto[i] == '(' and i + 1 < len(texto) and texto[i+1] == '*':
                estado = 'COM'
                i += 2
            else:
                resultado += texto[i]
                i += 1
        else:
            if texto[i] == '*' and i + 1 < len(texto) and texto[i+1] == ')':
                estado = 'Z'
                i += 2
            else:
                i += 1
    return resultado

texto_sin_comentarios = quitar_comentarios(texto)

# Etapa 3: separar en tokens (ahora con cadenas)
tokens = []
token = ''
i = 0
n = len(texto_sin_comentarios)

while i < n:
    if i < n-1 and texto_sin_comentarios[i] == ':' and texto_sin_comentarios[i+1] == '=':
        if token:
            tokens.append(token.lower())
            token = ''
        tokens.append(':=')
        i += 2
        continue

    letra = texto_sin_comentarios[i]

    if letra == '"':
        if token:
            tokens.append(token.lower())
            token = ''
        cadena = '"'
        i += 1
        while i < n:
            cadena += texto_sin_comentarios[i]
            if texto_sin_comentarios[i] == '"':
                i += 1
                break
            i += 1
        tokens.append(cadena)
        continue

    if letra in separadores:
        if token:
            tokens.append(token.lower())
            token = ''
    elif letra in especiales:
        if token:
            tokens.append(token.lower())
            token = ''
        tokens.append(letra.lower())
    else:
        token += letra
    i += 1

if token:
    tokens.append(token.lower())

# Etapa 4: Etiquetado de tokens
def get_etiqueta(t):
    operadores_asignacion = {':='}
    operadores_aritmeticos = {'+', '-', '*', '/', 'div', 'mod'}
    operadores_comparacion = {'=', '<>', '<', '>', '<=', '>='}
    delimitadores = {';', ',', '(', ')', '[', ']', '{', '}', '.', ':', '"'}

    if t.startswith('"') and t.endswith('"'):
        return 'cadena'
    elif t in funciones_intrinsecas:
        return 'función intrínseca'
    elif t in operadores_asignacion:
        return 'operador de asignación'
    elif t in operadores_aritmeticos:
        return 'operador aritmético'
    elif t in operadores_comparacion:
        return 'operador de comparación'
    elif t in delimitadores:
        return 'delimitador'
    elif t in palabras_reservadas:
        return 'palabra reservada'
    elif t[0].isalpha() or t[0] == '_':
        return 'identificador'
    elif t[0].isdigit():
        return 'entero'
    else:
        return 'desconocido'
    



# === ANALIZADOR SINTÁCTICO ===

pos = 0

def actual():
    return tokens[pos] if pos < len(tokens) else None

def coincidir(esperado):
    global pos
    if actual() == esperado:
        pos += 1
        return True
    return False

def es_identificador():
    return actual() is not None and get_etiqueta(actual()) == 'identificador'

def es_entero():
    return actual() is not None and get_etiqueta(actual()) == 'entero'

def error(msg):
    raise SyntaxError(f"{msg}. Token encontrado: '{actual()}'")

def analizar_programa():
    if not coincidir('program'):
        error("Se esperaba 'program' al inicio")

    if not es_identificador():
        error("Se esperaba el nombre del programa")
    nombre_programa = actual()
    coincidir(nombre_programa)

    if not coincidir(';'):
        error("Se esperaba ';' después del nombre del programa")

    # Aceptar múltiples bloques var
    while actual() == 'var':
        coincidir('var')
        declaracion_variable()
        if not coincidir(';'):
            error("Se esperaba ';' después de declaración de variable")

    if not coincidir('begin'):
        error("Se esperaba 'begin' antes de las sentencias")

    while actual() not in ('end', None):
        # Ignorar tokens ';' sueltos antes de sentencia
        while actual() == ';':
            coincidir(';')

        if actual() in ('end', None):
            break

        sentencia()

        if actual() not in ('end', '.'):
            if not coincidir(';'):
                error("Se esperaba ';' después de la sentencia")

    if not coincidir('end'):
        error("Se esperaba 'end' al final del bloque")
    if not coincidir('.'):
        error("Se esperaba '.' al final del programa")

    print("Análisis sintáctico finalizado correctamente.")



def declaracion_variable():
    if not es_identificador():
        error("Se esperaba un identificador en declaración de variable")
    var_name = actual()
    coincidir(var_name)

    if not coincidir(':'):
        error("Se esperaba ':' en declaración de variable")

    tipo = actual()
    tipos_validos = {'integer', 'real', 'boolean', 'char', 'string'}
    if tipo not in tipos_validos:
        error("Se esperaba tipo válido en declaración de variable")
    coincidir(tipo)

    print(f"[gen] declarar variable '{var_name}' de tipo '{tipo}'")


def sentencia():
    if es_identificador():
        asignacion()
    elif actual() == 'for':
        for_loop()
    elif actual() in ('write', 'writeln'):
        escritura()
    elif actual() in ('read', 'readln'):
        lectura()
    else:
        error("Sentencia no válida")

def asignacion():
    id_nombre = actual()
    coincidir(id_nombre)
    if not coincidir(':='):
        error("Se esperaba ':=' en asignación")
    expresion()
    print(f"[gen] Guardar resultado de expresión en '{id_nombre}'")

def for_loop():
    coincidir('for')
    var = actual()
    if not es_identificador():
        error("Se esperaba un identificador en bucle for")
    coincidir(var)
    if not coincidir(':='):
        error("Se esperaba ':=' en bucle for")
    expresion()
    if not (coincidir('to') or coincidir('downto')):
        error("Se esperaba 'to' o 'downto' en bucle for")
    expresion()
    if not coincidir('do'):
        error("Se esperaba 'do' en bucle for")
    sentencia()
    print(f"[gen] bucle for sobre '{var}'")

def escritura():
    instr = actual()
    coincidir(instr)
    if not coincidir('('):
        error(f"Se esperaba '(' en {instr}")

    if actual() != ')':
        while True:
            if get_etiqueta(actual()) == 'cadena':
                print(f"[gen] cadena literal: {actual()}")
                coincidir(actual())
            else:
                expresion()
            if not coincidir(','):
                break

    if not coincidir(')'):
        error(f"Se esperaba ')' en {instr}")
    print(f"[gen] imprimir resultado(s) en consola ({instr})")


def lectura():
    instr = actual()
    coincidir(instr)
    if not coincidir('('):
        error(f"Se esperaba '(' en {instr}")
    while True:
        if not es_identificador():
            error("Se esperaba identificador en read")
        print(f"[gen] leer valor para '{actual()}'")
        coincidir(actual())
        if not coincidir(','):
            break
    if not coincidir(')'):
        error(f"Se esperaba ')' en {instr}")

def expresion():
    termino()
    while actual() in ('+', '-'):
        op = actual()
        coincidir(op)
        termino()
        print(f"[gen] aplicar operador {op}")

def termino():
    factor()
    while actual() in ('*', '/', 'div', 'mod'):
        op = actual()
        coincidir(op)
        factor()
        print(f"[gen] aplicar operador {op}")

def factor():
    if es_entero():
        print(f"[gen] cargar entero {actual()} en fa0")
        coincidir(actual())
    elif es_identificador():
        print(f"[gen] cargar variable {actual()} en fa0")
        coincidir(actual())
    elif actual() in funciones_intrinsecas:
        funcion_intrinseca()
    elif coincidir('('):
        expresion()
        if not coincidir(')'):
            error("Se esperaba ')' en expresión")
    elif get_etiqueta(actual()) == 'cadena':
        print(f"[gen] cadena literal: {actual()}")
        coincidir(actual())
    else:
        error("Factor inválido")

def funcion_intrinseca():
    func = actual()
    coincidir(func)
    if not coincidir('('):
        error("Se esperaba '(' en función intrínseca")
    expresion()
    if not coincidir(')'):
        error("Se esperaba ')' en función intrínseca")
    print(f"[gen] llamar a función '{func}' con argumento en fa0")

# Ejecutar análisis sintáctico
analizar_programa()
