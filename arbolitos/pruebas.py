import json

def cargar_json(nombre):
    with open(nombre, 'r') as f:
        return json.load(f)

arbol = cargar_json('arbolito.json')

def trepador(data):
    pass

def trepador_profundo(data, objetivo, nodo_actual=None, visitados=None, ruta=None):
    """
    Realiza un recorrido en profundidad (DFS) de forma recursiva.
    Busca 'objetivo' en el grafo/árbol 'data'.
    """
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
        return ruta

    for vecino in data.get(nodo_actual, []):
        if vecino not in visitados:
            resultado = trepador_profundo(data, objetivo, vecino, visitados, list(ruta))
            if resultado:
                return resultado

    return None


def trepador_ancho(data, objetivo, inicio=None):
    """
    Realiza un recorrido en anchura (BFS) de forma iterativa.
    Busca 'objetivo' en el grafo/árbol 'data'.
    """
    if inicio is None:
        # Si no se indica el inicio, tomamos el primer nodo del diccionario
        inicio = next(iter(data))

    from collections import deque
    # La cola guarda tuplas de (nodo_actual, ruta_hasta_ahora)
    cola = deque([(inicio, [inicio])])
    visitados = set([inicio])

    while cola:
        nodo_actual, ruta = cola.popleft()
        print(f"Visitando: {nodo_actual}")

        if nodo_actual == objetivo:
            print(f"¡Objetivo '{objetivo}' encontrado!")
            return ruta

        for vecino in data.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, ruta + [vecino]))

    return None




trepador_profundo(arbol, "ABA")
print()
trepador_ancho(arbol, "AC")



colina = cargar_json('colina.json')

def subir(inicio, fin, pasos):
    pass






'''
while True:
    R = input(">")
    
    if R == 'salir':
        break
    
    T = eval(R)
    print(T)

'''