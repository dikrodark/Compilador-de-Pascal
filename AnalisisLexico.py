# Etapa 1 del analisis lexico: cargar archivos
with open('Intrinseca.pas', 'r') as archivo:
    texto = archivo.read()

# Lista de separadores y especiales
separadores = [' ', '\t', '\n']
especiales = "{};:,+-*/=()[]<>.'"

palabras_reservadas = {
    'PROGRAM', 'BEGIN', 'END', 'VAR', 'INTEGER', 'REAL', 'BOOLEAN', 'CHAR', 'STRING',
    'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FOR', 'TO', 'DOWNTO', 'REPEAT', 'UNTIL',
    'FUNCTION', 'PROCEDURE', 'AND', 'OR', 'NOT', 'DIV', 'MOD', 'TRUE', 'FALSE',
    'WRITELN', 'READLN'
}

# Lista adicional para funciones matemáticas intrínsecas
funciones_intrinsecas = {'SIN', 'COS', 'TAN'}

# Etapa 2 del analisis lexico: quitar comentarios tipo (* ... *)
def quitar_comentarios(texto):
    resultado = ''
    i = 0
    estado = 'Z'  # Z: fuera comentario, COM: dentro comentario
    while i < len(texto):
        if estado == 'Z':
            # Detectar inicio de comentario (* 
            if texto[i] == '(' and i + 1 < len(texto) and texto[i+1] == '*':
                estado = 'COM'
                i += 2  # Saltar '(*'
            else:
                resultado += texto[i]
                i += 1
        else:  # estado == 'COM'
            # Detectar fin de comentario *)
            if texto[i] == '*' and i + 1 < len(texto) and texto[i+1] == ')':
                estado = 'Z'
                i += 2  # Saltar '*)'
            else:
                i += 1
    return resultado

texto_sin_comentarios = quitar_comentarios(texto)

print("Código sin comentarios:\n")
print(texto_sin_comentarios)
print("\n_________________________\n")

# Etapa 3 del analisis lexico: separar en tokens
tokens = []
token = ''

for letra in texto_sin_comentarios:
    if letra in separadores:
        if token:
            tokens.append(token)
            token = ''
    elif letra in especiales:
        if token:
            tokens.append(token)
            token = ''
        tokens.append(letra)
    else:
        token += letra

if token:
    tokens.append(token)

# Etapa 4 del analisis lexico: etiquetar tokens
def get_etiqueta(t):
    operadores = {
        "+", "-", "*", "/", "=", "<>", "<", ">", "<=", ">=", ":=", ":", ";", ",", ".", "(", ")", "[", "]", "'"
    }
    minusculas = 'abcdefghijklmnopqrstuvwxyz_'
    mayusculas = minusculas.upper()

    if t.upper() in funciones_intrinsecas:
        return 'función intrínseca'
    elif t in operadores:
        return 'símbolo'
    elif t.upper() in palabras_reservadas:
        return 'palabra reservada'
    elif t[0] in minusculas or t[0] in mayusculas:
        return 'identificador'
    elif t[0].isdigit():
        return 'entero'
    else:
        return 'desconocido'

# Mostrar tokens con sus etiquetas
for t in tokens:
    print(f"{t} → {get_etiqueta(t)}")
