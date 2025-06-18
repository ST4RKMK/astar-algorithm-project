import heapq
import random

import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id, parent=None):
        self.id = id
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.f < other.f


def astar_graph(graph, start_id, goal_id, heuristic):
    start_node = Node(start_id)
    goal_node = Node(goal_id)

    open_list = []
    closed_set = set()

    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current = heapq.heappop(open_list)

        if current.id == goal_node.id:
            path = []
            cost = 0
            while current:
                path.append(current.id)
                if current.parent:
                    for neighbor, weight in graph[current.parent.id]:
                        if neighbor == current.id:
                            cost += weight
                            break
                current = current.parent
            path = path[::-1]

            return path, {
                "nodi_espansi": len(closed_set),
                "lunghezza_percorso": len(path),
                "path_cost": cost
            }

        closed_set.add(current.id)

        for neighbor_id, cost in graph[current.id]:
            if neighbor_id in closed_set:
                continue

            neighbor = Node(neighbor_id, current)
            neighbor.g = current.g + cost
            neighbor.h = heuristic(neighbor_id, goal_id)
            neighbor.f = neighbor.g + neighbor.h

            if any(n.id == neighbor.id and n.f <= neighbor.f for _, n in open_list):
                continue

            heapq.heappush(open_list, (neighbor.f, neighbor))

    return None, {
        "nodi_espansi": len(closed_set),
        "lunghezza_percorso": 0,
        "path_cost": 0
    }  # no path found

def draw_graph(graph_input, path=None, title="Grafo A*"):
    # Se è un dict, converti in DiGraph
    if isinstance(graph_input, dict):
        G = nx.DiGraph()
        for node, neighbors in graph_input.items():
            for neighbor, cost in neighbors:
                G.add_edge(node, neighbor, weight=cost)
    elif isinstance(graph_input, nx.Graph):
        G = graph_input
    else:
        raise ValueError("Input deve essere un dizionario o un NetworkX Graph")

    # Determina layout
    if "pos" in G.graph:
        pos = G.graph["pos"]
    elif nx.get_node_attributes(G, 'pos'):
        pos = nx.get_node_attributes(G, 'pos')
    else:
        pos = nx.spring_layout(G, seed=42)

    # Etichette archi
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Disegno base
    nx.draw(G, pos, with_labels=True, node_size=600, node_color='lightgray', font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Evidenzia percorso
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')

    plt.title(title if path else f"{title} (fallito)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def generate_weighted_graph(num_nodes=50, num_edges=200, min_w=1, max_w=10):
    graph = nx.gnm_random_graph(num_nodes, num_edges, directed=True)

    for (u, v) in graph.edges():
        graph[u][v]['weight'] = random.randint(min_w, max_w)

    return graph

def nx_to_dict(G):
    graph_dict = {}
    for node in G.nodes():
        graph_dict[node] = []
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1)
        graph_dict[u].append((v, weight))
    return graph_dict



def draw_cgraph(G, path=None):
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Disegna nodi e archi base
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightgray', font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')

    plt.title("Grafo generato + percorso A*")
    plt.show()


