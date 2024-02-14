import math 

class Point:
    def __init__(self,x,y,z=None,color = 'red') -> None:
        self.x =x
        self.y =y
        self.z =z
        self.color = color
    
    def __str__(self) -> str:

        return f'({self.x},{self.y})'

class Edge:
    def __init__(self,point1:Point,point2:Point,color = 'blue') -> None:
          self.point1 = point1
          self.point2 = point2
          self.color = color

    def __len__(self):
        return math.sqrt(
            ((self.point1.z ** 2 - self.point2.z ** 2)**2) +
            ((self.point1.x ** 2 - self.point2.x ** 2) **2) +
            ((self.point1.y ** 2 - self.point2.y ** 2)**2)
        )


class Graph:
    def __init__(self,points =[],edges=[]) -> None:
        self.points:list = points
        self.edges:list = edges

    def add_point(self,point):
        self.points.append(point)
    
    def add_points(self,points:list):
        for p in points:
            self.add_point(p)
    
    def add_edge(self,edge):
        self.edges.append(edge)

    def add_adges(self,edges):
        for e in edges:
            self.add_edge(e)




def real_to_map_index(real_coord:Point, array_origin:Point, map_size:Point, array_size:Point) -> Point:
        # Calculate the difference between the real coordinate and the array origin
    delta_x = real_coord.x - array_origin.x
    delta_y = real_coord.y - array_origin.y


    # Convert the difference to array indices based on resolution
    index_x = int(map_size.x/array_size.x) * delta_x
    index_y = int(map_size.y/array_size.y) * delta_y

    # Ensure the indices are within the array bounds
    index_x = max(0, min(index_x, array_size.x - 1))
    index_y = max(0, min(index_y, array_size.y - 1))

    return Point(index_x, index_y)


def map_value(value, in_min, in_max, out_min, out_max):
    # Map value from the input range to the output range
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min