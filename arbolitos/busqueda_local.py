import json
from collections import deque

def cargar_json(nombre):
    try:
        with open(nombre, 'r') as f:
            return json.load(f) 
    except FileNotFoundError:
        print("Error, archivo no encontrado")
        return {} 

arbol = cargar_json('arbolito.json')



def trepador_profundo(data, objetivo, nodo_actual=None, visitados=None, ruta=None):
    if visitados is None:
        visitados = set()
    if ruta is None:
        ruta = []
    if nodo_actual is None:
        nodo_actual = next(iter(data))

    visitados.add(nodo_actual)
    ruta.append(nodo_actual)

    print(f"Visitando: {nodo_actual}")

    if nodo_actual == objetivo:
        print(f"¡Objetivo '{objetivo}' encontrado!")
        return True

    for vecino in data.get(nodo_actual, []):
        if vecino not in visitados:
            encontrado = trepador_profundo(data, objetivo, vecino, visitados, list(ruta))
            if encontrado:
                return True
    return False



def trepador_ancho(data, objetivo, inicio=None):
    if inicio is None:
        inicio = next(iter(data))

    cola = deque([(inicio, [inicio])])
    visitados = set([inicio])

    while cola:
        nodo_actual, ruta = cola.popleft()
        print(f"Visitando: {nodo_actual}")

        if nodo_actual == objetivo:
            print(f"¡Objetivo '{objetivo}' encontrado!")
            return True

        for vecino in data.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, ruta + [vecino]))
    return False


colina = cargar_json('colina.json')

def subir_colina(inicio, fin):
    memoria = 3
    if inicio == fin:
        print(f"\n¡Objetivo '{fin}' encontrado en el inicio!")
        return [inicio]

    # Cada candidato guarda: (costo_acumulado, nodo_actual, camino_recorrido, nodos_visitados)
    candidatos = [(0, inicio, [inicio], {inicio})]
    mejor_costo = float('inf')
    mejor_camino = []

    while candidatos:
        print(f"Nodos en memoria: {[c[1] for c in candidatos]}")
        
        siguientes = []
        for costo, nodo, camino, visitados in candidatos:
            # Explorar los vecinos del nodo actual
            for vecino, peso in colina.get(nodo, {}).items():
                nuevo_costo = costo + peso
                nuevo_camino = camino + [vecino]

                # Si encontramos el objetivo, actualizamos el mejor camino si es más corto
                if vecino == fin:
                    if nuevo_costo < mejor_costo:
                        mejor_costo = nuevo_costo
                        mejor_camino = nuevo_camino
                    continue

                # Agregamos vecinos si no están visitados y aún tienen posibilidad de ser el mejor camino
                if vecino not in visitados and nuevo_costo < mejor_costo:
                    nuevos_visitados = visitados.copy()
                    nuevos_visitados.add(vecino)
                    siguientes.append((nuevo_costo, vecino, nuevo_camino, nuevos_visitados))
        
        # Ordenamos las opciones por el menor costo (ascendente)
        siguientes.sort(key=lambda x: x[0])
        
        # Conservamos solo las mejores opciones según el límite de memoria
        candidatos = siguientes[:memoria]

    if mejor_camino:
        print(f"\n¡Objetivo '{fin}' encontrado!")
        print(f"Camino: {' -> '.join(mejor_camino)} | Costo total: {mejor_costo}\n")
        return mejor_camino

    print("No se encontró un camino posible.")
    return []




G = None

def profundo(objetivo):
    global G
    G = trepador_profundo(arbol, objetivo)

def ancho(objetivo):
    global G
    G = trepador_ancho(arbol, objetivo)


if __name__ == "__main__":
    print("REPL de Búsqueda Iniciado.")
    print("Comandos útiles:")
    print("- profundo('AC')  # Ejecuta busqueda en profundidad hacia 'AC'")
    print("- ancho('AC')     # Ejecuta busqueda en anchura hacia 'AC'")
    print("- subir_colina('A', 'J') # Encuentra el camino más corto en el grafo de colina")

    while True:
        try:
            print()
            R = input(">")
            
            if R == 'salir':
                break
            
            T = eval(R)
            
            if T is not None:
                print(T)

        except Exception as e:
            print("Error!!! ", e)

