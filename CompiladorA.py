# Etapa 1 del análisis léxico: cargar archivos
with open('CicloFor.pas', 'r') as archivo:
    texto = archivo.read()

print("=== CÓDIGO ORIGINAL ===")
print(texto)
print("=======================\n")


# Lista de separadores y especiales
separadores = [' ', '\t', '\n']
especiales = "{}:;,+-*/=()[]<>.'\""

palabras_reservadas = {
    'program', 'begin', 'end', 'var', 'integer', 'real', 'boolean', 'char', 'string',
    'if', 'then', 'else', 'while', 'do', 'for', 'to', 'downto', 'repeat', 'until',
    'function', 'procedure', 'and', 'or', 'not', 'div', 'mod', 'true', 'false',
    'writeln', 'readln', 'write', 'read'
}

# Funciones matemáticas intrínsecas
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


print("=== CÓDIGO SIN COMENTARIOS ===")
print(texto_sin_comentarios)
print("================================\n")

# Etapa 3: separar en tokens 
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
        i += 1
        continue

    elif letra in especiales:
        if token:
            tokens.append(token.lower())
            token = ''
        tokens.append(letra.lower())
        i += 1
        continue

    else:
        # Para manejar números reales
        if letra.isdigit() or letra == '.':
            token += letra
            i += 1
            
            punto_contado = token.count('.')
            while i < n and (texto_sin_comentarios[i].isdigit() or (texto_sin_comentarios[i] == '.' and punto_contado == 0)):
                if texto_sin_comentarios[i] == '.':
                    punto_contado += 1
                token += texto_sin_comentarios[i]
                i += 1
            tokens.append(token.lower())
            token = ''
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
    delimitadores = {';', ',', '(', ')', '[', ']', '{', '}', '.', ':'}

    if t is None:
        return 'desconocido'
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
    elif t.isdigit():
        return 'integer'  
    elif t.count('.') == 1 and all(part.isdigit() for part in t.split('.')):
        return 'real'  
    else:
        return 'desconocido'
    
print("=== TOKENS GENERADOS ===")
for t in tokens:
    print(f"{t:<20} => {get_etiqueta(t)}")
print("=========================\n")
    

# === ANALIZADOR SINTÁCTICO ===

pos = 0
codigo_intermedio = []
temp_count = 0

def nuevo_temp():
    global temp_count
    temp = f"t{temp_count}"
    temp_count += 1
    return temp

def emit(instruccion):
    codigo_intermedio.append(instruccion)

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
    return actual() is not None and get_etiqueta(actual()) == 'integer'

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

    while actual() == 'var':
        coincidir('var')
        declaracion_variable()
        if not coincidir(';'):
            error("Se esperaba ';' después de declaración de variable")

    if not coincidir('begin'):
        error("Se esperaba 'begin' antes de las sentencias")

    while actual() not in ('end', None):
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

    print("\n=== TABLA DE SÍMBOLOS ===")
    imprimir_tabla()

    print("\n=== CÓDIGO INTERMEDIO GENERADO ===")
    for c in codigo_intermedio:
        print(c)
    print("===============================")

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

    emit(f'DECLARE {var_name} : {tipo}')  

    tipo_mapeado = {
        'real': 'float',
        'integer': 'int',
        'boolean': 'int',
        'char': 'char',
        'string': 'string'
    }[tipo]

    agregar_variable(var_name, tipo_mapeado)

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

    
    if actual() in funciones_intrinsecas:
        temp_resultado = funcion_intrinseca()
    else:
        temp_resultado, posfija = expresion()
        print(f"Expresión posfija: {' '.join(posfija)}")

    emit(f'{id_nombre} := {temp_resultado}')

def for_loop():
    if not coincidir('for'):
        error("Se esperaba 'for'")

    if not coincidir('('):
        error("Se esperaba '(' después de 'for'")

    var = actual()
    if not es_identificador():
        error("Se esperaba un identificador en el for")
    coincidir(var)

    if not coincidir(':='):
        error("Se esperaba ':=' en la asignación del for")

    
    inicio = actual()
    if inicio is None:
        error("Se esperaba expresión de inicio en el for")
    coincidir(inicio)

    if not coincidir(';'):
        error("Se esperaba ';' entre la asignación y el límite del for")

    fin = actual()
    if fin is None:
        error("Se esperaba expresión final en el for")
    coincidir(fin)

    if not coincidir(')'):
        error("Se esperaba ')' al final del encabezado del for")

    if not coincidir('{'):
        error("Se esperaba '{' para abrir el bloque del for")

    emit(f'FOR_INICIO {var} := {inicio} TO {fin}')

    while actual() != '}':
        if actual() is None:
            error("Se esperaba '}' para cerrar el bloque del for")
        sentencia()
        if actual() == ';':
            coincidir(';')

    if not coincidir('}'):
        error("Se esperaba '}' al final del bloque del for")

    emit(f'FOR_FIN {var}')

