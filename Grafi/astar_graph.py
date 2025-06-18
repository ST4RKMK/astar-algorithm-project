import heapq
import math
import random

import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id, parent=None):
        self.id = id
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.f < other.f

def zero_heuristic(a, b):  # comportamento tipo Dijkstra
    return 0

def manhattan_heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def astar_graph(graph, start_id, goal_id, heuristic, pos=None):
    start_node = Node(start_id)
    goal_node = Node(goal_id)

    open_list = []
    closed_set = set()

    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current = heapq.heappop(open_list)

        if current.id == goal_node.id:
            path = []
            cost = 0
            while current:
                path.append(current.id)
                if current.parent:
                    for neighbor, weight in graph[current.parent.id]:
                        if neighbor == current.id:
                            cost += weight
                            break
                current = current.parent
            path = path[::-1]

            return path, {
                "nodi_espansi": len(closed_set),
                "lunghezza_percorso": len(path),
                "path_cost": cost
            }

        closed_set.add(current.id)

        for neighbor_id, cost in graph[current.id]:
            if neighbor_id in closed_set:
                continue

            neighbor = Node(neighbor_id, current)
            neighbor.g = current.g + cost
            neighbor.h = heuristic(pos[neighbor_id], pos[goal_id]) if pos else heuristic(neighbor_id, goal_id)
            neighbor.f = neighbor.g + neighbor.h

            if any(n.id == neighbor.id and n.f <= neighbor.f for _, n in open_list):
                continue

            heapq.heappush(open_list, (neighbor.f, neighbor))

    return None, {
        "nodi_espansi": len(closed_set),
        "lunghezza_percorso": 0,
        "path_cost": 0
    }  # no path found


