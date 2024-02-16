import math 

class Generic_Figure:
    def __init__(self,color) -> None:
        self.color = color
        self.ref = None


class Point(Generic_Figure):
    def __init__(self,x,y,z=None,color = 'red',size = 25) -> None:
        super().__init__(color)
        self.x =x
        self.y =y
        self.z =z
        self.size = size
        self.printed_point_ref = None
    
    def __str__(self) -> str:

        return f'({self.x},{self.y})'

class Edge(Generic_Figure):
    def __init__(self,point1:Point,point2:Point,color = 'blue',thickness=1) -> None:
          super().__init__(color)
          self.point1 = point1
          self.point2 = point2
          self.thickness = thickness

    def __len__(self):
        return math.sqrt(
            ((self.point1.z ** 2 - self.point2.z ** 2)**2) +
            ((self.point1.x ** 2 - self.point2.x ** 2) **2) +
            ((self.point1.y ** 2 - self.point2.y ** 2)**2)
        )
    
    def __str__(self) -> str:
        return f'Point 1: {str(self.point1)}, Point 2: {str(self.point2)}'


class Graph:
    def __init__(self,points =[],edges=[]) -> None:
        self.points:list[Point] = points
        self.edges:list[Edge] = edges

    def add_point(self,point):
        self.points.append(point)
    
    def add_points(self,points:list):
        self.points.extend(points)
    
    def add_edge(self,edge):
        self.edges.append(edge)

    def add_adges(self,edges):
        self.edges.extend(edges)


class Square:
    def __init__(self,top_left_point,bottm_right_point,color = 'red',facecolor=(1, 0, 0, 0.3)) -> None:
        self.top_left_point:Point = top_left_point
        self.bottom_right_point:Point = bottm_right_point
        self.color = color
        self.facecolor = facecolor

    def is_inside(self,point:Point):
        if( point.x <= self.top_left_point.x and point.x >= self.bottom_right_point.x):
            if(point.y >= self.top_left_point.y and point.y <= self.bottom_right_point.y):
                if(self.top_left_point.x ==32 and self.top_left_point.y == 34.92):
                    print('0000000000000000000')
                return True
        return False

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