import math 
from shapely.geometry import LineString
from enum import Enum

class Point_Type(Enum):
    COSTUMER = 1
    PHARMECY = 2
    Regular = 3
class Generic_Figure:
    def __init__(self,color) -> None:
        self.color = color
        self.ref = None


class Point(Generic_Figure):
    def __init__(self,x,y,z=None,color = 'red',size = 25,point_type = Point_Type.Regular) -> None:
        super().__init__(color)
        self.x =x
        self.y =y
        self.z =z
        self.size = size
        self.printed_point_ref = None
        self.type = point_type
    
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
    
    def ls_intersects_line(self, line2):
        # Check if the lines are parallel
        det = (line2.point2.x - line2.point1.x) * (self.point2.y - self.point1.y) - \
            (line2.point2.y - line2.point1.y) * (self.point2.x - self.point1.x)

        # If lines are parallel, they don't intersect
        if det == 0:
            return False, None

        # Calculate intersection point
        s = ((line2.point2.y - line2.point1.y) * (self.point1.x - line2.point1.x) - \
            (line2.point2.x - line2.point1.x) * (self.point1.y - line2.point1.y)) / det
        t = ((self.point2.y - self.point1.y) * (self.point1.x - line2.point1.x) - \
            (self.point2.x - self.point1.x) * (self.point1.y - line2.point1.y)) / det

        # Check if intersection point is within the line segments
        if  ((0 <= s <= 1) and (0 <= t <= 1)):
            intersection_x = self.point1.x + (t * (self.point2.x - self.point1.x))
            intersection_y = self.point1.y + (t * (self.point2.y - self.point1.y))

            return True, Point(intersection_x,intersection_y)
        else: return False, None

            

    
    

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
                return True
        return False
    
    def is_edge_crossing(self,edge:Edge):
        all_squre_points = [
            self.top_left_point,
            Point(self.top_left_point.x,self.bottom_right_point.y),
            self.bottom_right_point,
            Point(self.bottom_right_point.x,self.top_left_point.y)
        ]
        squre_edges: list[Edge] = [
            Edge(all_squre_points[0],all_squre_points[1]),
            Edge(all_squre_points[1],all_squre_points[2]),
            Edge(all_squre_points[2],all_squre_points[3]),
            Edge(all_squre_points[3],all_squre_points[0]),
        ]
        for s_edge in squre_edges:
            is_cut = s_edge.ls_intersects_line(edge)
            if(is_cut[0]):
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