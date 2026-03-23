import json
import random

def crear_tablero_limpio():
    tablero = {}
    letras = ['A', 'B', 'C', 'D', 'E']
    for fila in range(1, 11):
        for col in letras:
            tablero[f"{col}{fila}"] = 0
    return tablero

def guardar_tablero(tablero):
    with open('tablero.json', 'w', encoding='utf-8') as archivo:
        json.dump(tablero, archivo, indent=2)

def plantar_bomba(tablero):
    casillas_vacias = [casilla for casilla, valor in tablero.items() if valor == 0]
    bomba = random.choice(casillas_vacias)
    tablero[bomba] = 1
    print(f"Bomba plantada en: {bomba}")

def detector_bomba(valor_real):

    # Si hay bomba: 90% de detectarla (9/10)
    # Si no hay bomba: 20% de falso positivo (2/10)

    vacias_10 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    bombas_10 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    
    if valor_real == 1:  # Hay bomba
        return random.choice(bombas_10)
    else:  # No hay bomba
        return random.choice(vacias_10)

def probabilidad_bayesiana(prob_anterior, mediciones):
    """
    Calcula la probabilidad actualizada usando el teorema de Bayes
    prob_anterior: P(Bomba) antes de las nuevas mediciones
    mediciones: lista de resultados del detector (0 o 1)
    """
    # Tasas del detector
    # P(medicion=1 | Bomba) = 0.9
    # P(medicion=1 | NoBomba) = 0.2
    p_detectar_bomba = 0.9  # Sensibilidad
    p_falso_positivo = 0.2   # Tasa de falsos positivos
    
    prob_actual = prob_anterior
    
    for medicion in mediciones:
        if medicion == 1:  # El detector dijo que hay bomba
            # P(Evidencia | Bomba) = p_detectar_bomba
            # P(Evidencia | NoBomba) = p_falso_positivo
            prob_actual = (p_detectar_bomba * prob_actual) / (
                p_detectar_bomba * prob_actual + p_falso_positivo * (1 - prob_actual)
            )
        else:  # El detector dijo que no hay bomba
            # P(Evidencia | Bomba) = 1 - p_detectar_bomba
            # P(Evidencia | NoBomba) = 1 - p_falso_positivo
            prob_actual = ((1 - p_detectar_bomba) * prob_actual) / (
                (1 - p_detectar_bomba) * prob_actual + (1 - p_falso_positivo) * (1 - prob_actual)
            )
    
    return prob_actual

def verificar_casilla_bayesiana(tablero, casilla, desactivaciones, prob_inicial=1/50):
    """
    Verifica una casilla usando inferencia bayesiana con 3 mediciones
    SOLO si el detector marca positivo al menos una vez
    """
    valor_real = tablero[casilla]
    
    # Tomar 3 mediciones independientes
    mediciones = []
    for _ in range(3):
        medicion = detector_bomba(valor_real)
        mediciones.append(medicion)
    
    # Verificar si alguna medición fue positiva
    hubo_positivo = any(m == 1 for m in mediciones)
    
    print(f"Mediciones en {casilla}: {mediciones}")
    
    # SOLO calcular probabilidad bayesiana si hubo al menos una medición positiva
    if hubo_positivo:
        probabilidad = probabilidad_bayesiana(prob_inicial, mediciones)
        print(f"Probabilidad bayesiana: {probabilidad:.1%}")
        
        # Si hay bomba real y probabilidad > 50%, desactivar si hay desactivaciones disponibles
        if valor_real == 1 and probabilidad >= 0.5:
            if desactivaciones > 0:
                print(f"Bomba detectada en {casilla} con {probabilidad:.1%} probabilidad bayesiana")
                tablero[casilla] = 0  # Desactivar bomba
                print(f"Bomba desactivada. Quedan {desactivaciones - 1} desactivaciones")
                return True, probabilidad, desactivaciones - 1
            else:
                print(f"Bomba detectada en {casilla} con {probabilidad:.1%} probabilidad bayesiana")
                print("Sin desactivaciones disponibles")
                return False, probabilidad, desactivaciones
        else:
            # No es bomba o probabilidad muy baja
            return True, probabilidad, desactivaciones
    else:
        # No hubo mediciones positivas, no calculamos probabilidad bayesiana
        print("No hubo detecciones positivas, se asume seguro")
        return True, 0, desactivaciones

def obtener_siguiente(casilla, direccion):
    letras = ['A', 'B', 'C', 'D', 'E']
    
    col = casilla[0]
    fila = int(casilla[1:])
    idx = letras.index(col)
    
    if direccion == 'derecha':
        if idx < 4:
            return f"{letras[idx + 1]}{fila}", 'derecha', False
        else:
            if fila == 10:
                return None, None, True
            return f"E{fila + 1}", 'izquierda', False
    else:
        if idx > 0:
            return f"{letras[idx - 1]}{fila}", 'izquierda', False
        else:
            if fila == 10:
                return None, None, True
            return f"A{fila + 1}", 'derecha', False

def imprimir_tablero(tablero, boome_pos=None):
    letras = ['A', 'B', 'C', 'D', 'E']
    
    print("\n   A B C D E")
    for fila in range(1, 11):
        print(f"{fila:2} ", end=" ")
        for col in letras:
            casilla = f"{col}{fila}"
            if boome_pos == casilla:
                print("B", end=" ")
            elif tablero[casilla] == 1:
                print("1", end=" ")
            else:
                print("0", end=" ")
        print()
    print()

def mover_boome():

    tablero = crear_tablero_limpio()
    plantar_bomba(tablero)
    
    print("=== TABLERO INICIAL ===")
    imprimir_tablero(tablero)
    
    casilla_actual = "A1"
    direccion = 'derecha'
    movimientos = 0
    ruta = []
    posicion_anterior = None
    desactivaciones = 3
    
    # Probabilidad inicial de encontrar bomba en cualquier casilla
    prob_inicial = 1/50
    
    while True:
        movimientos += 1
        print(f"\n--- Movimiento {movimientos}: {casilla_actual} ---")
        
        # Verificar usando bayesiana
        sobrevive, probabilidad, desactivaciones = verificar_casilla_bayesiana(
            tablero, casilla_actual, desactivaciones, prob_inicial
        )
        
        if not sobrevive:
            print(f"\nBoome murio en {casilla_actual}")
            print(f"Probabilidad bayesiana final: {probabilidad:.1%}")
            print(f"Movimientos realizados: {movimientos}")
            print(f"Casillas recorridas: {len(ruta)}")
            return False
        
        # Limpiar la casilla anterior (ya no tiene a Boome)
        if posicion_anterior:
            tablero[posicion_anterior] = 0
        
        # Marcar posición actual de Boome
        ruta.append(casilla_actual)
        tablero[casilla_actual] = "B"
        posicion_anterior = casilla_actual
        
        imprimir_tablero(tablero, casilla_actual)
        
        # Avanzar a la siguiente casilla
        siguiente, nueva_dir, completado = obtener_siguiente(casilla_actual, direccion)
        
        if completado:
            print(f"\nBoome completo el tablero")
            print(f"Casillas recorridas: {len(ruta)} de 50")
            print(f"Desactivaciones usadas: {3 - desactivaciones}")
            guardar_tablero(tablero)
            return True
        
        casilla_actual = siguiente
        direccion = nueva_dir

def main():
    mover_boome()

if __name__ == "__main__":
    main()