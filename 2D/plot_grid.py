import os
import random

from matplotlib import pyplot as plt
from datetime import datetime

def plot_grid(grid, path, start, goal):
    grid = [row[:] for row in grid]  # copia
    if path:
        for x, y in path:
            if (x, y) != start and (x, y) != goal:
                grid[x][y] = 0.5  # colore del path


    if start:
        grid[start[0]][start[1]] = 0.25
    if goal:
        grid[goal[0]][goal[1]] = 0.75

    plt.imshow(grid, cmap='gray_r')
    plt.title("A* path" if path else "A* fallito")
    plt.axis('off')
    plt.show()

def generate_random_grid(rows, cols, obstacle_prob=0.2):
    return [
        [1 if random.random() < obstacle_prob else 0 for _ in range(cols)]
        for _ in range(rows)
    ]

# def save_plot_grid(grid, path, start, goal, trial, heuristic, grid_size, timestamp, base_dir="plots"):
#     rows, cols = grid_size
#     subfolder = f"{rows}x{cols}_{timestamp}"
#     save_dir = os.path.join(base_dir, subfolder)
#     os.makedirs(save_dir, exist_ok=True)
#
#     grid = [row[:] for row in grid]  # copia
#
#     if path:
#         for x, y in path:
#             if (x, y) != start and (x, y) != goal:
#                 grid[x][y] = 0.5
#     grid[start[0]][start[1]] = 0.25
#     grid[goal[0]][goal[1]] = 0.75
#
#     plt.figure(figsize=(5, 5))
#     plt.imshow(grid, cmap='gray_r')
#     title = f"Trial {trial} | Euristica: {heuristic} | {'Successo' if path else 'Fallito'}"
#     plt.title(title, fontsize=10)
#     plt.axis('off')
#
#     filename = f"{save_dir}/trial_{trial}_{heuristic}_{'success' if path else 'fail'}.png"
#     plt.tight_layout()
#     plt.savefig(filename)
#     plt.close()

def save_plot_grid(grid, path, start, goal, trial, heuristic, grid_size, timestamp, base_dir="plots"):

    rows, cols = grid_size
    subfolder = f"{rows}x{cols}_{timestamp}"
    save_dir = os.path.join(base_dir, subfolder)
    os.makedirs(save_dir, exist_ok=True)

    grid_copy = [row[:] for row in grid]

    # Base map
    plt.figure(figsize=(6, 6))
    plt.imshow(grid_copy, cmap='gray_r', origin='upper')

    # Disegna path (in rosso)
    if path:
        px, py = zip(*path)
        plt.plot(py, px, color='red', linewidth=1.0, label="Percorso A*")

    # Start e Goal
    if start:
        plt.scatter(start[1], start[0], c='green', marker='o', s=30, label='Start')
    if goal:
        plt.scatter(goal[1], goal[0], c='blue', marker='x', s=30, label='Goal')

    title = f"Trial {trial} | Euristica: {heuristic} | {'Successo' if path else 'Fallito'}"
    plt.title(title, fontsize=10)
    plt.axis('off')
    plt.tight_layout()

    filename = f"{save_dir}/trial_{trial}_{heuristic}_{'success' if path else 'fail'}.png"
    plt.savefig(filename)
    plt.close()


