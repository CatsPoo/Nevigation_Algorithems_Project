import math
from heapq import heappop, heappush
from GraphicalUtils import Point,Edge,Graph

class HeapNode:
    def __init__(self,distamce,point):
        self.distance = distamce
        self.point = point

    def __gt__(self, other):
        return self.distance < other.distance
    
    def __lt__(self,other):
        return self.distance > other.distance


class Dijkstra:
    def __init__(self,graph: Graph,start_point:Point) -> None:
        self.predecessors = None
        self.distances = None
        self.start_point:Point = start_point
        self.graph:Graph = graph
          
    def run(self):
        self.distances = {point: math.inf for point in self.graph.points}
        self.predecessors = {point: None for point in self.graph.points}
        self.distances[self.start_point] = 0
        visited = set()
        queue = [HeapNode(0,self.start_point)]

        while queue:
            node  = heappop(queue)
            current_distance = node.distance
            current_point = node.point

            if current_point in visited:
                continue
            visited.add(current_point)

            for edge in self.graph.get_point_neighbors(current_point):
                neighbor = edge.point2
                new_distance = self.distances[current_point] + edge.length()
                if new_distance < self.distances[neighbor]:
                    self.distances[neighbor] = new_distance
                    self.predecessors[neighbor] = current_point
                    heappush(queue, HeapNode(new_distance, neighbor))
    
    def get_shortest_path(self,end_point:Point) ->list[Point]:
        if(self.distances == None or self.predecessors==None): return None
        if(end_point not in self.graph.points): return None

        path = []
        current_point = end_point
        while current_point is not None:
            path.append(current_point)
            current_point = self.predecessors[current_point]
        
        return path[::-1]