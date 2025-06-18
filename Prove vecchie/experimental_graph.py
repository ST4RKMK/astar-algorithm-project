import networkx as nx
import random
import math

from matplotlib import pyplot as plt

import networkx as nx


def generate_experimental_graph(model="gnp", n=30, p=0.1, k=50, delta=0.2, m=10, seed=42, weight_range=(1, 10)):
    random.seed(seed)


    if model == "gnp":
        # graph(n,p): grafo con probabilità p per ogni arco
        graph = nx.gnp_random_graph(n, p, seed=seed, directed=True)

    elif model == "gnk":
        # graph(n,k): grafo con esattamente k archi scelti a caso
        graph = nx.gnm_random_graph(n, k, seed=seed, directed=True)

    elif model == "grid":
        # Griglia nxm: utile per simulare mappe e pathfinding
        graph = nx.grid_2d_graph(n, m, create_using=nx.DiGraph())
        mapping = {(i, j): i * m + j for i in range(n) for j in range(m)}
        graph = nx.relabel_nodes(graph, mapping)

    elif model == "geo":
        # P(n, δ): grafo geometricamente connesso su piano [0,1]x[0,1]
        graph = nx.random_geometric_graph(n, radius=delta, seed=seed)
        graph = nx.DiGraph(graph)  # forza la direzione
        # Rimuove archi bidirezionali duplicati (li teniamo direzionali)
        graph.remove_edges_from([(v, u) for u, v in graph.edges() if graph.has_edge(u, v)])

    else:
        raise ValueError("Modello non riconosciuto: usa 'gnp', 'gnk', 'geo', o 'grid'")



        # Definisci le posizioni (necessarie per pesi euclidei e disegno)
    if model == "grid":
        width = m
        pos = {node: (node % width, node // width) for node in graph.nodes()}
    elif model == "geo":
        pos = nx.get_node_attributes(graph, "pos")
    else:
        pos = nx.spring_layout(graph, seed=seed)

    graph.graph["pos"] = pos

    # Assegna pesi
    for u, v in graph.edges():
        if model in ("geo", "grid") and u in pos and v in pos:
            dist = math.dist(pos[u], pos[v])
            graph[u][v]["weight"] = round(dist, 3)
        else:# Assegna pesi casuali agli archi
            graph[u][v]["weight"] = random.randint(*weight_range)

    return graph



def get_longest_shortest_path(graph):
    try:
        # Distanze minime da ogni nodo a tutti gli altri (considerando i pesi)
        lengths = dict(nx.all_pairs_dijkstra_path_length(graph, weight="weight"))

        max_dist = 0
        best_pair = (None, None)

        for u, targets in lengths.items():
            for v, dist in targets.items():
                if dist > max_dist:
                    max_dist = dist
                    best_pair = (u, v)

        return best_pair
    except Exception as e:
        print(f"[WARN] Errore nel calcolo del path più lungo: {e}")
        # Fallback: ritorna due nodi distinti qualsiasi
        nodes = list(graph.nodes())
        return nodes[0], nodes[-1] if len(nodes) > 1 else (nodes[0], nodes[0])
