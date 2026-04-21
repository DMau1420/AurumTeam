G = None

def contar(Stream):
    Data = {
            "1": 0,
            "2": 0,
            "0": 0 
    }

    while Stream:
        a = Stream.read(1)

        if a[0] == 1:
            Data["1"] = Data["1"] + 1
        if a[0] == 2:
            Data["2"] = Data["2"] + 1        
        if a[0] == 0:
            Data["0"] = Data["0"] + 1
        yield Data
    Stream.close()

def abrirVotos():
    Archivo = open("votos.bin")
    global G
    G = contar(Archivo)

while True:
    R = input(">")
    
    if R == 'salir':
        break
    
    T = eval(R)
    print(T)


