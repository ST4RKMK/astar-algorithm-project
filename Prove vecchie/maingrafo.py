import random
import time

from experiment_astar_graph import run_experimental, run_experiments, run_custom_graph_experiment
from astar_graph import astar_graph, draw_graph, generate_weighted_graph, nx_to_dict, draw_cgraph
from experimental_graph import generate_experimental_graph


def heuristic(a, b):
    # Esempio euristica semplice (zero = Dijkstra)
    return 0
#######################################################
# graph = {
#     'A': [('B', 1), ('C', 4)],
#     'B': [('C', 2), ('D', 5)],
#     'C': [('D', 1), ('E', 3)],
#     'D': [('F', 2)],
#     'E': [('F', 1)],
#     'F': []
# }
#
# path = astar_graph(graph, 'A', 'F', heuristic)
# print("Percorso trovato:", path)
#
# draw_graph(graph, path)

##########################################################################
# Parametri esperimento
# n_nodes = 20
# n_edges = 30
#
# # Genera grafo
# G = generate_weighted_graph(n_nodes, n_edges)
# graph_dict = nx_to_dict(G)
#
# # Scelta casuale di start/goal
# nodes = list(graph_dict.keys())
# start = random.choice(nodes)
# goal = random.choice([n for n in nodes if n != start])
#
# print(f"Start: {start}, Goal: {goal}")
#
# start_time = time.perf_counter()
# path = astar_graph(graph_dict, start, goal, heuristic)
# end_time = time.perf_counter()
#
# print("Percorso trovato:" if path else "Nessun percorso trovato.")
# print("Path:", path)
# print(f"Tempo di esecuzione: {end_time - start_time:.6f} secondi")
#
# draw_cgraph(G, path)
##########################################################


# import matplotlib.pyplot as plt
# import networkx as nx
#
# # G(n,p)
# G = generate_experimental_graph(model="gnp", n=50, p=0.1)
# nx.draw_spring(G, with_labels=True, node_size=400)
# plt.title("Grafo G(n,p)")
# plt.show()
#
#
# # Grafo di prossimità geometrica P(n, δ)
# G_geo = generate_experimental_graph(model="geo", n=40, delta=0.25)
# nx.draw(G_geo, pos=nx.get_node_attributes(G_geo, 'pos'), with_labels=True)
# plt.title("Grafo geometrico P(n, δ)")
# plt.show()
#################################################################

#run_experiments()
run_experimental()

#####################################################################

# n_nodes = 20
# n_edges = 30
#
# # Genera grafo
# G = generate_weighted_graph(n_nodes, n_edges)
# draw_graph(G)

#run_custom_graph_experiment(filename="results_custom.csv",num_trials=5,sizes=[(50, 200), (100, 400), (200, 800)])
