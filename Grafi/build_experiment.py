import csv
import os
import time
from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx
from generate_graph import generate_random_grid_graph, choose_start_and_goal
from astar_graph import astar_graph, euclidean_heuristic, manhattan_heuristic
from researchgraphalgo import bfs, dfs


def run_experiment_from_generator(G, pos, start, goal, graph_name="custom_graph", output_dir="results_graphs", num_trials=1):
    """
    Esegue A*, BFS e DFS su un grafo già generato, e salva i risultati.

    :param G: grafo NetworkX
    :param pos: dizionario {nodo: (x,y)} per disegno
    :param start: nodo iniziale
    :param goal: nodo obiettivo
    :param graph_name: nome logico del grafo
    :param output_dir: cartella di salvataggio CSV e immagini
    :param trial_id: numero del trial (usato nel nome file)
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"{graph_name}_results.csv")

    # Converti il grafo in formato dizionario per l'algoritmo
    graph_dict = {node: [(v, data["weight"]) for v, data in G[node].items()] for node in G.nodes()}

    algos = {
        "astar": lambda g, s, t: astar_graph(g, s, t, heuristic=lambda a, b: 0),
        "astar_manhattan": lambda g, s, t: astar_graph(g, s, t, heuristic=manhattan_heuristic, pos=pos),
    "astar_euclidean": lambda g, s, t: astar_graph(g, s, t, heuristic=euclidean_heuristic, pos=pos),
        "bfs": bfs,
        "dfs": dfs
    }

    with open(csv_path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "graph", "trial", "algo", "start", "goal", "success",
            "path_len", "path_cost", "nodes_expanded", "time_sec",
            "n_nodes", "n_edges", "density"
        ])
        if file.tell() == 0:
            writer.writeheader()

        for algo_name, func in algos.items():
            for trial in range(1, num_trials + 1):
                t0 = time.perf_counter()
                path, stats = func(graph_dict, start, goal)
                t1 = time.perf_counter()

                writer.writerow({
                    "graph": graph_name,
                    "trial": trial,
                    "algo": algo_name,
                    "start": start,
                    "goal": goal,
                    "success": "yes" if path else "no",
                    "path_len": stats["lunghezza_percorso"],
                    "path_cost": stats.get("path_cost", 0),
                    "nodes_expanded": stats["nodi_espansi"],
                    "time_sec": round(t1 - t0, 6),
                    "n_nodes": G.number_of_nodes(),
                    "n_edges": G.number_of_edges(),
                    "density": round(nx.density(G), 4),
                })

                if path:
                    save_graph_plot(G, path=path, model_name=f"{graph_name}_{algo_name}", trial=trial,
                                    base_dir=output_dir, pos=pos, start=start, goal=goal)

                # if algo_name == "astar" and path:
                #     # Salva il grafo con path
                #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                #     img_path = os.path.join(output_dir, f"{graph_name}_trial{trial_id}_{algo_name}_{timestamp}.png")
                #     save_graph_plot(G,path=path,model_name=graph_name,trial=trial_id, base_dir=output_dir,pos=pos,start=start,goal=goal)


def save_graph_plot(G, path, model_name, trial, base_dir, pos=None, start=None, goal=None):
    os.makedirs(base_dir, exist_ok=True)

    if pos is None:
        if model_name.lower().startswith("gnp"):
            pos = nx.spring_layout(G, seed=42, k=0.6)
        else:
            pos = nx.spring_layout(G, seed=42)

    edge_labels = nx.get_edge_attributes(G, 'weight')

    if model_name.lower().startswith("gnp"):
        isolated = list(nx.isolates(G))
        if isolated:
            G.remove_nodes_from(isolated)
            pos = {node: pos[node] for node in G.nodes()}  # aggiorna layout


    # Colori nodi
    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append("green")
        elif node == goal:
            node_colors.append("red")
        elif path and node in path:
            node_colors.append("orange")
        else:
            node_colors.append("lightgray")

    plt.figure(figsize=(8, 8))

    nx.draw(G, pos, with_labels=False, node_size=100, node_color=node_colors, edge_color='gray')

    # Etichette su archi NON nel path
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
    else:
        path_edges = []

    default_labels = {
        (u, v): w for (u, v), w in edge_labels.items()
        if (u, v) not in path_edges
    }

    nx.draw_networkx_edge_labels(G, pos, edge_labels=default_labels, font_size=6)

    # Archi del path evidenziati
    if path_edges:
        nx.draw_networkx_edges(G, pos,edgelist=path_edges,width=1.5)
        # Etichette del path in rosso e font più grande
        path_labels = {}
        for (u, v) in path_edges:
            if (u, v) in edge_labels:
                path_labels[(u, v)] = edge_labels[(u, v)]
            elif (v, u) in edge_labels:
                path_labels[(v, u)] = edge_labels[(v, u)]

        nx.draw_networkx_edge_labels(G, pos, edge_labels=path_labels, font_size=10)

    plt.title(f"{model_name.upper()} - Trial {trial}", fontsize=10)
    plt.axis("equal")
    filename = os.path.join(base_dir, f"{model_name}_trial_{trial}.png")
    plt.savefig(filename, bbox_inches='tight')
    plt.close()


import os
from datetime import datetime

def generate_multi_algo_graph_plots(G, pos, paths_dict, model_name, trial, base_dir, start, goal):
    """
    Salva:
    - un'immagine per ogni algoritmo con il suo percorso
    - una sola immagine con tutti i percorsi sovrapposti (colori diversi)

    :param G: grafo NetworkX
    :param pos: dizionario posizioni nodi
    :param paths_dict: dict {"algo_name": path}
    :param model_name: nome del grafo
    :param trial: numero del trial
    :param base_dir: directory per salvataggio
    :param start: nodo iniziale
    :param goal: nodo finale
    """
    import matplotlib.pyplot as plt
    import networkx as nx

    os.makedirs(base_dir, exist_ok=True)

    # Colori distinti per i percorsi
    algo_colors = {
        "astar": "orange",
        "bfs": "deepskyblue",
        "dfs": "violet"
    }

    # Immagine unica con percorsi sovrapposti
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=False, node_size=100, node_color='lightgray', edge_color='gray')

    for algo_name, path in paths_dict.items():
        if path:
            edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges, width=2.5, edge_color=algo_colors.get(algo_name, "black"), label=algo_name)

    # Evidenzia start e goal
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='green', node_size=120, label='Start')
    nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color='red', node_size=120, label='Goal')

    plt.title(f"{model_name.upper()} - Trial {trial} - MULTI-PATH", fontsize=10)
    plt.axis("equal")
    plt.legend()
    filename_multi = os.path.join(base_dir, f"{model_name}_trial{trial}_MULTI.png")
    plt.savefig(filename_multi, bbox_inches='tight')
    plt.close()

    # unica immagine per algo
    for algo_name, path in paths_dict.items():
        if not path:
            continue

        plt.figure(figsize=(8, 8))
        nx.draw(G, pos, with_labels=False, node_size=100, node_color='lightgray', edge_color='gray')

        edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=2.5, edge_color=algo_colors.get(algo_name, "black"))

        nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='green', node_size=120)
        nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color='red', node_size=120)

        plt.title(f"{model_name.upper()} - Trial {trial} - {algo_name.upper()}", fontsize=10)
        plt.axis("equal")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(base_dir, f"{model_name}_trial{trial}_{algo_name}_{timestamp}.png")
        plt.savefig(filename, bbox_inches='tight')
        plt.close()



if __name__ == "__main__":
    G, pos = generate_random_grid_graph(10, 10, remove_edge_prob=0.1)
    start, goal = choose_start_and_goal(G, must_be_connected=True)

    run_experiment_from_generator(G, pos, start, goal, graph_name="grid_10x10", output_dir="experiments/grid")
