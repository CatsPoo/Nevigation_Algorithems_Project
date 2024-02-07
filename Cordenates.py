class Point:
    def __init__(self,x,y,color = 'red') -> None:
        self.x =x
        self.y =y
        self.color = color
    
    def __str__(self) -> str:
        return '('+str(self.x)+','+str(self.y)+')'

class Edge:
     def __init__(self,point1:Point,point2:Point,color = 'blue') -> None:
          self.point1 = point1
          self.point2 = point2
          self.color = color


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