import matplotlib.pyplot as plt
import numpy as np

def cmap_setup(var_name, anomalyrequest, dataReady, request, lats_regional, lons_regional):

    manual_min = None
    manual_max = None

    if var_name == 'd':
        fullname = 'Divergence'
        dataReady = dataReady * (10**4)
        dataunit = '10^-4 s^−1'
        if anomalyrequest == 'No':
            cmap = 'RdYlBu_r'
            levels = np.arange(-2, 2.5, 0.25)
        elif anomalyrequest == 'Yes':
            cmap = 'RdBu_r'
            levels = np.arange(-2, 2, 0.25)

    elif var_name == 'z':
        fullname = 'Geopotential Height'
        dataReady = dataReady / 100
        dataunit = 'dam'

        if anomalyrequest == 'No':
            manual_min = 475
            manual_max = 600

            colors = [(0, 'purple'),     
                      (0.2, 'blue'),  
                      (0.4, 'cyan'),  
                      (0.56, 'green'),  
                      (0.8, 'yellow'),  
                      (1, 'crimson')]      

            cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('custom_z', colors, N=256)
            levels = np.arange(manual_min, manual_max + 1, 5)

            variable = request['variable'][0] if isinstance(request['variable'], list) else request['variable']
#            contour_lines = ax.contour(lons_regional, lats_regional, dataReady,
#                                     levels=np.arange(540, 541, 1),
#                                     colors='black',
#                                     linewidths=1,
#                                     transform=ccrs.PlateCarree())
#
#            ax.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.0f')

        elif anomalyrequest == 'Yes':
            manual_min = -36
            manual_max = 36

            colors = [(0, 'darkblue'),      # Strong negative
                      (0.5, 'white'),  
                      (1, 'crimson')]      # Strong positive

            cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('custom_z', colors, N=256)
            levels = np.arange(manual_min, manual_max + 1, 4)

            # variable = request['variable'][0] if isinstance(request['variable'], list) else request['variable']
            # contour_lines = ax.contour(lons_regional, lats_regional, dataReady,
            #                          levels=np.arange(, 541, 1),
            #                          colors='black',
            #                          linewidths=1,
            #                          transform=ccrs.PlateCarree())
            # # Label the contour lines
            # ax.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.0f')

    elif var_name == 'vo':
        fullname = 'Relative Vorticity'
        dataReady = dataReady * (10**5)
        dataunit = '10⁻⁵ s⁻¹'

        manual_min = -30
        manual_max = 30

        # Define custom colormap
        colors = [(0, 'blue'),      # Strong negative vorticity
                  (0.4, 'white'),  
                  (0.6, 'white'),  
                  (1, 'red')]      # Strong positive vorticity

        cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('custom_vorticity', colors, N=256)
        levels = np.arange(manual_min, manual_max + 1, 1)

    elif var_name == 'wind':
        fullname = 'Wind Speed'
        dataReady = dataReady * 1.94384
        dataunit = 'kts'

        if anomalyrequest == 'No':
            manual_min = 0
            manual_max = 200

            colors = [(0, 'white'),
                      (0.2, 'lightgreen'),
                      (0.4, 'yellow'),
                      (0.6, 'red'),
                      (0.8, 'purple'),
                      (1, 'pink')]

            cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('custom_wind', colors, N=256)
            levels = np.arange(manual_min, manual_max + 1, 5)

        elif anomalyrequest == 'Yes':
            manual_min = -50
            manual_max = 50

            colors = [(0, 'darkblue'),      # Strong negative
                      (0.5, 'white'),  # White
                      (1, 'crimson')]      # Strong positive

            cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('custom_wind', colors, N=256)
            levels = np.arange(manual_min, manual_max + 1, 5)

    elif var_name == 'pv':
        fullname = 'Potential Vorticity'
        dataReady = dataReady * (10**6)
        dataunit = 'PVU'
        cmap = 'RdBu_r'
        levels = np.arange(-3, 9, 0.5)

    elif var_name == 'sp':
        fullname = 'Surface Pressure'
        dataReady = dataReady / 100
        dataunit = 'hPa'
        cmap = 'RdBu'
        levels = np.arange(500, 1050, 50)

    elif var_name == 'msl':
        fullname = 'Mean Sea Level Pressure'
        dataReady = dataReady / 100
        dataunit = 'hPa'

        manual_min = 900
        manual_max = 1050

        colors = [(0, 'blue'),      # low
                  (0.7333, 'white'),  # average (1000)
                  (1, 'red')]      # high

        cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('custom_pres', colors, N=256)
        levels = np.arange(manual_min, manual_max + 1, 1)

        variable = request['variable'][0] if isinstance(request['variable'], list) else request['variable']
