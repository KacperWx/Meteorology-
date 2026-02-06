# IPTCWC OSPO eTRaP Rainfall Potential Product

!pip install cartopy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import urllib3
import os
import subprocess

import cities as city # Import cities list file

# ----------------------------------------------

# Configuration 

name = 'PENHA'

name = name.upper()

url = f'https://satepsanone.nesdis.noaa.gov/pub/TRAP/ETRAP/NWPacific/{name}-WP.ETRAP.TXT.Z'
http = urllib3.PoolManager()
response = http.request('GET', url)

compressed_file_path = f'{name}-WP.ETRAP.TXT.Z'
decompressed_file_path = f'{name}-WP.ETRAP.TXT'
with open(compressed_file_path, 'wb') as out:
    out.write(response.data)

subprocess.run(['gzip', '-d', compressed_file_path], check=False)
print(f"Successfully decompressed {compressed_file_path} to {decompressed_file_path}")
file_path = decompressed_file_path

# Read logo
logo = mpimg.imread('/content/logo.jpg')

logoimg = OffsetImage(logo, zoom=0.125)
ab_logo = AnnotationBbox(logoimg, (0, 1), frameon=False, xycoords='axes fraction', box_alignment=(0, 1))

# ------------------------------------------------------------------

# Data

print(f"Attempting to read data from: {file_path}")
try:
    
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()

    parts = first_line.split()

    storm_year_str = parts[0][4:8]
    storm_month_day_hour_str = parts[1]

    full_date_str = f'{storm_year_str}{storm_month_day_hour_str}00'
    print(f"Full Date String: {full_date_str}")
    valid_time = pd.to_datetime(full_date_str, format='%Y%m%d%H%M')
    print(f"Valid time: {valid_time}")
    forecast_end_time = valid_time + pd.Timedelta(hours=24)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    print("Please ensure the file is in the same directory as the script or provide its full path.")
    exit()
except Exception as e:
    print(f"An error occurred during file reading or time parsing: {e}")
    exit()

# 'sep=r'\s+'' handles one or more spaces as delimiters
skip_rows = 9
df = pd.read_csv(file_path, sep=r'\s+', skiprows=skip_rows, header=None)

if df.empty:
    print("Error: No data was read. The file might be empty or 'skiprows' is incorrect.")
    exit()

# Inspect
print("\n--- Parsed DataFrame Head ---")
print(df.head())
print(f"DataFrame shape: {df.shape}")

if df.shape[1] < 3:
    print(f"Error: Expected at least 3 columns for plotting (X, Y, Z), but found {df.shape[1]}.")
    print("Please check your file format and the 'skip_rows' setting.")
    exit()

# Assign data to variables
x_data = df.iloc[:, 0]
y_data = df.iloc[:, 1]
z_data = df.iloc[:, 2]

print(f"\nExtracted data types: X={x_data.dtype}, Y={y_data.dtype}, Z={z_data.dtype}")

x_data = pd.to_numeric(x_data, errors='coerce')
y_data = pd.to_numeric(y_data, errors='coerce')
z_data = pd.to_numeric(z_data, errors='coerce')

df_cleaned = pd.DataFrame({'X': x_data, 'Y': y_data, 'Z': z_data}).dropna()

if df_cleaned.empty:
    print("Error: All data points were non-numeric or resulted in NaNs after cleaning. Cannot plot.")
    exit()

x_data = df_cleaned['X']
y_data = df_cleaned['Y']
z_data = df_cleaned['Z']

unique_x = np.sort(x_data.unique())
unique_y = np.sort(y_data.unique())

