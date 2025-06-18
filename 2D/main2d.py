# main2d.py
import time

from astar2D import astar
from csvsave import run_experiments_csv
from plot_grid import plot_grid, generate_random_grid
from multipletest import multipletest, run_heuristic_experiment, run_non_heuristic_experiment

# #0 = libero, 1 = ostacolo
# grid = [
#     [0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0]
# ]
# start = (0, 0)
# goal = (3, 4)
#
# start_time = time.time()
# path = astar(grid, start, goal)
# end_time = time.time()
#
# print("Percorso trovato:")
# print(path)
# print("Tempo di esecuzione:", end_time - start_time, "secondi")

################################################################
# rows, cols = 10, 10
# grid = generate_random_grid(rows, cols, obstacle_prob=0.3)
# start = (0, 0)
# goal = (rows - 1, cols - 1)
# grid[start[0]][start[1]] = 0
# grid[goal[0]][goal[1]] = 0
#
# start_time = time.time()
# path, stats = astar(grid, start, goal)
# end_time = time.time()
#
# print("Percorso trovato:")
# print(path)
# print("Tempo di esecuzione:", end_time - start_time, "secondi")
#
# print("→ Statistiche:")
# for k, v in stats.items():
#     print(f"  {k}: {v}")
#
# plot_grid(grid, path, start, goal)

########################################################################

#multipletest()

#############################################################

#run_experiments_csv("risultati_astar.csv", num_tests=50, size=(20, 20), obstacle_prob=0.25)
#############################################################
#run_heuristic_experiment("results_20x20.csv",10,(20,20),0.2)
#run_heuristic_experiment(filename="results_50x50.csv", num_trials=5, grid_size=(50,50), obstacle_prob=0.2)
#run_heuristic_experiment(filename="results_100x100.csv", num_trials=5, grid_size=(100,100), obstacle_prob=0.2)

#run_heuristic_experiment(filename="results_200x200.csv", num_trials=5, grid_size=(200,200), obstacle_prob=0.2)

#run_non_heuristic_experiment(filename="results_non_heuristic_200x200.csv", num_trials=5, grid_size=(200,200), obstacle_prob=0.2)

run_non_heuristic_experiment(filename="results_non_heuristic_300x300.csv", num_trials=5, grid_size=(300,300), obstacle_prob=0.2)