def escritura():
    instr = actual()
    coincidir(instr)
    if not coincidir('('):
        error(f"Se esperaba '(' en {instr}")

    textos_a_imprimir = []

    if actual() != ')':
        while True:
            if get_etiqueta(actual()) == 'cadena':
                textos_a_imprimir.append(actual())
                coincidir(actual())
            else:
                temp, _ = expresion()
                textos_a_imprimir.append(temp)
            if not coincidir(','):
                break

    if not coincidir(')'):
        error(f"Se esperaba ')' en {instr}")

    for item in textos_a_imprimir:
        emit(f'PRINT {item}')  

def lectura():
    instr = actual()
    coincidir(instr)
    if not coincidir('('):
        error(f"Se esperaba '(' en {instr}")
    variables_a_leer = []
    while True:
        if not es_identificador():
            error("Se esperaba identificador en read")
        variables_a_leer.append(actual())
        coincidir(actual())
        if not coincidir(','):
            break
    if not coincidir(')'):
        error(f"Se esperaba ')' en {instr}")

    for var in variables_a_leer:
        emit(f'READ {var}')  


def obtenerPrioridadOperador(op):
    if op in ['+', '-']:
        return 1
    elif op in ['*', '/']:
        return 2
    elif op == '^':
        return 3
    return 0


def convertirInfijaAPostfija(infija):
    pila = []
    salida = []
    for e in infija:
        if e == '(':
            pila.append(e)
        elif e == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            if pila:
                pila.pop()  # Quitar '('
        elif e in ['+', '-', '*', '/', '^']:
            while (pila and obtenerPrioridadOperador(e) <= obtenerPrioridadOperador(pila[-1])):
                salida.append(pila.pop())
            pila.append(e)
        else:
            salida.append(e)
    while pila:
        salida.append(pila.pop())
    return salida


def expresion():
    infija = []
    paren_count = 0

    while True:
        token = actual()
        if token is None:
            break
        if token == '(':
            paren_count += 1
            infija.append(token)
            coincidir(token)
        elif token == ')':
            if paren_count == 0:
                
                break
            paren_count -= 1
            infija.append(token)
            coincidir(token)
        elif token in (';', ',', '}') and paren_count == 0:
            
            break
        else:
            infija.append(token)
            coincidir(token)

    print(f"Expresión infija: {' '.join(infija)}")

    posfija = convertirInfijaAPostfija(infija)
    print(f"Expresión posfija: {' '.join(posfija)}")

    stack = []
    for t in posfija:
        if t.isidentifier() or t.isdigit() or get_etiqueta(t) == 'real':
            stack.append(t)
        else:
            if len(stack) < 2:
                error("Error: No hay suficientes operandos para la operación.")
            right = stack.pop()
            left = stack.pop()
            temp = nuevo_temp()
            emit(f'{temp} := {left} {t} {right}')
            stack.append(temp)

    if len(stack) != 1:
        error("Error: La expresión no se evaluó correctamente.")

    return stack.pop(), posfija

def funcion_intrinseca():
    func = actual()
    coincidir(func)
    if not coincidir('('):
        error("Se esperaba '(' en función intrínseca")
    
    arg = actual()
    if arg is None:
        error("Se esperaba argumento en función intrínseca")
    coincidir(arg)
    if not coincidir(')'):
        error("Se esperaba ')' en función intrínseca")
    temp = nuevo_temp()
    emit(f'{temp} := LLAMAR_FUNCION {func} {arg}')
    return temp

# Tabla de símbolos y registro
tabla_simbolos = {}

registros_float = [f"ft{i}" for i in range(32)]
registros_int = [f"x{i}" for i in range(32)]
registros_char = [f"a{i}" for i in range(8)]

indice_float = 0
indice_int = 0
indice_char = 0
indice_mem_float = 0
indice_mem_int = 0
indice_mem_char = 0
indice_mem_string = 0

def agregar_variable(nombre, tipo):
    global indice_float, indice_int, indice_char
    global indice_mem_float, indice_mem_int, indice_mem_char, indice_mem_string

    if nombre in tabla_simbolos:
        raise Exception(f"Error: Variable '{nombre}' redeclarada.")

    if tipo == 'float':
        if indice_float < len(registros_float):
            registro = registros_float[indice_float]
            indice_float += 1
        else:
            registro = f"mem_float_{indice_mem_float}"
            indice_mem_float += 1

    elif tipo == 'int':
        if indice_int < len(registros_int):
            registro = registros_int[indice_int]
            indice_int += 1
        else:
            registro = f"mem_int_{indice_mem_int}"
            indice_mem_int += 1

    elif tipo == 'char':
        if indice_char < len(registros_char):
            registro = registros_char[indice_char]
            indice_char += 1
        else:
            registro = f"mem_char_{indice_mem_char}"
            indice_mem_char += 1

    elif tipo == 'string':
        registro = f"mem_string_{indice_mem_string}"
        indice_mem_string += 1

    else:
        raise Exception(f"Error: Tipo desconocido '{tipo}'.")

    tabla_simbolos[nombre] = {
        'tipo': 'real' if tipo == 'float' else 'integer' if tipo == 'int' else tipo,
        'registro': registro
    }

