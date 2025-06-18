import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_geometric_graph(n=50, r=0.2, seed=42):
    """
    Crea un grafo geometrico con n nodi posizionati casualmente nel piano [0,1]x[0,1],
    connessi se la distanza euclidea tra due nodi è inferiore a r.

    :param n: Numero di nodi
    :param r: Raggio di connessione
    :param seed: Seed per la riproducibilità
    :return: Grafo G, posizioni dei nodi pos
    """
    np.random.seed(seed)
    pos = {i: (np.random.rand(), np.random.rand()) for i in range(n)}
    G = nx.random_geometric_graph(n, r, pos=pos)

    # Aggiunge il peso (distanza euclidea) agli archi
    for u, v in G.edges():
        G.edges[u, v]['weight'] = int(round(np.linalg.norm(np.array(pos[u]) - np.array(pos[v])) * 10))

    return G, pos


def generate_random_geometric_graph(n=50, r=0.2, seed=None):
    """
    Crea un grafo geometrico con n nodi connessi se la distanza euclidea è < r.
    :param n: Numero di nodi
    :param r: Raggio di connessione
    :param seed: Seed per la randomizzazione (None = completamente casuale)
    """
    if seed is not None:
        np.random.seed(seed)

    pos = {i: (np.random.rand(), np.random.rand()) for i in range(n)}
    G = nx.random_geometric_graph(n, r, pos=pos)

    for u, v in G.edges():
        G.edges[u, v]['weight'] = int(round(np.linalg.norm(np.array(pos[u]) - np.array(pos[v])) * 10))

    return G, pos


def generate_grid_graph(rows=5, cols=10):
    G = nx.grid_2d_graph(rows, cols)

    # Posizioni originali (prima della conversione)
    original_pos = {(i, j): (j, -i) for i, j in G.nodes()}  # j = x, -i = y per layout ordinato

    # Rinomina nodi con interi
    mapping = {node: idx for idx, node in enumerate(sorted(G.nodes(), key=lambda x: (x[0], x[1])))}
    G = nx.relabel_nodes(G, mapping)

    # Ricrea il dizionario delle posizioni convertite
    pos = {mapping[node]: original_pos[node] for node in mapping}

    return G, pos


def generate_random_grid_graph(rows=5, cols=10, remove_edge_prob=0.2, random_weights=True):
    G = nx.grid_2d_graph(rows, cols)

    # Rimuovi archi con una certa probabilità
    edges_to_remove = [(u, v) for u, v in G.edges() if np.random.rand() < remove_edge_prob]
    G.remove_edges_from(edges_to_remove)

    # Assegna pesi casuali
    if random_weights:
        for u, v in G.edges():
            G.edges[u, v]['weight'] = np.random.randint(1, 11)

    # Rinomina nodi e genera posizioni
    original_pos = {(i, j): (j, -i) for i, j in G.nodes()}
    mapping = {node: idx for idx, node in enumerate(sorted(G.nodes(), key=lambda x: (x[0], x[1])))}
    G = nx.relabel_nodes(G, mapping)
    pos = {mapping[node]: original_pos[node] for node in mapping}

    return G, pos


def generate_gnk_graph(n=50, k=150):
    G = nx.gnm_random_graph(n, k)
    for u, v in G.edges():
        G.edges[u, v]['weight'] = np.random.randint(1, 11)
    pos = nx.spring_layout(G, seed=np.random.randint(1000))
    return G, pos

def generate_gnp_graph(n=50, p=0.05):
    G = nx.gnp_random_graph(n, p)
    for u, v in G.edges():
        G.edges[u, v]['weight'] = np.random.randint(1, 11)
    pos = nx.spring_layout(G, seed=np.random.randint(1000))
    return G, pos

