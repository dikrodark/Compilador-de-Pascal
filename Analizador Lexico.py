class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo    
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"Token({self.tipo}, {self.valor}, línea={self.linea}, col={self.columna})"


class AnalizadorLexico:
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.caracter_actual = self.codigo_fuente[self.posicion] if self.codigo_fuente else None

    def avanzar(self):
        if self.caracter_actual == '\n':
            self.linea += 1
            self.columna = 0
        self.posicion += 1
        if self.posicion < len(self.codigo_fuente):
            self.caracter_actual = self.codigo_fuente[self.posicion]
            self.columna += 1
        else:
            self.caracter_actual = None

    def ignorar_espacios_y_comentarios(self):
        while self.caracter_actual is not None and (self.caracter_actual.isspace() or self.caracter_actual == '{'):
            if self.caracter_actual == '{':
                while self.caracter_actual != '}' and self.caracter_actual is not None:
                    self.avanzar()
                if self.caracter_actual == '}':
                    self.avanzar()
            else:
                self.avanzar()

    def ver_siguiente_caracter(self):
        peek_pos = self.posicion + 1
        return self.codigo_fuente[peek_pos] if peek_pos < len(self.codigo_fuente) else None

    def obtener_siguiente_token(self):
        self.ignorar_espacios_y_comentarios()

        if self.caracter_actual is None:
            return Token('FIN_DE_ARCHIVO', None, self.linea, self.columna)

        if self.caracter_actual.isalpha() or self.caracter_actual == '_':
            return self.obtener_id_o_pal_res()

        elif self.caracter_actual.isdigit():
            return self.obtener_numero()

        elif self.caracter_actual == "'":
            return self.obtener_cadena()

        elif self.caracter_actual in ':=+-*/<>=()[];.,':
            return self.obtener_simbolo_u_operador()

        raise Exception(f"Carácter inválido '{self.caracter_actual}' en línea {self.linea}, col {self.columna}")

    def obtener_id_o_pal_res(self):
        texto = ''
        col_inicio = self.columna

        while self.caracter_actual is not None and (self.caracter_actual.isalnum() or self.caracter_actual == '_'):
            texto += self.caracter_actual
            self.avanzar()

        palabras_reservadas = {
            'PROGRAM': 'PROGRAMA',
            'BEGIN': 'INICIO',
            'END': 'FIN',
            'VAR': 'VARIABLE',
            'INTEGER': 'ENTERO',
            'REAL': 'REAL',
            'BOOLEAN': 'BOOLEANO',
            'CHAR': 'CARACTER',
            'STRING': 'CADENA',
            'IF': 'SI',
            'THEN': 'ENTONCES',
            'ELSE': 'SINO',
            'WHILE': 'MIENTRAS',
            'DO': 'HACER',
            'FOR': 'PARA',
            'TO': 'HASTA',
            'DOWNTO': 'DESDE',
            'REPEAT': 'REPETIR',
            'UNTIL': 'HASTA_QUE',
            'FUNCTION': 'FUNCION',
            'PROCEDURE': 'PROCEDIMIENTO',
            'AND': 'Y',
            'OR': 'O',
            'NOT': 'NO',
            'DIV': 'DIVISION_ENTERA',
            'MOD': 'MODULO',
            'TRUE': 'VERDADERO',
            'FALSE': 'FALSO',
            'WRITELN': 'ESCRIBIR_LINEA',
            'READLN': 'LEER_LINEA'
        }

        tipo = palabras_reservadas.get(texto.upper(), 'IDENTIFICADOR')
        return Token(tipo, texto, self.linea, col_inicio)

    def obtener_numero(self):
        numero = ''
        col_inicio = self.columna
        es_real = False

        while self.caracter_actual is not None and (self.caracter_actual.isdigit() or self.caracter_actual == '.'):
            if self.caracter_actual == '.':
                if es_real:
                    raise Exception(f"Número mal formado en línea {self.linea}")
                es_real = True
            numero += self.caracter_actual
            self.avanzar()

        if es_real:
            return Token('REAL', float(numero), self.linea, col_inicio)
        else:
            return Token('ENTERO', int(numero), self.linea, col_inicio)

    def obtener_cadena(self):
        cadena = ''
        col_inicio = self.columna
        self.avanzar()

        while self.caracter_actual is not None and self.caracter_actual != "'":
            cadena += self.caracter_actual
            self.avanzar()

        if self.caracter_actual != "'":
            raise Exception(f"Cadena no cerrada en línea {self.linea}")

        self.avanzar()
        return Token('CADENA', cadena, self.linea, col_inicio)

    def obtener_simbolo_u_operador(self):
        simbolo = self.caracter_actual
        col_inicio = self.columna

        if simbolo == ':' and self.ver_siguiente_caracter() == '=':
            self.avanzar()
            self.avanzar()
            return Token('ASIGNACION', ':=', self.linea, col_inicio)
        elif simbolo == '<' and self.ver_siguiente_caracter() == '>':
            self.avanzar()
            self.avanzar()
            return Token('DIFERENTE', '<>', self.linea, col_inicio)
        elif simbolo == '<' and self.ver_siguiente_caracter() == '=':
            self.avanzar()
            self.avanzar()
            return Token('MENOR_IGUAL', '<=', self.linea, col_inicio)
        elif simbolo == '>' and self.ver_siguiente_caracter() == '=':
            self.avanzar()
            self.avanzar()
            return Token('MAYOR_IGUAL', '>=', self.linea, col_inicio)

        tipos_simbolos = {
            '+': 'SUMA',
            '-': 'RESTA',
            '*': 'MULTIPLICACION',
            '/': 'DIVISION',
            '=': 'IGUAL',
            '<': 'MENOR',
            '>': 'MAYOR',
            '(': 'PARENTESIS_IZQ',
            ')': 'PARENTESIS_DER',
            '[': 'CORCHETE_IZQ',
            ']': 'CORCHETE_DER',
            ';': 'PUNTO_Y_COMA',
            ',': 'COMA',
            '.': 'PUNTO',
            ':': 'DOS_PUNTOS'
        }

        if simbolo in tipos_simbolos:
            self.avanzar()
            return Token(tipos_simbolos[simbolo], simbolo, self.linea, col_inicio)
        else:
            raise Exception(f"Símbolo desconocido '{simbolo}' en línea {self.linea}, col {self.columna}")


# 🔽 Leer código desde archivo
nombre_archivo = 'Pendiente.pas'
with open(nombre_archivo, 'r') as archivo:
    codigo = archivo.read()

print("Contenido del archivo:")
print(codigo)
print("___________________________\n")

# 🔽 Ejecutar analizador
analizador = AnalizadorLexico(codigo)
tokens = []

while True:
    token = analizador.obtener_siguiente_token()
    tokens.append(token)
    if token.tipo == 'FIN_DE_ARCHIVO':
        break

# 🔽 Imprimir tokens
print("Tokens encontrados:")
for t in tokens:
    print(t)
