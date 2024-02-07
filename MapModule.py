
import numpy as np
import matplotlib.pyplot as plt
from cartopy.io import srtm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import rasterio
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from rasterio.plot import show
from Cordenates import Point,real_to_map_index
import os


class Map:
    def __init__(self,bounds,heights,points = [], edges = []) -> None:
        self.bounds = bounds
        self.heights = heights
        
        self.marked_points = points
        self.marked_edges = edges

        self.map_heights= (self.bounds[3]-self.bounds[1])
        self.map_width = (self.bounds[2]-self.bounds[0])
        
        self.resulution = 1/3000
        self.map_orgin = Point(self.bounds[0],self.bounds[1])
        #BoundingBox(left=34.99986111111111, bottom=29.999861111111112, right=36.000138888888884, top=31.00013888888889)

    def get_top_left_corner(self):
        return Point(self.bounds[3],self.bounds[0])
    
    def get_bottomn_right_corner(self):
        return Point(self.bounds[1],self.bounds[2])
    

    def crop(self,top_left_point:Point = None,bottom_right_point:Point = None):
        if(not top_left_point):
            top_left_point = self.get_top_left_corner()
        if(not bottom_right_point):
            bottom_right_point = self.get_bottomn_right_corner()
        
        top_left_map_index :Point = real_to_map_index(top_left_point,self.map_orgin,Point(self.map_width,self.map_heights),Point(len(self.heights[0]),len(self.heights)))
        bottom_right_point_map_index: Point = real_to_map_index(bottom_right_point,self.map_orgin,Point(self.map_width,self.map_heights),Point(len(self.heights[0]),len(self.heights)))

        cropped_bounds = [bottom_right_point.x,top_left_point.y,top_left_point.x,bottom_right_point.y]
        cropped_heights = [] 

        print(cropped_bounds)
        print('@@@')
        print(top_left_map_index)
        print(len(self.heights))
        print(len(self.heights[0]))

        for row in self.heights.copy()[top_left_map_index.y:]:#bottom_right_point_map_index.y]:
            cropped_heights.append(row)#[top_left_map_index.x:bottom_right_point_map_index.x])

        return Map(cropped_bounds,cropped_heights)


        
def get_map_info(tlf_file) -> Map:
    src = rasterio.open(tlf_file)
    return Map(src.bounds, src.read()[0][::-1])


def merge_horizontal_maps(left_map:Map,right_map:Map) ->Map:
    new_heights = []
    for i in range(left_map.heights.shape[0]):
        new_row = []
        new_row.extend(left_map.heights[i])
        new_row.extend(right_map.heights[i])
        new_heights.append(new_row)
    new_bounds = [left_map.bounds[0],left_map.bounds[1],right_map.bounds[2],left_map.bounds[3]]
    return Map(new_bounds,new_heights)

def merge_verticaly_maps(top_map,bottom_map) ->Map:
    new_heights = bottom_map.heights.copy().extend(top_map.heights.copy())
    new_bounds = [top_map.bounds[0],bottom_map.bounds[1],top_map.bounds[2],top_map.bounds[3]]
    return Map(new_bounds,top_map.heights)


def get_full_israel_map() -> Map:
    m1= get_map_info('./maps/n29_e034_1arc_v3.tif')
    m2= get_map_info('./maps/n29_e035_1arc_v3.tif')

    m3= get_map_info('./maps/n30_e034_1arc_v3.tif')
    m4= get_map_info('./maps/n30_e035_1arc_v3.tif')

    m5= get_map_info('./maps/n31_e034_1arc_v3.tif')
    m6= get_map_info('./maps/n31_e035_1arc_v3.tif')

    m7= get_map_info('./maps/n32_e034_1arc_v3.tif')
    m8= get_map_info('./maps/n32_e035_1arc_v3.tif')

    couple1 = merge_horizontal_maps(m1,m2)
    couple2 = merge_horizontal_maps(m3,m4)
    couple3 = merge_horizontal_maps(m5,m6)
    couple4 = merge_horizontal_maps(m7,m8)

    mv1 = merge_verticaly_maps(couple4,couple3)
    mv2 = merge_verticaly_maps(mv1,couple2)
    full_map = merge_verticaly_maps(mv2,couple1)
    return full_map


def print_map(map:Map):
    # Tel Aviv coordinates
    lat = map.bounds[1]
    lon = map.bounds[0]

    map_width = (map.bounds[2]-map.bounds[0])
    map_height =(map.bounds[3]-map.bounds[1])
    
    elevation_data = np.array(map.heights)

    # Create a figure and axis with Cartopy projection
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

    # Add coastlines and other features
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, edgecolor='black')

    # Plot the height data using pcolormesh
    c = ax.pcolormesh(lon + np.linspace(0, map_width, elevation_data.shape[1]),
                    lat + np.linspace(0, map_height, elevation_data.shape[0]),
                    elevation_data, cmap='viridis', transform=ccrs.PlateCarree())

    # Add colorbar
    cbar = plt.colorbar(c, ax=ax, orientation='vertical', label='Height (meters)')

    # Add gridlines and labels for x and y axes
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER


    for point in map.marked_points:
        ax.scatter(point.y, point.x, color=point.color, marker='o', s=50, transform=ccrs.PlateCarree(), label='Marker')
    
    for edges in map.marked_edges:
        pass
        
    # Set title and show the plot
    plt.title('Tel Aviv - Height Map')
    return plt


