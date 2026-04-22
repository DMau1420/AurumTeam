import json

def cargar_json(nombre):
    with open(nombre, 'r') as f:
        return json.load(f)

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

G = trepador_profundo(arbol, "ABA")
for x in G:
    print(x)
