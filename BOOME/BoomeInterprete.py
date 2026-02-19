import argparse
import anlex
from vm import BoomeVM

parser = argparse.ArgumentParser(
    prog='BoomeInterprete',
    description='Ejecuta un archivo de código para boome',
    epilog='Este programa fue hecho para la clase IA 2026'
)

parser.add_argument(
    'archivo_codigo',
    type=argparse.FileType('r'),
    help='Ejemplo:\nBoomeInterprete.py codigo.boome'
)

args = parser.parse_args()

if args.archivo_codigo:
    lineas = args.archivo_codigo.readlines()
    # Hacer copia de las lineas
    # .rstrip  saltos de línea \n y espacios al final
    lineas_originales = [l.rstrip() for l in lineas]
    # Limpiar para procesar
    lineas_procesar = []


    for i, l in enumerate(lineas):
        # ignorar comentarios y quitar espacios en blanco
        # el split divide la lista en dos al encontrar el caracter #
        #  el [0] indica que tomara lo que estaba antes del #
        l_limpia = l.split('#')[0].strip()
        if l_limpia:
            lineas_procesar.append((i, l_limpia))

    # EJEMPLO DE LINEA LIMPIA (0, "movi")
    ovm = BoomeVM()
    print("\n ESTADO INICIAL ")
    print(ovm)

    contador = 0

    while contador < len(lineas_procesar):


        #  contador=0  idx = 0, linea = 'movi'
        idx, linea = lineas_procesar[contador]
        print(f"\n--- Ejecutando línea {idx}: {linea} ---")

        # Parsear la linea con anlex
        instruccion = anlex.procesar_linea(linea)

        if not instruccion:
            print(f"ERROR de sintaxis en la linea {idx}: {linea}")
            break


        # 1 podemos ejecutar la siguiente linea sin problemas
        # Si es difeente de uno nos da el numero de linea a la cual queremos volver o en otras
        # palabras el destino

        siguiente = ovm.fetchDecodeExecute(instruccion)

        # MOSSTRAR ESTADO DESPUES DE EJECUTAR
        print(ovm)

        # isinstance(objeto, tipo)
        # Actualizar el contador
        if isinstance(siguiente, int):
            if siguiente != 1:  # Es un salto
                contador = siguiente  # ¡Cambiamos el flujo!
            else:
                contador += 1  # Siguiente instrucción normalmente
        else:
            contador += 1

        if not ovm.Vivo:
            print("Boome ha muerto :( DETENIENDO EJECUCION")
            break

    print("\n--- EJECUCIÓN FINALIZADA ---")









