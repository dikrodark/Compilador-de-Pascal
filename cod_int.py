class GeneradorCodigoIntermedio:
    def __init__(self):
        self.codigo_intermedio = []
        self.etiqueta_contador = 0
        self.temporal_contador = 0
        self.etiquetas_loop = []

    def nueva_etiqueta(self):
        return f"L{self.etiqueta_contador := self.etiqueta_contador + 1}"

    def nuevo_temporal(self):
        return f"t{self.temporal_contador := self.temporal_contador + 1}"

    def agregar_codigo(self, instruccion):
        if instruccion:  # Evita líneas vacías 
            self.codigo_intermedio.append(instruccion)

    def generar_asignacion(self, destino, fuente):
        self.agregar_codigo(f"{destino} = {fuente}")

    def generar_operacion(self, destino, op1, operador, op2):
        self.agregar_codigo(f"{destino} = {op1} {operador} {op2}")

    def generar_if(self, condicion, etiqueta_true):
        self.agregar_codigo(f"if {condicion} goto {etiqueta_true}")

    def generar_goto(self, etiqueta):
        self.agregar_codigo(f"goto {etiqueta}")

    def generar_etiqueta(self, etiqueta):
        self.agregar_codigo(f"{etiqueta}:")

    def generar_for_loop(self, var, inicio, fin, cuerpo):
        temp_fin = self.nuevo_temporal()
        temp_cond = self.nuevo_temporal()
        etiqueta_inicio = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()

        self.etiquetas_loop.append((etiqueta_inicio, etiqueta_fin))

        self.generar_asignacion(var, inicio)
        self.generar_asignacion(temp_fin, fin)
        self.generar_etiqueta(etiqueta_inicio)

        self.generar_operacion(temp_cond, var, ">", temp_fin)
        self.generar_if(temp_cond, etiqueta_fin)

        cuerpo()

        self.generar_operacion(var, var, "+", "1")
        self.generar_goto(etiqueta_inicio)
        self.generar_etiqueta(etiqueta_fin)

        self.etiquetas_loop.pop()

    def generar_llamada_funcion(self, nombre, *args):
        args_str = ", ".join(args)
        self.agregar_codigo(f"call {nombre}, {args_str}")

    def imprimir_codigo_intermedio(self):
        print("\n=== CÓDIGO INTERMEDIO ===")
        for instruccion in self.codigo_intermedio:
            print(instruccion)
        print("=========================")
