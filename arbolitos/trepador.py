import json
from collections import deque

def cargar_json(nombre):
    try:
        with open(nombre, 'r') as f:
            return json.load(f) 
    except FileNotFoundError:
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

    yield f"Visitando: {nodo_actual}"

    if nodo_actual == objetivo:
        yield f"¡Objetivo '{objetivo}' encontrado!"
        return True

    for vecino in data.get(nodo_actual, []):
        if vecino not in visitados:
            encontrado = yield from trepador_profundo(data, objetivo, vecino, visitados, list(ruta))
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
        yield f"Visitando: {nodo_actual}"

        if nodo_actual == objetivo:
            yield f"¡Objetivo '{objetivo}' encontrado!"
            return

        for vecino in data.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, ruta + [vecino]))




colina = cargar_json('colina.json')

def subir(inicio, fin, pasos):
    # No se que hace porque no me acuerdo
    pass




G = None

def profundo(objetivo):
    global G
    G = trepador_profundo(arbol, objetivo)

def ancho(objetivo):
    global G
    G = trepador_ancho(arbol, objetivo)

print()

print("REPL de Búsqueda Iniciado.")
print("Comandos útiles:")
print("- profundo('AC')  # Inicializa trepador profundo hacia 'AC'")
print("- ancho('AC')     # Inicializa trepador ancho hacia 'AC'")
print("- next(G)         # Avanza un paso en la búsqueda")

while True:
    try:
        R = input(">")
        
        if R == 'salir':
            break
        
        T = eval(R)
        
        if T is not None:
            print(T)

    except Exception as e:
        print("Error!!! ", e)

