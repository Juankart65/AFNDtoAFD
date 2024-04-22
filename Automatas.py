def es_automata_determinista(afn):
    transiciones = set()

    # Analizar las transiciones
    for estado, transiciones_estado in afn['transiciones'].items():
        for simbolo, destinos in transiciones_estado.items():
            # Verificar si hay múltiples destinos para el mismo símbolo
            if len(destinos) > 1:
                return False
            for estado in destinos:
                if (estado, simbolo) in transiciones:
                    # Si ya existe una transición para un estado y símbolo dado,
                    # entonces el autómata es no determinista
                    return False
                else:
                    transiciones.add((estado, simbolo))

    # Si no se encontraron problemas, el autómata es determinista
    return True



def epsilon_cerradura(afn, estados):
    epsilon_cerradura_set = set(estados)
    for estado in estados:
        if estado in afn['transiciones']:  # Verificar si el estado tiene transiciones definidas
            epsilon_cerradura_set |= afn['transiciones'][estado].get('', set())  # Añadir estados alcanzables con transiciones epsilon
    return epsilon_cerradura_set


def mover(afn, estados, simbolo):
    mover_set = set()
    for estado in estados:
        mover_set |= afn['transiciones'][estado].get(simbolo, set())  # Agregar estados alcanzables con la entrada dada
    return mover_set

def convertir_afn_a_afd(afn):
    afd = {
        'estados': [],
        'alfabeto': afn['alfabeto'],
        'transiciones': {},
        'estado_inicial': None,
        'estados_finales': set()
    }

    # Calcula el estado inicial del AFD
    estado_inicial_afd = epsilon_cerradura(afn, {afn['estado_inicial']})
    afd['estados'].append(estado_inicial_afd)
    afd['estado_inicial'] = estado_inicial_afd

    # Inicializa los estados procesados y pendientes
    estados_procesados = set()
    estados_pendientes = [estado_inicial_afd]

    # Mientras haya estados pendientes por procesar
    while estados_pendientes:
        estado_actual_afd = estados_pendientes.pop()
        estados_procesados.add(tuple(estado_actual_afd))

        # Calcula las transiciones para cada símbolo del alfabeto
        transiciones_estado_actual = {}
        for simbolo in afd['alfabeto']:
            estados_alcanzables_afn = epsilon_cerradura(afn, mover(afn, estado_actual_afd, simbolo))
            transiciones_estado_actual[simbolo] = estados_alcanzables_afn

            if estados_alcanzables_afn not in afd['estados']:
                afd['estados'].append(estados_alcanzables_afn)
                estados_pendientes.append(estados_alcanzables_afn)

        # Asigna las transiciones al estado actual del AFD
        afd['transiciones'][tuple(estado_actual_afd)] = transiciones_estado_actual

        # Si alguno de los estados alcanzables es final en el AFN, marcar el estado actual del AFD como final
        if any(estado in afn['estados_finales'] for estado in estado_actual_afd):
            afd['estados_finales'].add(tuple(estado_actual_afd))

    return afd

def convert_to_pydot_format(automata):
    # Convertir los conjuntos de estados en cadenas simples
    estados = ["".join(estado) for estado in automata['estados']]

    # Convertir las tuplas de transiciones en diccionarios con cadenas simples como claves
    transiciones = {}
    for estado_tupla, trans in automata['transiciones'].items():
        estado_str = "".join(estado_tupla)
        transiciones[estado_str] = {}
        for simbolo, destinos in trans.items():
            if isinstance(destinos, set):
                # Combinar los destinos en un solo estado
                if len(destinos) >= 2:  # Verificar si hay mas de dos destinos
                    destino_combinado = "".join(destinos)
                    destino_combinado = "".join(destinos)
                    if destino_combinado in automata['estados']:
                        transiciones[estado_str][simbolo] = [destino_combinado]
                    else:
                        transiciones[estado_str][simbolo] = [destino_combinado]
                        automata['estados'].append(destino_combinado)  # Agregar el nuevo estado a la lista de estados
                else:
                    # Si no hay exactamente dos destinos, conservar los destinos originales
                    transiciones[estado_str][simbolo] = ["".join(destino) for destino in destinos]
            else:
                # Convertir los destinos en cadenas simples
                transiciones[estado_str][simbolo] = "".join(destinos)

    # Convertir el estado inicial a una cadena simple
    estado_inicial = "".join(automata['estado_inicial'])

    # Convertir los conjuntos de estados finales en listas de cadenas simples
    estados_finales = ["".join(estado) for estado in automata['estados_finales']]

    # Construir el diccionario compatible con pydot
    automata_pydot = {
        'estados': estados,
        'alfabeto': automata['alfabeto'],
        'transiciones': transiciones,
        'estado_inicial': estado_inicial,
        'estados_finales': estados_finales
    }

    return automata_pydot


# # Ejemplo de uso
# afn = {
#     'estados': ['q0', 'q1', 'q2'],
#     'alfabeto': ['0', '1'],
#     'transiciones': {
#         'q0': {'0': {'q1'}, '1': {'q0', 'q2'}},
#         'q1': {'0': {'q2'}, '1': set()},
#         'q2': {'0': set(), '1': {'q2'}}
#     },
#     'estado_inicial': 'q0',
#     'estados_finales': {'q2'}
# }
