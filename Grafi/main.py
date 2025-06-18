from generate_graph import (
    generate_random_grid_graph,
    generate_random_geometric_graph,
    generate_gnp_graph,
    generate_gnk_graph,
    choose_start_and_goal, get_most_distant_nodes_weighted
)
from build_experiment import run_experiment_from_generator

if __name__ == "__main__":

    trials = 1  # cambia se vuoi più prove
    output_base = "experiments"

    # GRIGLIA
    G_grid, pos_grid = generate_random_grid_graph(10, 10, remove_edge_prob=0.1)
    start, goal = get_most_distant_nodes_weighted(G_grid)
    run_experiment_from_generator(G_grid, pos_grid, start, goal, graph_name="grid_10x10", output_dir=f"{output_base}/grid", num_trials=trials)

    # GRAFO GEOMETRICO
    G_geo, pos_geo = generate_random_geometric_graph(n=50, r=0.25, seed=42)
    start, goal = get_most_distant_nodes_weighted(G_geo)
    run_experiment_from_generator(G_geo, pos_geo, start, goal, graph_name="geo_50", output_dir=f"{output_base}/geo", num_trials=trials)

    # GNP (probabilità p)
    G_gnp, pos_gnp = generate_gnp_graph(n=50, p=0.05)
    start, goal = get_most_distant_nodes_weighted(G_gnp)
    run_experiment_from_generator(G_gnp, pos_gnp, start, goal, graph_name="gnp_50", output_dir=f"{output_base}/gnp", num_trials=trials)

    # GNK (numero fisso di archi)
    G_gnk, pos_gnk = generate_gnk_graph(n=50, k=150)
    start, goal = get_most_distant_nodes_weighted(G_gnk)
    run_experiment_from_generator(G_gnk, pos_gnk, start, goal, graph_name="gnk_50", output_dir=f"{output_base}/gnk", num_trials=trials)
