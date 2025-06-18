from collections import deque

def bfs(graph, start, goal):
    queue = deque()
    visited = set()
    parent_map = {}

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            path = [current]
            while current in parent_map:
                current = parent_map[current]
                path.append(current)
            path.reverse()
            return path, {
                "nodi_espansi": len(visited),
                "lunghezza_percorso": len(path)
            }

        for neighbor, _ in graph.get(current, []):  # ignora i pesi
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current
                queue.append(neighbor)

    return None, {
        "nodi_espansi": len(visited),
        "lunghezza_percorso": 0
    }

def dfs(graph, start, goal):
    stack = []
    visited = set()
    parent_map = {}

    stack.append(start)

    while stack:
        current = stack.pop()

        if current == goal:
            path = [current]
            while current in parent_map:
                current = parent_map[current]
                path.append(current)
            path.reverse()
            return path, {
                "nodi_espansi": len(visited),
                "lunghezza_percorso": len(path)
            }

        if current not in visited:
            visited.add(current)
            for neighbor, _ in graph.get(current, []):
                if neighbor not in visited:
                    parent_map[neighbor] = current
                    stack.append(neighbor)

    return None, {
        "nodi_espansi": len(visited),
        "lunghezza_percorso": 0
    }
