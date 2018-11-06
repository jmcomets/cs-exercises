import heapq

def rebuild_path(predecessor_map, node, reverse=False):
    path = []
    while node is not None:
        path.append(node)
        node = predecessor_map.get(node)
    if not reverse:
        path.reverse()
    return path

class ComparedBy:
    def __init__(self, wrapped, key):
        self.wrapped = wrapped
        self.key = key

    def __lt__(self, other):
        return self.key(self.wrapped) < other.key(other.wrapped)

def astar(node, neighbors, transition_cost, heuristic, is_goal=lambda node: False):
    """A* algorithm."""
    cost_map = {node: 0}
    predecessor_map = {}
    min_scored = lambda n: ComparedBy((cost_map[n] + heuristic(n), n), key=lambda x: x[0])
    to_visit = [min_scored(node)]
    visited = set()
    while to_visit:
        _, node = heapq.heappop(to_visit).wrapped
        if node in visited:
            continue
        visited.add(node)

        if is_goal(node):
            return rebuild_path(predecessor_map, node)

        for neighbor in neighbors(node):
            neighbor_cost = cost_map[node] + transition_cost(node, neighbor)
            if neighbor_cost < cost_map.get(neighbor, float('infinity')):
                predecessor_map[neighbor] = node
                cost_map[neighbor] = neighbor_cost
                heapq.heappush(to_visit, min_scored(neighbor))

def dijkstra(node, neighbors, transition_cost, is_goal=lambda node: False):
    """Dijkstra's algorithm."""
    return astar(node, neighbors, transition_cost, lambda _: 0, is_goal)

if __name__ == '__main__':
    grid = \
"""
...........
.#.#######.
.#.......#.
.#######.#.
.#.......#.
.#.#######.
.#.......#.
.#######.#.
...........
"""
    grid = [[cell == '.' for cell in row] for row in grid.split('\n') if row]
    w, h = len(grid[0]), len(grid)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    def neighbors(pos):
        for dx, dy in directions:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < w and 0 <= y < h and grid[y][x]:
                yield x, y
    import pprint; pprint.pprint(dijkstra((0, 0), neighbors, lambda _u, _v: 1, lambda pos: pos == (w-1, h-1)))
