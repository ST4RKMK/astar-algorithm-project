
import networkx as nx
import random
import os
import csv
import time
from astar_graph import astar_graph, manhattan_heuristic, euclidean_heuristic
from researchgraphalgo import bfs, dfs
from generate_graph import (
    generate_random_geometric_graph,
    generate_random_grid_graph,
    generate_gnp_graph,
    generate_gnk_graph,
    get_most_distant_nodes_weighted
)


base_output = "multiexperiments"
os.makedirs(base_output, exist_ok=True)

node_sizes = [25, 50, 100, 200, 300, 500, 1000]
trials_per_n = 3

algos = {
    "astar_null": lambda g, s, t, pos: astar_graph(g, s, t, heuristic=lambda a, b: 0),
    "astar_manhattan": lambda g, s, t, pos: astar_graph(g, s, t, heuristic=manhattan_heuristic, pos=pos),
    "astar_euclidean": lambda g, s, t, pos: astar_graph(g, s, t, heuristic=euclidean_heuristic, pos=pos),
    "bfs": lambda g, s, t, pos: bfs(g, s, t),
    "dfs": lambda g, s, t, pos: dfs(g, s, t),
}

def generate_graph(graph_type, n):
    if graph_type == "geo":
        return generate_random_geometric_graph(n=n, r=0.25)
    elif graph_type == "grid":
        side = int(n**0.5)
        return generate_random_grid_graph(rows=side, cols=side)
    elif graph_type == "gnp":
        return generate_gnp_graph(n=n, p=0.03)
    elif graph_type == "gnk":
        return generate_gnk_graph(n=n, k=int(2*n))

graph_types = ["geo", "grid", "gnp", "gnk"]

# test per ogni tipo di grafo
for graph_type in graph_types:
    for n in node_sizes:
        for trial in range(1, trials_per_n + 1):
            graph_name = f"{graph_type}_{n}"
            output_dir = os.path.join(base_output, graph_type)
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"{graph_name}_results.csv")

            G, pos = generate_graph(graph_type, n)
            graph_dict = {node: [(v, data["weight"]) for v, data in G[node].items()] for node in G.nodes()}
            start, goal = get_most_distant_nodes_weighted(G)

            with open(filename, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "graph", "trial", "algo", "start", "goal", "success",
                    "path_len", "path_cost", "nodes_expanded", "time_sec",
                    "n_nodes", "n_edges", "density"
                ])
                if file.tell() == 0:
                    writer.writeheader()

                for algo_name, func in algos.items():
                    t0 = time.perf_counter()
                    try:
                        path, stats = func(graph_dict, start, goal, pos)
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
                            "density": round(nx.density(G), 4)
                        })
                    except Exception as e:
                        print(f"Errore con {algo_name} su {graph_name} trial {trial}: {e}")
