from datetime import datetime
import math
import os
import time
import csv
import random

import networkx as nx
from matplotlib import pyplot as plt

from graph_map import get_furthest_nodes
from researchgraphalgo import bfs, dfs
from astar_graph import astar_graph, draw_graph, generate_weighted_graph

from experimental_graph import generate_experimental_graph, get_longest_shortest_path


def zero_heuristic(a, b):  # comportamento tipo Dijkstra
    return 0

def manhattan_heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def nx_to_dict(G):
    graph_dict = {node: [] for node in G.nodes()}
    for u, v, data in G.edges(data=True):
        graph_dict[u].append((v, data.get("weight", 1)))
    return graph_dict

def run_experimental(filename="results_astar_comparison.csv", num_trials=5):
    models = [
        ("gnp", {"n": 50, "p": 0.05}),
        ("gnk", {"n": 50, "k": 150}),
        ("grid", {"n": 10, "m": 10}),
        ("geo", {"n": 50, "delta": 0.25}),
    ]

    with open(filename, mode="w", newline="") as csvfile:
        fieldnames = ["model", "trial", "n", "m_or_k_or_p", "success", "path_len", "nodes_expanded", "time_sec"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_dir = os.path.join("plots_graph", timestamp)
        os.makedirs(plot_dir, exist_ok=True)

        for model_name, params in models:
            for trial in range(1, num_trials + 1):
                # Genera grafo
                G = generate_experimental_graph(model=model_name, **params)
                graph_dict = nx_to_dict(G)

                nodes = list(G.nodes())
                #start = random.choice(nodes)
                #goal = random.choice([n for n in nodes if n != start])

                pos = G.graph.get("pos", nx.spring_layout(G, seed=42))
                start, goal = get_longest_shortest_path(G) if model_name != "grid" else get_furthest_nodes(pos)

                start_time = time.perf_counter()
                path, stats = astar_graph(graph_dict, start, goal, zero_heuristic)
                end_time = time.perf_counter()

                writer.writerow({
                    "model": model_name,
                    "trial": trial,
                    "n": params.get("n", "-"),
                    "m_or_k_or_p": params.get("m", params.get("k", params.get("p", params.get("delta", "-")))),
                    "success": "yes" if path else "no",
                    "path_len": stats["lunghezza_percorso"],
                    "nodes_expanded": stats["nodi_espansi"],
                    "time_sec": round(end_time - start_time, 6),
                })

                print(f"[✓] {model_name.upper()} trial {trial} completato.")
                if trial == 1:
                    draw_graph(G, path, title=f"{model_name.upper()} - Trial {trial}")
                    save_graph_plot(G, path, model_name=model_name, trial=trial, base_dir=plot_dir)


def run_experiments(filename="results_astar_bfs_dfs.csv", num_trials=5):
    models = [
        ("gnp", {"n": 50, "p": 0.05}),
        ("gnk", {"n": 50, "k": 150}),
        ("grid", {"n": 10, "m": 10}),
        ("geo", {"n": 50, "delta": 0.25}),
    ]

    with open(filename, mode="w", newline="") as csvfile:
        fieldnames = ["model", "trial", "n", "m_or_k_or_p", "algo", "success", "path_len", "nodes_expanded", "time_sec", "path_cost"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_plot_dir = f"plots_graph/{timestamp}"
        os.makedirs(base_plot_dir, exist_ok=True)

        for model_name, params in models:
            for trial in range(1, num_trials + 1):
                G = generate_experimental_graph(model=model_name, **params)
                graph_dict = nx_to_dict(G)
                nodes = list(G.nodes())
                start = random.choice(nodes)
                goal = random.choice([n for n in nodes if n != start])

                for algo_name, algo_func in [
                    ("astar", lambda g, s, t: astar_graph(g, s, t, zero_heuristic)),
                    ("bfs", bfs),
                    ("dfs", dfs)
                ]:
                    start_time = time.perf_counter()
                    path, stats = algo_func(graph_dict, start, goal)
                    end_time = time.perf_counter()

                    writer.writerow({
                        "model": model_name,
                        "trial": trial,
                        "n": params.get("n", "-"),
                        "m_or_k_or_p": params.get("m", params.get("k", params.get("p", params.get("delta", "-")))),
                        "algo": algo_name,
                        "success": "yes" if path else "no",
                        "path_len": stats["lunghezza_percorso"],
                        "nodes_expanded": stats["nodi_espansi"],
                        "time_sec": round(end_time - start_time, 6),
                        "path_cost": stats.get("path_cost", 0)
                    })

                    print(f"[✓] {model_name.upper()} | Trial {trial} | {algo_name.upper()}")

                # Mostra solo 1 grafico A*
                if trial == 1:
                    save_graph_plot(G, path, model_name, trial, base_plot_dir)



def save_graph_plot(G, path, model_name, trial, base_dir):
    from matplotlib import pyplot as plt
    import networkx as nx
    import os


    os.makedirs(base_dir, exist_ok=True)


    pos = nx.spring_layout(G, seed=42, k=2)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(7, 7))
    nx.draw(G, pos, with_labels=True, node_size=600, node_color='lightgray', font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')

    plt.title(f"{model_name.upper()} - Trial {trial}", fontsize=10)
    plt.axis('off')
    plt.tight_layout()
    filename = os.path.join(base_dir, f"{model_name}_trial_{trial}.png")
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def run_custom_graph_experiment(filename="results_custom_graphs.csv", num_trials=3, sizes=[(50, 200), (100, 500)]):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_dir = f"plots_graph_custom/{timestamp}"
    os.makedirs(plot_dir, exist_ok=True)

    with open(filename, mode="w", newline="") as f:
        fieldnames = [
            "trial", "n_nodes", "n_edges", "algo", "success",
            "path_len", "path_cost", "nodes_expanded", "time_sec"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for n_nodes, n_edges in sizes:
            for trial in range(1, num_trials + 1):
                G = generate_weighted_graph(n_nodes, n_edges)
                graph_dict = nx_to_dict(G)
                nodes = list(G.nodes())
                start = random.choice(nodes)
                goal = random.choice([n for n in nodes if n != start])

                for algo_name, algo_func in [
                    ("astar", lambda g, s, t: astar_graph(g, s, t, zero_heuristic)),
                    ("bfs", bfs),
                    ("dfs", dfs)
                ]:
                    start_time = time.perf_counter()
                    path, stats = algo_func(graph_dict, start, goal)
                    end_time = time.perf_counter()

                    writer.writerow({
                        "trial": trial,
                        "n_nodes": n_nodes,
                        "n_edges": n_edges,
                        "algo": algo_name,
                        "success": "yes" if path else "no",
                        "path_len": stats["lunghezza_percorso"],
                        "path_cost": stats.get("path_cost", 0),
                        "nodes_expanded": stats["nodi_espansi"],
                        "time_sec": round(end_time - start_time, 6)
                    })

                    if trial == 1 and algo_name == "astar":
                        save_graph_plot(G, path, model_name=f"{n_nodes}_{n_edges}", trial=trial, base_dir=plot_dir)


