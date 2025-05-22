class AnalizadorSemantico:
     
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.tabla_simbolos = {}  # variable: tipo
        
    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def avanzar(self):
        self.pos += 1

    def analizar(self):
        if not self._esperar('PROGRAM'): return
        self.avanzar()  # nombre del programa
        self.avanzar()  # ;
        self._analizar_declaraciones()
        if not self._esperar('BEGIN'): return
        self.avanzar()
        self._analizar_sentencias()
        if not self._esperar('END'): return
        self.avanzar()
        if not self._esperar('.'): return
        print("Análisis semántico exitoso ")

    def _esperar(self, esperado):
        actual = self.token_actual()
        if actual != esperado:
            print(f"Error semántico: se esperaba '{esperado}', se encontró '{actual}'")
            return False
        return True

    def _analizar_declaraciones(self):
        if self.token_actual() == 'VAR':
            self.avanzar()
            while self.token_actual() and self.token_actual().isidentifier():
                nombre = self.token_actual()
                self.avanzar()
                if self.token_actual() != ':':
                    print(f"Error: se esperaba ':' después de {nombre}")
                    return
                self.avanzar()
                tipo = self.token_actual()
                if tipo not in ['INTEGER', 'REAL', 'BOOLEAN', 'CHAR', 'STRING']:
                    print(f"Error: tipo desconocido '{tipo}'")
                    return
                if nombre in self.tabla_simbolos:
                    print(f"Error: variable '{nombre}' ya declarada")
                    return
                self.tabla_simbolos[nombre] = tipo
                self.avanzar()
                if self.token_actual() != ';':
                    print(f"Error: falta ';' después de declarar '{nombre}'")
                    return
                self.avanzar()

    def _analizar_sentencias(self):
        while self.token_actual() and self.token_actual() != 'END':
            var = self.token_actual()
            if var not in self.tabla_simbolos:
                print(f"Error: variable '{var}' no declarada")
                return
            self.avanzar()
            if self.token_actual() != ':=':
                print("Error: se esperaba ':=' en la asignación")
                return
            self.avanzar()
            valor = self.token_actual()
            tipo_var = self.tabla_simbolos[var]

            if tipo_var == 'INTEGER':
                if not valor.isdigit():
                    print(f"Error: se esperaba un entero para la variable '{var}', se encontró '{valor}'")
                    return
            elif tipo_var == 'BOOLEAN':
                if valor not in ['TRUE', 'FALSE']:
                    print(f"Error: se esperaba un booleano para '{var}'")
                    return

            self.avanzar()
            if self.token_actual() != ';':
                print("Error: se esperaba ';' después de la asignación")
                return
            self.avanzar()
