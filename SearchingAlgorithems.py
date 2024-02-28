import math
from heapq import heappop, heappush
from GraphicalUtils import Point,Edge,Graph
import numpy as np

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
    

class Node:
    def __init__(self, parent=None, position:Point=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f
    
class A_STAR:
    def __init__(self,maze,start:Point,end:Point) -> None:
        self.start_node = Node(None,start)
        self.end_node = Node(None,end)
        self.maze = maze
        self.path :list[Point] = None

        # Initialize open and closed lists
        self.open_list = []
        self.closed_list = []

        heappush(self.open_list, self.start_node)
    
    def run(self):
        while self.open_list:
            current_node:Node= heappop(self.open_list)
            self.closed_list.append(current_node)

            if current_node == self.end_node:
                path = []
                while current_node is not None:
                    path.append(current_node.position)
                    current_node = current_node.parent
                self.path =  path[::-1]  # Return reversed path
            

            # Generate children
            children:list[Node] = []
            for new_position in [(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]:  # Adjacent squares
                # Get node position
                node_position = current_node.position + new_position

                # Make sure within range
                if node_position.x > (len(self.maze) - 1) or node_position.x < 0 or node_position.y > (len(self.maze[len(self.maze)-1]) -1) or node_position.y < 0:
                    continue

                # Make sure walkable terrain
                if self.maze[node_position.x][node_position.y] == np.nan:
                    continue

                if(not node_position.z): continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)
            
            # Loop through children
            for child in children:
                # Child is on the closed list
                if any(child == closed_child for closed_child in self.closed_list):
                    continue

                # Create the f, g, and h values
                print('$$$$$')
                child.g = current_node.g + 1
                child.h = Edge(child.position,self.end_node.position).length()
                child.f = child.g + child.h

                # Child is already in the open list
                if any(child == open_node for open_node in self.open_list):
                    continue

                # Add the child to the open list
                heappush(self.open_list, child)
                 # No path found
        self.path =  None