def imprimir_tabla():
    print(f"{'Nombre':<10} {'Tipo':<10} {'Registro/Memoria':<20}")
    print("-" * 40)
    for nombre, info in tabla_simbolos.items():
        print(f"{nombre:<10} {info['tipo']:<10} {info['registro']:<20}")


# Ejecutar análisis sintáctico
analizar_programa()

# Generar codigo RiscV
print("\n=== CÓDIGO ENSAMBLADOR RISC-V ===\n")

registros_disponibles = [f't{i}' for i in range(32)]
registros = {}
contador_etiquetas = 0

def nuevo_etiqueta():
    global contador_etiquetas
    etiqueta = f"L{contador_etiquetas}"
    contador_etiquetas += 1
    return etiqueta

def obtener_registro(var):
    if var not in registros:
        if registros_disponibles:
            reg = registros_disponibles.pop(0)
            registros[var] = reg
        else:
            raise RuntimeError(f"No hay registros disponibles para '{var}'")
    return registros[var]

def traducir_instruccion(instr):
    partes = instr.split()
    if not partes:
        return []

    codigo = []

    if partes[0] == 'DECLARE':
        codigo.append(f"# Reservar espacio para variable {partes[1]}")
    elif partes[0] == 'READ':
        var = partes[1]
        reg_var = obtener_registro(var)
        codigo.append("li a7, 5")
        codigo.append("ecall")
        codigo.append(f"mv {reg_var}, a0")
    elif partes[1] == ':=' and len(partes) == 3:
        var = partes[0]
        valor = partes[2]
        reg_var = obtener_registro(var)
        try:
            val_num = int(valor)
            codigo.append(f"li {reg_var}, {val_num}")
        except ValueError:
            reg_val = obtener_registro(valor)
            codigo.append(f"mv {reg_var}, {reg_val}")
    elif partes[1] == ':=' and len(partes) == 5:
        temp = partes[0]
        var1 = partes[2]
        op = partes[3]
        var2 = partes[4]
        reg_temp = obtener_registro(temp)
        try:
            if op == '+':
                try:
                    val1 = int(var1)
                    reg_var2 = obtener_registro(var2)
                    codigo.append(f"addi {reg_temp}, {reg_var2}, {val1}")
                except ValueError:
                    reg_var1 = obtener_registro(var1)
                    try:
                        val2 = int(var2)
                        codigo.append(f"addi {reg_temp}, {reg_var1}, {val2}")
                    except ValueError:
                        reg_var2 = obtener_registro(var2)
                        codigo.append(f"add {reg_temp}, {reg_var1}, {reg_var2}")
            elif op == '-':
                reg_var1 = obtener_registro(var1)
                try:
                    val2 = int(var2)
                    codigo.append(f"addi {reg_temp}, {reg_var1}, {-val2}")
                except ValueError:
                    reg_var2 = obtener_registro(var2)
                    codigo.append(f"sub {reg_temp}, {reg_var1}, {reg_var2}")
            elif op == '*':
                reg_var1 = obtener_registro(var1)
                reg_var2 = obtener_registro(var2)
                codigo.append(f"mul {reg_temp}, {reg_var1}, {reg_var2}")
            elif op == '/':
                reg_var1 = obtener_registro(var1)
                reg_var2 = obtener_registro(var2)
                codigo.append(f"div {reg_temp}, {reg_var1}, {reg_var2}")
            else:
                codigo.append(f"# Operador {op} no soportado")
        except Exception:
            codigo.append(f"# Error en traducción de instrucción: {instr}")
    elif partes[0] == 'PRINT':
        arg = partes[1]
        if arg.startswith('"') and arg.endswith('"'):
            codigo.append(f"# print string literal {arg}")
        else:
            reg_print = obtener_registro(arg)
            codigo.append(f"mv a0, {reg_print}")
            codigo.append("li a7, 1")
            codigo.append("ecall")
    else:
        codigo.append(f"# Instrucción no reconocida: {instr}")

    return codigo


for instr in codigo_intermedio:
    instrucciones_asm = traducir_instruccion(instr)
    for linea in instrucciones_asm:
        print(linea)
