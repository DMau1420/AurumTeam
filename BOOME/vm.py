class BoomeVM:

    def __init__(self):

        """

        Registro: Es como la memoria RAM del robot, pero solo hay 4 espacios.

        Registros del boome - self.R es un diccionario que guarda 4 registros:

            "0" (r0) empieza en 0

            "1" (r1) empieza en 1

            "2" (r2) empieza en 2

            "3" (r3) empieza en 3
        """

        self.R = {"0":0,"1":1,"2":2,"3":3}

        # Posición inicial del robot
        self.Columna = 0
        self.Fila = 0

        # Crear el mapa 5 X 10
        self.Mapa = [
            ["0", "0", "1", "0", "2", "0", "0", "0", "0", "0"],
            ["1", "2", "0", "0", "1", "0", "0", "2", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
            ["0", "1", "0", "2", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "2", "0", "1", "0", "0"]
        ]


        self.obstaculo = "1"
        self.bomba = "2"

        # La ultima construccion que se ejecuto
        self.ultimaInstruccion = ""
        self.Vivo = True
        self.InstruccionActual = ""

    def __str__(self):

        Ret = f"Registros\nR0: {self.R['0']}\n"
        Ret += f"R1: {self.R['1']} \n"
        Ret += f"R2: {self.R['2']} \n"
        Ret += f"R3: {self.R['3']} \n"

        # [:] Sirve específicamente para crear una copia superficial
        Mapa = [fila[:] for fila in self.Mapa]

        Mapa[self.Fila][self.Columna] = "B"

        for fila in Mapa:
            Ret += f'{fila}\n'

        Ret += f'Ultima instruccion : {self.ultimaInstruccion}\n'
        Ret += f'Instruccion actual : {self.InstruccionActual}\n'
        Ret += f'Vivo : {self.Vivo}\n'
        Ret += f'----------------------------------------------\n'
        return Ret


    def movIzquierda(self):

        self.Columna = self.Columna -1
        if self.Columna  < 0:
            self.Vivo = False
            self.Columna = self.Columna + 1


    def movDerecha(self):

        self.Columna = self.Columna + 1
        if self.Columna  >= len(self.Mapa[self.Fila]):
            self.Vivo = False
            self.Columna = self.Columna - 1

    def movArriba(self):

        self.Fila = self.Fila -1
        if self.Fila  < 0:
            self.Vivo = False
            self.Fila = self.Fila + 1

    def movAbajo(self):
        self.Fila = self.Fila + 1
        if self.Fila  >= len(self.Mapa):
            self.Vivo = False
            self.Fila = self.Fila - 1

    def leer_sensor(self,direccion):

        # Obtener la posición ACTUAL del robot
        fila,col = self.Fila, self.Columna

        # izquierda
        if direccion == "ab":
            col -= 1

        # derecha
        elif direccion == "je":
            col += 1

        elif direccion == "dw":
            fila -= 1

        elif direccion == "up":
            fila += 1

        # VERIFICAR que la nueva posición está DENTRO del mapa

        if (fila >= 0 and fila < len(self.Mapa)) and (col >= 0 and col < len(self.Mapa[0])):

            valor = int(self.Mapa[fila][col])

            if valor == 1:
                print("PELIGRO OBSTACULO DETECTADO ")

            elif valor == 2:
                print("BOMBA DETECTADA")



        return 0


    def obtener_valor(self,operando):

        if operando in self.R:
            return self.R[operando]

        elif operando.startswith("0x"):
            return int(operando,16)

        else:
            return int(operando)

    def fetchDecodeExecute(self, instruccion_parseada):

        """
        Ejecutar la instrucción y devolver:
        - 1: si debe continuar con la siguiente línea
        - N: si debe saltar a la línea N
        """

        if not self.Vivo:
            return 1

        self.ultimaInstruccion = self.InstruccionActual
        self.InstruccionActual = str(instruccion_parseada)

        tipo = instruccion_parseada["tipo"]

        # CASO 1 MOVIMIENTO
        if tipo == "movimiento":
            accion = instruccion_parseada["valor"]

            if accion == "movi":
                self.movIzquierda()
            elif accion == "movd":
                self.movDerecha()
            elif accion == "mova":
                self.movArriba()
            elif accion == "movb":
                self.movAbajo()

            return 1

        # CASO 2 SENSOR
        elif tipo == "sensor":
            direccion = instruccion_parseada["direccion"]
            self.leer_sensor(direccion)
            return 1

        # CASO 3 ASIGNACION SIMPLE
        elif tipo == "asignacion_simple":
            destino = instruccion_parseada["destino"]
            fuente = instruccion_parseada["fuente"]

            if fuente in self.R:
                self.R[destino] = self.R[fuente]
            else:
                self.R[destino] = self.obtener_valor(fuente)

            return 1

        # CASO 4 ASIGNACION SENSOR
        elif tipo == "asignacion_sensor":
            destino = instruccion_parseada["destino"]
            direccion = instruccion_parseada["direccion"]
            self.R[destino] = self.leer_sensor(direccion)
            return 1  # ¡Faltaba este return!

        # CASO 5 OPERACION ARITMETICA
        elif tipo == "operacion":
            destino = instruccion_parseada["destino"]
            # CORRECCIÓN: Necesitas obtener los VALORES, no los strings
            op1 = self.obtener_valor(instruccion_parseada["operando1"])
            op2 = self.obtener_valor(instruccion_parseada["operando2"])
            operador = instruccion_parseada["operador"]

            if operador == "+":
                self.R[destino] = op1 + op2
            else:  # "-"
                self.R[destino] = op1 - op2

            return 1

        # CASO 6 SALTO
        elif tipo == "salto":
            condicion = instruccion_parseada["condicion"]
            op1 = self.obtener_valor(instruccion_parseada["operando1"])
            op2 = self.obtener_valor(instruccion_parseada["operando2"])
            destino = self.obtener_valor(instruccion_parseada["destino"])

            # Depuración de salto
            print(f"Evaluando salto: {condicion} {op1} {op2} -> línea {destino}")

            # Evaluar condición
            if condicion == "salta_igual" and op1 == op2:
                print(f"¡CONDICIÓN VERDADERA! Saltando a línea {destino}")
                return destino

            elif condicion == "salta_dif" and op1 != op2:
                print(f"¡CONDICIÓN VERDADERA! Saltando a línea {destino}")
                return destino

            else:
                print("Condición FALSA, siguiente línea")
                return 1

        return 1




