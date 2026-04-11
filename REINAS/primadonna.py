"""
El problema de las 4 reinas se resuelve matemáticamente colocando 4 reinas en un tablero 
sin que se ataquen (misma fila, columna o diagonal). La solución se encuentra usando 
algoritmos de búsqueda con retroceso (backtracking), 
probando posiciones y descartando las que generan conflictos, 
resultando en dos soluciones principales. 
"""

tablero =  [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0,],
    [0,0,0,0,]
]

"""
 Podemos representarlo mejor en una permutacion asi
 De esta manera cada posicion corresponde a una fila
 y el numero dentro de ellas representa la columna
 reinas = (1,3,2,4)
 
 Se comparan dos reinas en posiciones (f1,c1) y (f2,c2)
 Condicion de no amenaza |c1-c2| != |f1-f2|
 En nuestro caso |1-4| = |1-4| se amenazan or estan en la misma columna 
"""

def imprimir_tablero(tablero,array_reinas):

    tab_i = [fila.copy() for fila in tablero]
    if len(array_reinas) >= 1: tab_i[0][array_reinas[0] - 1] = "R1"
    if len(array_reinas) >= 2: tab_i[1][array_reinas[1] - 1] = "R2"
    if len(array_reinas) >= 3: tab_i[2][array_reinas[2] - 1] = "R3"
    if len(array_reinas) == 4: tab_i[3][array_reinas[3] - 1] = "R4"
    
    for i in range(len(tab_i)):
        print(tab_i[i])
    print("\n")


def es_factible(array_reinas):

    f2 = len(array_reinas)-1
    c2 = array_reinas[f2]

    for fila  in range (len(array_reinas)-1):
        f1 = fila
        c1 = array_reinas[f1]

        if  (abs(f1 - f2) == abs(c1-c2)) or  (c1==c2):
            print("!!!  NO ES FACTIBLE MASTER  !!!\n")
            return False
    
    return True

def posicionar_reinas(array_reinas):
    
    if len(array_reinas) == 4:
        print(" EXITO LAS REINAS NO PELEAN LOS TERRENOS \n")
        print(array_reinas)
        return

    for numero in [1,2,3,4]: 
        
        array_reinas.append(numero)
        imprimir_tablero(tablero,array_reinas)

        ban_f = es_factible(array_reinas)

        if ban_f is True:
            posicionar_reinas(array_reinas)
    
        array_reinas.pop()

# Ejecución inicial
print("\n * * *  PROBLEMA DE LAS 4 REINAS \n")
posicionar_reinas([])










