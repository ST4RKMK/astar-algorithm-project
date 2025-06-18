import csv
import time
from astar2D import astar
from plot_grid import generate_random_grid



def run_experiments_csv(filename, num_tests=20, size=(10, 10), obstacle_prob=0.2):
    rows, cols = size

    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['test_id', 'rows', 'cols', 'obstacle_prob', 'found_path', 'path_length', 'nodes_expanded', 'time_sec']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, num_tests + 1):
            grid = generate_random_grid(rows, cols, obstacle_prob)
            grid[0][0] = 0
            grid[rows - 1][cols - 1] = 0
            start, goal = (0, 0), (rows - 1, cols - 1)

            start_time = time.perf_counter()
            path, stats = astar(grid, start, goal)
            end_time = time.perf_counter()

            writer.writerow({
                'test_id': i,
                'rows': rows,
                'cols': cols,
                'obstacle_prob': obstacle_prob,
                'found_path': 'yes' if path else 'no',
                'path_length': stats['lunghezza_percorso'],
                'nodes_expanded': stats['nodi_espansi'],
                'time_sec': round(end_time - start_time, 6)
            })

            print(f" Test {i}/{num_tests} completato.")
