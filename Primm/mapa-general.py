import networkx as nx
import matplotlib.pyplot as plt

# primero generamos un grafo con la funcion de networkx
grafo = nx.Graph()

# creamos una lista de vertices. en este caso simplemente usamos las letras del abecedario
vertices = ["a", "b", "c", "d", "e", "f", "g", "h"]
grafo.add_nodes_from(vertices) # podemos agregarle los nodos o vertices directamente usando la lista anterior

# despues podemos crear los aristas, en este caso teniendo pesos de forma aleatoria
aristas = [
    ("a", "b", 7),
    ("a", "c", 3),
    ("a", "d", 9),
    ("b", "c", 5),
    ("b", "e", 12),
    ("c", "d", 4),
    ("c", "f", 8),
    ("d", "f", 2),
    ("d", "g", 11),
    ("e", "f", 6),
    ("e", "h", 10),
    ("f", "g", 1),
    ("f", "h", 13),
    ("g", "h", 4),
    ("b", "h", 15)
]

grafo.add_weighted_edges_from(aristas) # despues podemos agregar las aristas de la lista anterior que creamos

arbol_expansion_minima = nx.minimum_spanning_tree(grafo, algorithm="kruskal") # sacamos el arbol de expansion minima

posicion_grafos = nx.spring_layout(grafo, seed=1) # esta variable la usamos para sacar una posicion estandar para los dos grafos, el original y el de expansion
# basicamente aplicamos seed = 1 para que siempre se grafiquen o generen igual graficamente.

# grafica del grafo original
plt.figure(figsize=(8, 6))

nx.draw(
    grafo,
    posicion_grafos,
    with_labels=True,
    node_color="lightpurple",
    node_size=900,
    font_size=15,
    edge_color="black"
)

# Etiquetas de pesos
etiquetas_pesos = nx.get_edge_attributes(grafo, "weight")

nx.draw_networkx_edge_labels(
    grafo,
    posicion_grafos,
    edge_labels=etiquetas_pesos,
    font_size=10
)

plt.title("Grafo original con 8 vértices y 15 aristas")
plt.show()

# ===============================
# 6. GRAFICAR ÁRBOL DE EXPANSIÓN MÍNIMA
# ===============================

plt.figure(figsize=(8, 6))

nx.draw(
    arbol_expansion_minima,
    posicion_grafos,
    with_labels=True,
    node_color="lightgreen",
    node_size=900,
    font_size=12,
    font_weight="bold",
    edge_color="red",
    width=2
)

# Etiquetas de pesos del MST
etiquetas_mst = nx.get_edge_attributes(arbol_expansion_minima, "weight")

nx.draw_networkx_edge_labels(
    arbol_expansion_minima,
    posicion_grafos,
    edge_labels=etiquetas_mst,
    font_size=10
)

plt.title("Árbol de Expansión Mínima usando Kruskal")
plt.show()