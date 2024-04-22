import pydot
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin' 

def dibujar_automata(automata):
    graph = pydot.Dot(graph_type='digraph')
    estados = automata['estados']
    transiciones = automata['transiciones']
    estado_inicial = automata['estado_inicial']
    estados_finales = automata['estados_finales']

    # Verificar el contenido de las variables después del bucle
    print("\nEstados:", estados)
    print("\nTransiciones:", transiciones)
    print("\nEstado inicial:", estado_inicial)
    print("\nEstados finales:", estados_finales)

    # Agregar nodos
    for estado in estados:
        if estado:  # Verifica si el estado no está vacío
            shape = 'circle'
            if estado == estado_inicial:
                shape = 'doublecircle'
            elif estado in estados_finales:
                shape = 'doublecircle'
            node = pydot.Node(estado, shape=shape)
            graph.add_node(node)

    # Agregar arcos
    for origen, trans in transiciones.items():
        for simbolo, destinos in trans.items():
            for destino in destinos:
                graph.add_edge(pydot.Edge(origen, destino, label=simbolo))

    # Guardar y mostrar el gráfico
    graph.write_png('automata.png')
    # graph.write_pdf('automata.pdf')


