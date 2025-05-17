from AnalizadorSintatico import AnalizadorLexico, Token

class AnalizadorSintatico:
    def __init__(self, lexer):
        self.AalizadorSintatico = lexer
        self.token_actual = self.AalizadorSintatico.obtener_siguiente_token()
    
    def leer(self, tipo_esperado, mensaje_error):
        if self.token_actual.tipo == tipo_esperado:
            self.token_actual = self.AalizadorSintatico.obtener_siguiente_token()
        else:
            raise Exception(f"Error sintáctico en línea {self.token_actual.linea}: {mensaje_error}")

    def analizar(self):
        self.programa()
        print("Análisis sintáctico completado sin errores")

    def programa(self):
        """PROGRAMA ID ; BLOQUE ."""
        self.leer('PROGRAMA', "Se esperaba 'PROGRAM' al inicio")
        self.leer('IDENTIFICADOR', "Se esperaba un nombre de programa")
        self.leer('PUNTO_Y_COMA', "Falta ';' después del nombre del programa")
        self.bloque()
        self.leer('PUNTO', "Falta '.' al final del programa")

    def bloque(self):
        """BLOQUE -> INICIO LISTA_SENTENCIAS FIN"""
        self.leer('INICIO', "Se esperaba 'BEGIN'")
        self.lista_sentencias()
        self.leer('FIN', "Se esperaba 'END'")

    def lista_sentencias(self):
        while self.token_actual.tipo not in ['FIN', 'FIN_DE_ARCHIVO']:
            self.sentencia()
            if self.token_actual.tipo == 'PUNTO_Y_COMA':
                self.leer('PUNTO_Y_COMA', "Falta ';' después de la sentencia")
            else:
                break

    def sentencia(self):
        """SENTENCIA -> ASIGNACION | ESCRITURA | SI ..."""
        if self.token_actual.tipo == 'IDENTIFICADOR':
            self.asignacion()
        elif self.token_actual.tipo == 'ESCRIBIR_LINEA':
            self.escritura()
        elif self.token_actual.tipo == 'SI':
            self.si()
        else:
            raise Exception(f"Sentencia inválida en línea {self.token_actual.linea}")

    def asignacion(self):
        self.leer('IDENTIFICADOR', "Se esperaba un identificador")
        self.leer('ASIGNACION', "Falta ':=' en la asignación")
        self.expresion()

    def escritura(self):
        self.leer('ESCRIBIR_LINEA', "Se esperaba 'WRITELN'")
        self.leer('PARENTESIS_IZQ', "Falta '(' después de WRITELN")
        self.lista_expresiones()
        self.leer('PARENTESIS_DER', "Falta ')' después de la lista de expresiones")

    def si(self):
        self.leer('SI', "Se esperaba 'IF'")
        self.expresion()
        self.leer('ENTONCES', "Se esperaba 'THEN'")
        self.sentencia()
        if self.token_actual.tipo == 'SINO':
            self.leer('SINO', "Se esperaba 'ELSE'")
            self.sentencia()

    def expresion(self):
        self.termino()
        while self.token_actual.tipo in ['SUMA', 'RESTA', 'O']:
            self.leer(self.token_actual.tipo, f"Se esperaba un operador")
            self.termino()

    def termino(self):
        self.factor()
        while self.token_actual.tipo in ['MULTIPLICACION', 'DIVISION', 'Y']:
            self.leer(self.token_actual.tipo, f"Se esperaba un operador")
            self.factor()

    def factor(self):
        if self.token_actual.tipo == 'IDENTIFICADOR':
            self.leer('IDENTIFICADOR', "Se esperaba un identificador")
        elif self.token_actual.tipo in ['ENTERO', 'REAL']:
            self.leer(self.token_actual.tipo, "Se esperaba un número")
        elif self.token_actual.tipo == 'PARENTESIS_IZQ':
            self.leer('PARENTESIS_IZQ', "Falta '('")
            self.expresion()
            self.leer('PARENTESIS_DER', "Falta ')'")
        elif self.token_actual.tipo == 'RESTA':
            self.leer('RESTA', "Falta '-'")
            self.factor()
        elif self.token_actual.tipo == 'NO':
            self.leer('NO', "Falta 'NOT'")
            self.factor()
        else:
            raise Exception(f"Factor inválido en línea {self.token_actual.linea}")

    def lista_expresiones(self):
        if self.token_actual.tipo not in ['PARENTESIS_DER', 'PUNTO_Y_COMA']:
            self.expresion()
            while self.token_actual.tipo == 'COMA':
                self.leer('COMA', "Falta ','")
                self.expresion()
