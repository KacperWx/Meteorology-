import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime as dt
from scipy.interpolate import griddata
import warnings

data_path = "https://www.wpc.ncep.noaa.gov/tropical/rain/CONUS_rainfall_obs_1900-2020.csv"
df = pd.read_csv(data_path)
print(df)

stormname = 'Irma'
stormyear = '2017'

filter_df = df[df['Storm'] == f'{stormname} {stormyear}']
# Remove NaN entries
filter_df = filter_df.loc[~np.isnan(filter_df['Lat']) & ~np.isnan(filter_df['Lon']) & ~np.isnan(filter_df['Total'])]

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
ax.spines['geo'].set_visible(False)

rainfall = filter_df['Total'].values
lat = filter_df['Lat'].values
lon = filter_df['Lon'].values

def interpolate(filter_df, lat, lon):
    grid_res=0.1
    method='linear'
    grid_lon = np.arange(-140, -60+grid_res, grid_res)
    grid_lat = np.arange(20, 50+grid_res, grid_res)

    # Interpolation
    grid = griddata((lat, lon), rainfall,
                    (grid_lat[None, :], grid_lon[:, None]), method=method)
    grid = np.transpose(grid)

    return xr.DataArray(grid, coords=[grid_lat, grid_lon], dims=['lat', 'lon'])

rainfall_grid = interpolate(filter_df, lat, lon)

levels = np.arange(0, 25, 1)

# Zorders set to restrict rainfall contours to land.
colors = ax.contourf(rainfall_grid.lon, rainfall_grid.lat, rainfall_grid.values, cmap='Greens', levels=levels, transform=ccrs.PlateCarree(), zorder=1)
cbar = plt.colorbar(colors, ax=ax, label='Total Precipitation (in)')

ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor='#0A0C33', zorder=2)

ax.add_feature(cfeature.LAND.with_scale('10m'), edgecolor='k', facecolor='white', linewidth=0.5, zorder=0)
ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.5, edgecolor='k', zorder=2)
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.5, edgecolor='k', zorder=2)
ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.5, edgecolor='k', zorder=2)

# To focus on the most relevant areas
boundfilter_df = filter_df.loc[(filter_df['Total'] > 5)]

lonmin = boundfilter_df['Lon'].min() - 5
lonmax = boundfilter_df['Lon'].max() + 5
latmin = boundfilter_df['Lat'].min() - 5
latmax = boundfilter_df['Lat'].max() + 5

ax.set_extent([lonmin, lonmax, latmin, latmax], crs=ccrs.PlateCarree()) 
gl = ax.gridlines(draw_labels=True, color='w', linestyle='--', zorder=5)
gl.top_labels = False
gl.right_labels = False

plt.title(f"{stormname} {stormyear}\nWeather Prediction Center\nTropical Rainfall", loc='left', fontweight='bold')
plt.title(f"@KacperWx", loc='right')
plt.show()
print(filter_df)