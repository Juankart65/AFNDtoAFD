from Automatas import *
from DibujoAutomata import *


# Con este metodo se llena la matriz la cual  representa la tabla de autómata determinista  
# o no determinista
def llenar_afn_por_consola():
    afn = {
        'estados': [],
        'alfabeto': [],
        'transiciones': {},
        'estado_inicial': None,
        'estados_finales': set()
    }

    # Llenar estados
    estados_str = input("Ingrese los estados separados por comas: ")
    afn['estados'] = estados_str.split(',')

    # Llenar alfabeto
    alfabeto_str = input("Ingrese el alfabeto separado por comas: ")
    afn['alfabeto'] = alfabeto_str.split(',')

    # Llenar transiciones
    for estado in afn['estados']:
        transiciones_estado = {}
        for simbolo in afn['alfabeto']:
            transiciones_str = input(f"Ingrese los estados alcanzables desde {estado} con el símbolo {simbolo} separados por comas (deje vacío si no hay transición): ")
            if transiciones_str:
                transiciones_estado[simbolo] = set(transiciones_str.split(','))
        afn['transiciones'][estado] = transiciones_estado

    # Llenar estado inicial
    estado_inicial = input("Ingrese el estado inicial: ")
    afn['estado_inicial'] = estado_inicial

    # Llenar estados finales
    estados_finales_str = input("Ingrese los estados finales separados por comas: ")
    afn['estados_finales'] = set(estados_finales_str.split(','))

    return afn

afn = llenar_afn_por_consola()

# Recorrer transiciones
print("\nTransiciones:")
for origen, destinos in afn['transiciones'].items():
    for simbolo, destino in destinos.items():
        print(f"De {origen} a {destino} con el símbolo {simbolo}")

if(es_automata_determinista(afn)):
    print(afn)
else:
    afd = convertir_afn_a_afd(afn)
    afd_pydot = convert_to_pydot_format(afd)
    dibujar_automata(afd_pydot)