def draw_graph(G, pos, title="Grafo", show_weights=True, start=None, goal=None):
    plt.figure(figsize=(8, 8))
    #nx.draw(G, pos, node_size=50, edge_color='gray', with_labels=False)

    model_name = title.lower()  # ricavato dal titolo

    if pos is None:
        if model_name.startswith("grafo g(n,p)") or "gnp" in model_name:
            pos = nx.spring_layout(G, seed=42, k=0.6)
        else:
            pos = nx.spring_layout(G, seed=42)

    # Rimuovi nodi isolati per G(n,p)
    if model_name.startswith("grafo g(n,p)") or "gnp" in model_name:
        isolated = list(nx.isolates(G))
        if isolated:
            print(f"[INFO] Rimuovo {len(isolated)} nodi isolati")
            G.remove_nodes_from(isolated)
            pos = {node: pos[node] for node in G.nodes()}

    # Colori nodi
    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append("green")  # start = verde
        elif node == goal:
            node_colors.append("red")  # goal = rosso
        else:
            node_colors.append("skyblue")

    nx.draw(G, pos, node_size=100, node_color=node_colors, edge_color='gray', with_labels=False)

    if show_weights:
        labels = nx.get_edge_attributes(G, 'weight')
        #labels = {k: f"{v:.1f}" for k, v in labels.items()}  # opzionale: arrotonda a 1 decimale
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
    plt.title(title)
    plt.axis('equal')
    plt.show()

def draw_geometric_graph(G, pos):
    """
    Visualizza un grafo geometrico.
    :param G: Il grafo NetworkX
    :param pos: Dizionario {nodo: (x, y)} con le posizioni
    """
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_size=50, edge_color='gray', with_labels=False)
    plt.title("Grafo Geometrico")
    plt.axis('equal')
    plt.show()



def choose_start_and_goal(G, must_be_connected=True):
    """
    Sceglie due nodi distinti (start, goal) nel grafo G.
    Se must_be_connected=True, garantisce che start e goal siano nello stesso componente connesso.

    :param G: grafo NetworkX
    :param must_be_connected: richiedi che esista un cammino tra i due nodi
    :return: (start, goal)
    """
    nodes = list(G.nodes())

    if must_be_connected and not nx.is_connected(G):
        # Lavora sul componente connesso più grande
        largest_cc = max(nx.connected_components(G), key=len)
        nodes = list(largest_cc)

    start = random.choice(nodes)
    goal_choices = [node for node in nodes if node != start]
    goal = random.choice(goal_choices)
    return start, goal

def get_most_distant_nodes(G):
    """
    Restituisce la coppia di nodi (start, goal) più lontani nel grafo (in termini di numero di archi).
    Funziona solo se il grafo è connesso.
    """
    if not nx.is_connected(G):
        G = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)

    lengths = dict(nx.all_pairs_shortest_path_length(G))
    max_dist = -1
    start, goal = None, None

    for u in lengths:
        for v in lengths[u]:
            if lengths[u][v] > max_dist:
                max_dist = lengths[u][v]
                start, goal = u, v

    return start, goal


def get_most_distant_nodes_weighted(G, weight="weight"):
    """
    Restituisce la coppia (start, goal) con la massima distanza Dijkstra.
    Usa pesi sugli archi.
    """
    if not nx.is_connected(G):
        G = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)

    max_dist = -1
    start, goal = None, None

    for source in G.nodes():
        lengths = nx.single_source_dijkstra_path_length(G, source, weight=weight)
        for target, dist in lengths.items():
            if dist > max_dist:
                max_dist = dist
                start, goal = source, target

    return start, goal


# Esempio d'uso
if __name__ == "__main__":
    G_geo, pos_geo = generate_random_geometric_graph(n=200, r=0.2)
    start, goal = get_most_distant_nodes_weighted(G_geo)
    print("Grafo geometrico start:", start, "goal:", goal)
    draw_graph(G_geo, pos_geo, "Grafo Geometrico", start=start, goal=goal)

    G_grid, pos_grid = generate_random_grid_graph(rows=10, cols=10)
    start, goal = get_most_distant_nodes_weighted(G_grid)
    print("Griglia random start:", start, "goal:", goal)
    draw_graph(G_grid, pos_grid, "Grafo a Griglia ", start=start, goal=goal)

    G_gnk, pos_gnk = generate_gnk_graph(n=100, k=250)
    start, goal = get_most_distant_nodes_weighted(G_gnk)
    print("Grafo G(n,k) start:", start, "goal:", goal)
    draw_graph(G_gnk, pos_gnk, "Grafo G(n,k) ", start=start, goal=goal)

    G_gnp, pos_gnp = generate_gnp_graph(n=100, p=0.05)
    start, goal = get_most_distant_nodes_weighted(G_gnp)
    print("Grafo G(n,p)  start:", start, "goal:", goal)
    draw_graph(G_gnp, pos_gnp, "Grafo G(n,p) ", start=start, goal=goal)

