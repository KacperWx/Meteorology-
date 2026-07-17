import matplotlib.pyplot as plt
import numpy as np
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from shapely import geometry

regions = ["atl", "gom", "wgom", "nwatl", "nwatl", "subtropatl", 
           "ncatl", "neatl", "carib", "opentropatl", "etropatl", 
           "aew", "epac_prop", "epac", "cpac", "wpac", "opentropwpac", "subtropwpac", "scs", "dateline", "northindian", "ph", "med", "cmed", 
           "emed", "global", "southwest_indian", "mozchannel", "map", "list"]

def regionselector(region):

    if region == "atl":
        lat_min = 0
        lat_max = 60
        lon_min = -100
        lon_max = -5
        region = "Atlantic"
        dataset = "hurdat_atl"

    elif region == "gom":
        lat_min = 15
        lat_max = 35
        lon_min = -105
        lon_max = -75
        region = "Gulf of Mexico"
        dataset = "hurdat_atl"

    elif region == "wgom":
        lat_min = 15
        lat_max = 35
        lon_min = -105
        lon_max = -90
        region = "Western Gulf of Mexico"
        dataset = "hurdat_atl"

    elif region == "nwatl":
        lat_min = 20
        lat_max = 50
        lon_min = -90
        lon_max = -50
        region = "Northwest Atlantic"
        dataset = "hurdat_atl"

    elif region == "subtropatl":
        lat_min = 20
        lat_max = 50
        lon_min = -85
        lon_max = -5
        region = "Subtropical Atlantic"
        dataset = "hurdat_atl"

    elif region == "ncatl":
        lat_min = 20
        lat_max = 50
        lon_min = -70
        lon_max = -30
        region = "North-Central Atlantic"
        dataset = "hurdat_atl"

    elif region == "neatl":
        lat_min = 20
        lat_max = 50
        lon_min = -40
        lon_max = -5
        region = "Northeast Atlantic"
        dataset = "hurdat_atl"

    elif region == "carib":
        lat_min = 5
        lat_max = 25
        lon_min = -90
        lon_max = -60
        region = "Caribbean"
        dataset = "hurdat_atl"

    elif region == "opentropatl":
        lat_min = 5
        lat_max = 25
        lon_min = -65
        lon_max = -15
        region = "Tropical Atlantic"
        dataset = "hurdat_atl"

    elif region == "etropatl":
        lat_min = 5
        lat_max = 25
        lon_min = -40
        lon_max = -15
        region = "Eastern Tropical Atlantic"
        dataset = "hurdat_atl"

    elif region == "aew":
        lat_min = 0
        lat_max = 25
        lon_min = -40
        lon_max = 40
        region = "Eastern Tropical Atlantic, Sahel and Southern Sahara"
        dataset = "hurdat_atl"

    elif region == "epac_prop":
        lat_min = 0
        lat_max = 30
        lon_min = -140
        lon_max = -80
        region = "Eastern Pacific (east of 140W)"
        dataset = "hurdat_epa"

    elif region == "epac":
        lat_min = 0
        lat_max = 50
        lon_min = -180
        lon_max = -80
        region = "Central and Eastern Pacific"
        dataset = "hurdat_epa"

    elif region == "cpac":
        lat_min = 0
        lat_max = 50
        lon_min = -180
        lon_max = -140
        region = "Central Pacific"
        dataset = "hurdat_epa"

    elif region == "wpac":
        lat_min = 0
        lat_max = 50
        lon_min = 100
        lon_max = 180
        region = "Western Pacific"
        dataset = "jtwc_wp"

    elif region == "ph":
        lat_min = 0
        lat_max = 25
        lon_min = 120
        lon_max = 145
        region = "Philippine Sea"
        dataset = "jtwc_wp"

    elif region == "opentropwpac":
        lat_min = 0
        lat_max = 50
        lon_min = 140
        lon_max = 180
        region = "Open Tropical Western Pacific"
        dataset = "jtwc_wp"

    elif region == "subtropwpac":
        lat_min = 20
        lat_max = 45
        lon_min = 120
        lon_max = 180
        region = "Subtropical Western Pacific"
        dataset = "jtwc_wp"

    elif region == "scs":
        lat_min = 0
        lat_max = 25
        lon_min = 100
        lon_max = 125
        region = "South China Sea"
        dataset = "jtwc_wp"

    elif region == "dateline":
        lat_min = -20
        lat_max = 20
        lon_min = 140
        lon_max = 220
        region = "International Date Line"
        dataset = "all"

    elif region == "northindian":
        lat_min = 0
        lat_max = 30
        lon_min = 40
        lon_max = 100
        region = "North Indian Ocean"
        dataset = "jtwc_io"

    elif region == "med":
        lat_min = 30
        lat_max = 50
        lon_min = -10
        lon_max = 45
        region = "Mediterranean"
        dataset = None

    elif region == "cmed":
        lat_min = 30
        lat_max = 42
        lon_min = 10
        lon_max = 25
        region = "Central Mediterranean"
        dataset = None

    elif region == "emed":
        lat_min = 30
        lat_max = 42
        lon_min = 20
        lon_max = 40
        region = "Eastern Mediterranean"
        dataset = None

    elif region == "global":
        lat_min = -60
        lat_max = 60
        lon_min = -180
        lon_max = 180
        region = "Global"
        dataset = "all"

    elif region == "southwest_indian":
        lat_min = -40
        lat_max = 0
        lon_min = 20
        lon_max = 90
        region = "South-West Indian Ocean"
        dataset = "jtwc_sh"

    elif region == "mozchannel":
        lat_min = -25
        lat_max = -12
        lon_min = 30
        lon_max = 49
        region = "Mozambique Channel"
        dataset = "jtwc_sh"

    elif region == "map":
        # Create a single figure for all regions
        fig = plt.figure(figsize=(16, 10))
        ax = plt.axes(projection=ccrs.PlateCarree())

        ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.5)
        ax.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.5)
        ax.add_feature(cfeature.LAND.with_scale('10m'), facecolor='#54B461')
        ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor='#0A0C33')

        # Add all regions to the same plot
        for reg in regions:
            if reg != "map" and reg != "list":
                lat_min, lat_max, lon_min, lon_max, region_name, dataset = regionselector(reg)
                geom = geometry.box(minx=lon_min, maxx=lon_max, miny=lat_min, maxy=lat_max)
                ax.add_geometries([geom], crs=ccrs.PlateCarree(), alpha=0.5, 
                                facecolor='none', edgecolor='white', linewidth=1.5)
                # Add region label at the center of the box
                center_lon = (lon_min + lon_max) / 2
                center_lat = (lat_min + lat_max) / 2
                ax.text(center_lon, center_lat, reg, 
                       transform=ccrs.PlateCarree(), 
                       fontsize=10, ha='center', va='center', color='white')
        gl = ax.gridlines(draw_labels=True, linestyle='--', color='white', alpha=0.6)
        gl.top_labels = False
        gl.right_labels = False

        for spines in ax.spines:
          ax.spines[spines].set_visible(False)
        
        plt.title('All Defined Regions', fontsize=14, fontweight='bold', loc='left')
        plt.show()
        return None, None, None, None, None, None 

    elif region == "list":
        print(regions)
        return None, None, None, None, None, None 

    return lat_min, lat_max, lon_min, lon_max, region, dataset

