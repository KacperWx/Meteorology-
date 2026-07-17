!pip install cartopy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter

import regionfile as rf

print(plt.colormaps)


csv_path = "ibtracs.ALL.list.v04r01.csv"
# years = [2025]
years = np.arange(1951, 2024)


df = pd.read_csv(csv_path, low_memory=False)

region = 'southwest_indian'
wind_min = 0
months = [1, 2, 3, 4, 5, 11, 12]

lat_min, lat_max, lon_min, lon_max, region, dataset = rf.regionselector(region)
if lat_min == None:
    sys.exit()

if lon_max > 180:
    lon_max = lon_max % 360
central_lon = (lon_min + lon_max) / 2

print(lon_min, lon_max)

# -----------------------

# corrections to data formatting
df["SEASON"] = pd.to_numeric(df["SEASON"], errors='coerce')
df["LON"] = pd.to_numeric(df["LON"], errors='coerce')
df["LAT"] = pd.to_numeric(df["LAT"], errors='coerce')
df["USA_WIND"] = pd.to_numeric(df["USA_WIND"], errors='coerce')
df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"], errors='coerce')

# wrap longitudes to 0-360
if lon_max > 180:
  df["LON"] = df["LON"] % 360


if dataset == "all":
    df = df[df["USA_AGENCY"].notna()].copy()
elif dataset in ("hurdat_atl", "hurdat_epa", "jtwc_wp", "jtwc_io", "jtwc_sh", "tcvitals", "tcvightals"):
    df = df[df["USA_AGENCY"] == dataset].copy()
else:
    print("not valid")

df_filtered = df[
                (df["SEASON"].isin(years)) &
                (df["ISO_TIME"].notna()) &
                (df["ISO_TIME"].dt.hour.isin([0, 6, 12, 18])) &
                # (df["ISO_TIME"].dt.month.isin(months)) &
                (df["USA_AGENCY"].notna()) &
                (df["USA_WIND"].notna())
].copy()

#   (df["USA_AGENCY"].notna()) &

# Wrap longitudes to [0,360)
# df["LON"] = df["LON"] % 360

df_processing = df_filtered.copy()

df_filtered_agency = df_processing[~df_processing["USA_AGENCY"].isin(["tcvitals", "tcvightals"])].copy()
if not df_filtered_agency.empty:
    genesis = df_filtered_agency[~df_filtered_agency["USA_STATUS"].isin(['EX', 'MD', 'WV', 'LO', 'DB'])].copy()


genesis = (
    df_filtered_agency.sort_values("ISO_TIME")
      .groupby("USA_ATCF_ID", as_index=False)
      .first()[["LAT", "LON", "USA_ATCF_ID", "ISO_TIME"]] # "SEASON"
)

genesis = genesis[
    (genesis["LON"] >= lon_min) & (genesis["LON"] <= lon_max) &
    (genesis["LAT"] >= lat_min) & (genesis["LAT"] <= lat_max) &
    (genesis["ISO_TIME"].dt.month.isin(months))
]

lats = genesis["LAT"].values
lons = genesis["LON"].values

print(df_processing["USA_ATCF_ID"].nunique(), "storms in region after filtering")
print(df_processing["BASIN"].unique())

print(f"Found {len(genesis)} genesis points for {years}")

print(f"Genesis locations: {genesis}")


fig, ax = plt.subplots(figsize=(20, 8),
                       subplot_kw={'projection': ccrs.PlateCarree()}) # central_longitude=central_lon

# Plot the world map using Cartopy's features
ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.5)
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.5)
ax.add_feature(cfeature.LAND.with_scale('10m'))
ax.add_feature(cfeature.OCEAN.with_scale('10m'))


lon_bins = np.linspace(0, 360, 360+1)# (lon_max - lon_min)
lat_bins = np.linspace(-90, 90, 180+1)# (lat_max - lat_min)
heatmap, _, _ = np.histogram2d(lats, lons, bins=[lat_bins, lon_bins])
sigma = 5
heatmap_blurred = gaussian_filter(heatmap, sigma=sigma)

heatmap_blurred[heatmap_blurred < 0.05] = np.nan

lon_mesh, lat_mesh = np.meshgrid(lon_bins, lat_bins)

img = ax.pcolormesh(lon_mesh[:-1, :-1],
                    lat_mesh[:-1, :-1],
                    heatmap_blurred[:, :-1],
                    cmap="Spectral_r", alpha=1, transform=ccrs.PlateCarree())

ax.scatter(lons, lats, color='black', s=2.5, alpha=0.5, transform=ccrs.PlateCarree())

ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
for spine in ax.spines.values():
    spine.set_visible(False)
gls = ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', color='gray')
gls.top_labels = False
gls.right_labels = False


cbar = plt.colorbar(img, ax=ax, orientation="vertical",)
cbar.set_label("Genesis Density")

plt.title(f"TC Genesis Density\n{region}, {years.min()}-{years.max()} from IBTrACS\n{sigma}σ - 1°x1° grid", loc='left', fontsize=12, fontweight='bold', transform=ax.transAxes)
# plt.text(0, 0.01, f'*Note: High densities are possible in edge regions\nwhere existing TCs move into the plotted area', ha='left', va='bottom', fontsize=8, family='monospace', transform=ax.transAxes)
plt.title(f'@KacperWx', loc='right', fontsize=12, transform=ax.transAxes)
plt.show()