# grid_map.py
import math


class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent

        self.g = 0  # costo dal nodo iniziale
        self.h = 0  # euristica (es. distanza Manhattan)
        self.f = 0  # costo totale

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

# astar.py
from heapq import heappush, heappop

def heuristic(a, b):
    # distanza di Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def zero_heuristic(a, b):
    return 0

def manhattan_heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def aggressive_manhattan(a, b):
    return 2.5 * (abs(a[0] - b[0]) + abs(a[1] - b[1]))


def astar(grid, start, goal):
    start_node = Node(start)
    goal_node = Node(goal)

    open_list = []
    closed_set = set()

    heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current = heappop(open_list)
        print(f"[INFO] Espansione nodo: {current.position} | g={current.g} h={current.h} f={current.f}")

        if current == goal_node:
            # ricostruisci il path
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            path= path[::-1]
            return path, {
                "nodi_espansi": len(closed_set),
                "lunghezza_percorso": len(path)
            }
            # reverse

        closed_set.add(current.position)

        for neighbor in get_neighbors(current, grid):
            if neighbor.position in closed_set:
                continue

            neighbor.g = current.g + 1
            neighbor.h = heuristic(neighbor.position, goal_node.position)
            neighbor.f = neighbor.g + neighbor.h

            # evita duplicati peggiori
            if any(n.position == neighbor.position and n.f <= neighbor.f for _, n in open_list):
                continue

            heappush(open_list, (neighbor.f, neighbor))
            print(f"  ↳ Considero vicino: {neighbor.position} | g={neighbor.g} h={neighbor.h} f={neighbor.f}")

    return None, {
        "nodi_espansi": len(closed_set),
        "lunghezza_percorso": 0
    }
    # Nessun percorso trovato

def astarh(grid, start, goal, heuristic):
    start_node = Node(start)
    goal_node = Node(goal)

    open_list = []
    closed_set = set()
    nodes_generated = 0
    open_list_max = 1

    heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current = heappop(open_list)
        print(f"[INFO] Espansione nodo: {current.position} | g={current.g} h={current.h} f={current.f}")

        if current == goal_node:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            path = path[::-1]
            return path, {
                "nodi_espansi": len(closed_set),
                "lunghezza_percorso": len(path),
                "nodes_generated": nodes_generated,
                "open_list_max": open_list_max
            }

        closed_set.add(current.position)

        for neighbor in get_neighbors(current, grid):
            if neighbor.position in closed_set:
                continue

            neighbor.g = current.g + 1
            neighbor.h = heuristic(neighbor.position, goal_node.position)
            neighbor.f = neighbor.g + neighbor.h

            if any(n.position == neighbor.position and n.f <= neighbor.f for _, n in open_list):
                continue

            heappush(open_list, (neighbor.f, neighbor))
            nodes_generated += 1
            open_list_max = max(open_list_max, len(open_list))
            print(f"  ↳ Considero vicino: {neighbor.position} | g={neighbor.g} h={neighbor.h} f={neighbor.f}")

    return None, {
        "nodi_espansi": len(closed_set),
        "lunghezza_percorso": 0,
        "nodes_generated": nodes_generated,
        "open_list_max": open_list_max
    }


def get_neighbors(node, grid):
    neighbors = []
    x, y = node.position
    rows, cols = len(grid), len(grid[0])

    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
            neighbors.append(Node((nx, ny), node))
    return neighbors