# The total number of unique X * unique Y should equal the number of data points.
if len(unique_x) * len(unique_y) != len(df_cleaned):
    print("\nWarning: Data points do not form a perfectly rectangular grid.")
    print("Contour plot might require interpolation, which is not implemented in this direct approach.")
    print("Consider a scatter plot if your data is not gridded, or use `scipy.interpolate.griddata`.")
    print(f"Unique X points: {len(unique_x)}, Unique Y points: {len(unique_y)}")
    print(f"Expected data points for grid: {len(unique_x) * len(unique_y)}")
    print(f"Actual data points: {len(df_cleaned)}")

    # Create an empty grid for Z values
    Z_grid = np.full((len(unique_y), len(unique_x)), np.nan)
    for idx, row in df_cleaned.iterrows():
        x_idx = np.where(unique_x == row['X'])[0][0]
        y_idx = np.where(unique_y == row['Y'])[0][0]
        Z_grid[y_idx, x_idx] = row['Z']
else:
    df_sorted = df_cleaned.sort_values(by=['X', 'Y']).reset_index(drop=True)
    Z_grid = df_sorted['Z'].values.reshape(len(unique_x), len(unique_y)).T
    print("\nData successfully reshaped into a grid.")

# Create meshgrid for plotting
X_mesh, Y_mesh = np.meshgrid(unique_x, unique_y)

min_lon = X_mesh.min() + 5
max_lon = X_mesh.max() - 5
min_lat = Y_mesh.min() + 5
max_lat = Y_mesh.max() - 5
minplotvalshade = 0
minplotvalcontour = 100
maxplotval = 500
numlevelsshading = 51
numlevelscontour = 5
custom_levels_shade = np.linspace(minplotvalshade, maxplotval, numlevelsshading)
custom_levels_contour = np.linspace(minplotvalcontour, maxplotval, numlevelscontour)

# --- Plotting the Data ---
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(12, 10))
ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND.with_scale('10m'), facecolor='#54B461', edgecolor='black', linewidth=0.2) # Light gray land
ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.3, zorder=2)
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.5)
ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor='#0A0C33') # Light blue ocean

ax.spines['geo'].set_visible(False)

Z_grid = Z_grid * 25.4 # convert to mm

print("\n--- Generating Contour Plot ---")

contourf = ax.contourf(X_mesh, Y_mesh, Z_grid, cmap='GnBu', levels=custom_levels_shade, extend='max', transform=ccrs.PlateCarree(), zorder=1)

# Add contour lines for better visualization of gradients
contour = ax.contour(X_mesh, Y_mesh, Z_grid, colors='black', linestyles='dashed', linewidths=0.8, levels=custom_levels_contour)
plt.clabel(contour, inline=True, fontsize=8, fmt='%1.1f') # Optional: label contour lines

plt.colorbar(contourf, ax=ax, label='Forecast Rainfall (mm)') # Adjust label as per your data's units

plot_title = (
    f'NOAA OSPO Ensemble Tropical Rainfall Potential (eTRaP) for {name}\n'
    f'Rainfall Accumulation Forecast for next 24 hours\n'
    f'Valid {valid_time.strftime('%H:%M UTC %b %d %Y')} until {forecast_end_time.strftime('%H:%M UTC %b %d %Y')}'
)
plt.title(plot_title, loc='left', fontweight='bold')

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude') 
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

gl.top_labels = False
gl.right_labels = False

# What countries to plot?
regions = ['sph',]


dot_lons = []
dot_lats = []
dot_labels = []
for region in regions:
    region_function = getattr(city, region)
    current_lons, current_lats, current_labels = region_function()
    dot_lons.extend(current_lons)
    dot_lats.extend(current_lats)
    dot_labels.extend(current_labels)

# Add dots and labels
ax.scatter(dot_lons, dot_lats, color='red', marker='o', alpha=1, transform=ccrs.PlateCarree(), zorder=3)
offset = 0.05
for i in range(len(dot_lats)):
    ax.text(dot_lons[i] + offset, dot_lats[i] + offset, dot_labels[i],
            transform=ccrs.PlateCarree(), color='black')

ax.add_artist(ab_logo)
plt.tight_layout()
plt.show()