#        contour_lines10 = ax.contour(lons_regional, lats_regional, dataReady,
#                                 levels=np.arange(manual_min, manual_max + 1, 10),
#                                 colors='black',
#                                 linewidths=2,
#                                 transform=ccrs.PlateCarree())
#        contour_lines2 = ax.contour(lons_regional, lats_regional, dataReady,
#                                 levels=np.arange(manual_min, manual_max + 1, 2),
#                                 colors='black',
#                                 linewidths=1,
#                                 transform=ccrs.PlateCarree())
#        ax.clabel(contour_lines2, inline=True, fontsize=10, fmt='%1.0f')

#        size = 50
#        local_max = maximum_filter(dataReady, size=size)
#        local_min = minimum_filter(dataReady, size=size)
#
#        maxima_locations = np.where(dataReady == local_max)
#        minima_locations = np.where(dataReady == local_min)
#
#        for i in range(len(maxima_locations[0])):
#            lat_idx = maxima_locations[0][i]
#            lon_idx = maxima_locations[1][i]
#
#            if 0 <= lat_idx < len(lats_regional) and 0 <= lon_idx < len(lons_regional):
#                lat = lats_regional[lat_idx]
#                lon = lons_regional[lon_idx]
#                val = dataReady.values[lat_idx, lon_idx]
#
#                ax.text(lon, lat, f'H\n{val:.0f}', ha='center', va='center',
#                        color='black', fontsize=12, fontweight='bold',
#                        transform=ccrs.PlateCarree())
#
#        for i in range(len(minima_locations[0])):
#            lat_idx = minima_locations[0][i]
#            lon_idx = minima_locations[1][i]
#
#            if 0 <= lat_idx < len(lats_regional) and 0 <= lon_idx < len(lons_regional):
#                lat = lats_regional[lat_idx]
#                lon = lons_regional[lon_idx]
#                val = dataReady.values[lat_idx, lon_idx]
#
#                ax.text(lon, lat, f'L\n{val:.0f}', ha='center', va='center',
#                        color='black', fontsize=12, fontweight='bold',
#                        transform=ccrs.PlateCarree())

    elif var_name == 't2m' or var_name == 't':
        fullname = 'Temperature'
        dataReady = dataReady - 273.15
        dataunit = 'deg C'
        cmap = 'rainbow'
        levels = np.arange(-40, 41, 2)

    elif var_name == 'd2m':
        fullname = '2m Dewpoint Temperature'
        dataReady = dataReady - 273.15
        dataunit = 'deg C'
        cmap = 'RdYlGn'
        levels = np.arange(-40, 41, 2)

    elif var_name == 'sde':
        fullname = 'Snow Depth'
        dataunit = 'm'
        cmap = 'Blues'
        levels = np.arange(0, 201, 20)

    elif var_name == 'snowc':
        fullname = 'Snow Cover'
        dataunit = '%'
        if anomalyrequest == 'No':
            cmap = 'Blues'
            levels = np.arange(0, 100, 2)
        elif anomalyrequest == 'Yes':
            cmap = 'RdBu_r'
            levels = np.arange(-50, 50, 2)

    elif var_name == 'r':
        fullname = 'Relative Humidity'
        dataunit = '%'
        cmap = 'RdYlGn'
        levels = np.arange(0, 101, 5)

    elif var_name == 'w':
        fullname = 'Vertical Velocity'
        dataunit = 'Pa s^-1'
        cmap = 'coolwarm'
        levels = np.arange(-2, 2, 0.25)

    elif var_name == 'theta_e':
        fullname = 'Equivalent Potential Temperature'
        dataunit = 'K'
        cmap = 'RdYlGn'
        levels = np.arange(280, 380, 2.5)

    else:
        print(f"{var_name} is the var name")
        fullname = var_name.upper()
        dataunit = 'units'
        cmap = 'viridis'
        data_min, data_max = float(dataReady.min()), float(dataReady.max())
        levels = np.linspace(data_min, data_max, 21)

    return manual_min, manual_max, dataReady, fullname, dataunit, cmap, levels