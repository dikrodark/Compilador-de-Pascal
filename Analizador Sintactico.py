class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def avanzar(self):
        self.pos += 1

    def coincidir(self, esperado):
        if self.token_actual() == esperado:
            self.avanzar()
            return True
        else:
            print(f"Error de sintaxis: se esperaba '{esperado}' pero se encontró '{self.token_actual()}'")
            return False

    def analizar_programa(self):
        if not self.coincidir('PROGRAM'):
            return False
        if not self.token_actual().isidentifier():
            print(f"Error: se esperaba un identificador, se encontró '{self.token_actual()}'")
            return False
        self.avanzar()
        if not self.coincidir(';'):
            return False
        self.analizar_declaraciones()
        if not self.coincidir('BEGIN'):
            return False
        self.analizar_sentencias()
        if not self.coincidir('END'):
            return False
        if not self.coincidir('.'):
            return False
        print("Análisis sintáctico exitoso")
        return True

    def analizar_declaraciones(self):
        if self.token_actual() == 'VAR':
            self.avanzar()
            while self.token_actual().isidentifier():
                self.avanzar()
                if not self.coincidir(':'):
                    return
                tipo = self.token_actual()
                if tipo not in ['INTEGER', 'REAL', 'BOOLEAN', 'CHAR', 'STRING']:
                    print(f"Error: tipo desconocido '{tipo}'")
                    return
                self.avanzar()
                if not self.coincidir(';'):
                    return

    def analizar_sentencias(self):
        while self.token_actual() and self.token_actual() != 'END':
            if not self.token_actual().isidentifier():
                print(f"Error: se esperaba una asignación, se encontró '{self.token_actual()}'")
                return
            self.avanzar()
            if not self.coincidir(':='):
                return
            if not (self.token_actual().isdigit() or self.token_actual().isidentifier()):
                print(f"Error: valor inválido '{self.token_actual()}'")
                return
            self.avanzar()
            if not self.coincidir(';'):
                return

# Uso
analizador = AnalizadorSintactico(tokens)
analizador.analizar_programa()
