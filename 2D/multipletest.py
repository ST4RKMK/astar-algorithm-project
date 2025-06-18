import csv
import time
from datetime import datetime

from astar2D import astar, zero_heuristic, manhattan_heuristic, euclidean_heuristic, astarh, aggressive_manhattan
from plot_grid import generate_random_grid, plot_grid, save_plot_grid


def multipletest():
    for i in range(5):
        rows, cols = 10, 10
        grid = generate_random_grid(rows, cols, obstacle_prob=0.2)
        start = (0, 0)
        goal = (rows - 1, cols - 1)
        grid[start[0]][start[1]] = 0
        grid[goal[0]][goal[1]] = 0
        grid[0][0] = 0
        grid[9][9] = 0
        start_time = time.time()
        path, stats = astar(grid, (0, 0), (9, 9))
        end_time = time.time()
        print(f"Test {i + 1} eseguito in {end_time - start_time} secondi:")
        print(f"  Lunghezza: {stats['lunghezza_percorso']}, Nodi espansi: {stats['nodi_espansi']}")
        print(f"  Riuscito: {'SI' if path else 'NO'}\n")
        plot_grid(grid, path, start, goal)
        print("→ Statistiche:")
        for k, v in stats.items():
            print(f"  {k}: {v}")


def run_heuristic_experiment(filename="results_heuristics.csv", num_trials=10, grid_size=(20, 20), obstacle_prob=0.2):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rows, cols = grid_size
    heuristics = {
        "zero": zero_heuristic,
        "manhattan": manhattan_heuristic,
        "euclidean": euclidean_heuristic,
    }

    with open(filename, mode="w", newline="") as file:
        fieldnames = [
            "trial", "heuristic", "success", "path_len", "nodes_expanded",
            "nodes_generated", "open_list_max", "time_sec"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for trial in range(1, num_trials + 1):
            grid = generate_random_grid(rows, cols, obstacle_prob)
            start = (0, 0)
            goal = (rows - 1, cols - 1)
            grid[start[0]][start[1]] = 0
            grid[goal[0]][goal[1]] = 0


            for h_name, h_func in heuristics.items():
                start_time = time.perf_counter()
                path, stats = astarh(grid, start, goal, heuristic=h_func)
                end_time = time.perf_counter()
                save_plot_grid(grid, path, start, goal, trial, h_name, grid_size, timestamp)

                writer.writerow({
                    "trial": trial,
                    "heuristic": h_name,
                    "success": "yes" if path else "no",
                    "path_len": stats["lunghezza_percorso"],
                    "nodes_expanded": stats["nodi_espansi"],
                    "nodes_generated": stats["nodes_generated"],
                    "open_list_max": stats["open_list_max"],
                    "time_sec": round(end_time - start_time, 6)

                })

                print(f" Trial {trial} | {h_name} → {'Successo' if path else 'Fallito'}")


def run_non_heuristic_experiment(filename="results_heuristics.csv", num_trials=10, grid_size=(20, 20), obstacle_prob=0.2):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rows, cols = grid_size
    heuristics = {
        "zero": zero_heuristic,
        "manhattan": manhattan_heuristic,
        "euclidean": euclidean_heuristic,
        "aggressive": aggressive_manhattan
    }

    with open(filename, mode="w", newline="") as file:
        fieldnames = [
            "trial", "heuristic", "success", "path_len", "nodes_expanded",
            "nodes_generated", "open_list_max", "time_sec"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for trial in range(1, num_trials + 1):
            grid = generate_random_grid(rows, cols, obstacle_prob)
            start = (0, 0)
            goal = (rows - 1, cols - 1)
            grid[start[0]][start[1]] = 0
            grid[goal[0]][goal[1]] = 0


            for h_name, h_func in heuristics.items():
                start_time = time.perf_counter()
                path, stats = astarh(grid, start, goal, heuristic=h_func)
                end_time = time.perf_counter()
                save_plot_grid(grid, path, start, goal, trial, h_name, grid_size, timestamp)

                writer.writerow({
                    "trial": trial,
                    "heuristic": h_name,
                    "success": "yes" if path else "no",
                    "path_len": stats["lunghezza_percorso"],
                    "nodes_expanded": stats["nodi_espansi"],
                    "nodes_generated": stats["nodes_generated"],
                    "open_list_max": stats["open_list_max"],
                    "time_sec": round(end_time - start_time, 6)

                })

                print(f" Trial {trial} | {h_name} → {'Successo' if path else 'Fallito'}")