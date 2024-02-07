import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances


def get_edges(graph):
    edges = []
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            edges.append((node, neighbor, weight))
    return edges

# Example graph representation (dictionary of dictionaries)
# Define coordinates as variables
coord_A = (0, 0)
coord_B = (1, 1)
coord_C = (0, 1)
coord_D = (1, 2)

# Example graph representation (dictionary of dictionaries)
graph = {
    coord_A: {coord_B: 1, coord_C: 4},
    coord_B: {coord_A: 1, coord_C: 2, coord_D: 5},
    coord_C: {coord_A: 4, coord_B: 2, coord_D: 1},
    coord_D: {coord_B: 5, coord_C: 1}
}

edges = get_edges(graph)
print("Edges of the graph:")
for edge in edges:
    print(edge)