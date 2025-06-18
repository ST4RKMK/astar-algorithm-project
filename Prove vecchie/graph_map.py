import networkx as nx
import random
import math

from astar_graph import nx_to_dict, astar_graph

def zero_heuristic(a, b):  # comportamento tipo Dijkstra
    return 0

def generate_map_like_graph(model="grid", n=20, m=20, radius=0.2, weight_mode="random", seed=42):
    random.seed(seed)

    if model == "grid":
        G = nx.grid_2d_graph(n, m, create_using=nx.DiGraph())
        mapping = {(i, j): i * m + j for i in range(n) for j in range(m)}
        G = nx.relabel_nodes(G, mapping)

    elif model == "geo":
        G = nx.random_geometric_graph(n, radius=radius, seed=seed)
        G = nx.DiGraph(G)
        G.remove_edges_from([(v, u) for u, v in G.edges() if G.has_edge(u, v)])

    elif model == "planar":
        # Usa triangolazione planare su punti casuali
        points = [(random.random(), random.random()) for _ in range(n)]
        G = nx.delaunay_graph(points)
        G = nx.DiGraph(G)
        G.remove_edges_from([(v, u) for u, v in G.edges() if G.has_edge(u, v)])

    else:
        raise ValueError("Modello non valido: usa 'grid', 'geo' o 'planar'")

    # Seleziona posizioni per disegno
    if model == "grid":
        pos = {i: (i % m, i // m) for i in G.nodes()}
    elif model == "geo":
        pos = nx.get_node_attributes(G, "pos")
    elif model == "planar":
        pos = nx.get_node_attributes(G, "pos")
        if not pos:
            # se non esistono, ricrea posizioni da coordinate
            pos = nx.kamada_kawai_layout(G)

    # Aggiungi pesi
    for u, v in G.edges():
        if weight_mode == "random":
            G[u][v]["weight"] = random.randint(1, 10)
        elif weight_mode == "euclidean" and u in pos and v in pos:
            G[u][v]["weight"] = round(math.dist(pos[u], pos[v]), 3)

    G.graph["pos"] = pos
    return G

def get_furthest_nodes(pos_dict):
    max_dist = 0
    start, goal = None, None
    for u in pos_dict:
        for v in pos_dict:
            if u != v:
                dist = math.dist(pos_dict[u], pos_dict[v])
                if dist > max_dist:
                    max_dist = dist
                    start, goal = u, v
    return start, goal

import matplotlib.pyplot as plt


def draw_graph_with_path(G, path=None, title="Grafo", save_path=None):
    pos = G.graph.get("pos", nx.spring_layout(G, seed=42))
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_size=400, node_color='lightgray', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')

    plt.title(title)
    plt.axis('off')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

import osmnx as ox

def load_osm_graph(place_name="Milan, Italy", weight_mode="length", network_type="drive"):
    # Scarica grafo stradale da OpenStreetMap
    G = ox.graph_from_place(place_name, network_type=network_type, simplify=True)

    # Converti in grafo diretto
    G = ox.utils_graph.get_digraph(G)

    # Estrai coordinate per disegno
    pos = {node: (data["x"], data["y"]) for node, data in G.nodes(data=True)}
    G.graph["pos"] = pos

    # Imposta pesi
    for u, v, data in G.edges(data=True):
        if weight_mode == "length" and "length" in data:
            G[u][v]["weight"] = data["length"]
        else:
            G[u][v]["weight"] = 1  # fallback

    return G



G = generate_map_like_graph(model="grid", n=30, m=30, weight_mode="random")
#G = load_osm_graph("Modena, Italy")
start, goal = get_furthest_nodes(G.graph["pos"])
path, _ = astar_graph(nx_to_dict(G), start, goal, heuristic=zero_heuristic)
draw_graph_with_path(G, path, title="Modena - A* path")
