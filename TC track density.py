!pip install cartopy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter
import sys

import regionfile as rf


csv_path = "ibtracs.ALL.list.v04r01.csv"
target_years = [1982,1997,2015]                       
climo_years = np.arange(1991, 2021)         

region = 'northindian'

# -----------------------

lat_min, lat_max, lon_min, lon_max, region, dataset = rf.regionselector(region)
if lat_min == None:
    sys.exit()

if lon_max < 180:
    lon_max = lon_max % 360
central_lon = (lon_min + lon_max) / 2


df_raw = pd.read_csv(csv_path, low_memory=False)

# 1° bins (edges). Use the same for both target and climatology.
lon_bins = np.linspace(0, 360, 361)   # 0..360 edges (360 bins of 1°)
lat_bins = np.linspace(-90, 90, 181)    # edges (181 bins of 1°)
lon_mesh, lat_mesh = np.meshgrid(lon_bins, lat_bins)


def calculate_grid_counts(df_all, years,
                          lon_bins=lon_bins, lat_bins=lat_bins,
                          apply_agency_status_logic=True):

    df = df_all.copy()

    df["SEASON"] = pd.to_numeric(df["SEASON"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["USA_WIND"] = pd.to_numeric(df["USA_WIND"], errors="coerce")
    df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"], errors="coerce")

    # wrap longitudes to 0-360
    df["LON"] = df["LON"] % 360

    if dataset == "all":
        df = df[df["USA_AGENCY"].notna()].copy()
    else:
        df = df[df["USA_AGENCY"] == dataset].copy()

    df = df[
        (df["SEASON"].isin(years)) &
        (df["LON"].notna()) & (df["LAT"].notna()) &
        (df["LON"] >= lon_min) & (df["LON"] <= lon_max) &
        (df["LAT"] >= lat_min) & (df["LAT"] <= lat_max) &
        (df["ISO_TIME"].notna()) &
        (df["ISO_TIME"].dt.hour.isin([0, 6, 12, 18])) &
        (df["USA_WIND"].notna())
    ].copy()


    if apply_agency_status_logic:
        has_tcvitals = df["USA_AGENCY"].isin(["tcvitals", "tcvightals"]).any()
        if not has_tcvitals:
            df = df[~df["USA_STATUS"].isin(['EX', 'MD', 'WV', 'LO', 'DB'])].copy()
            print("Applied STATUS filter (removed EX/MD/WV/LO/DB)")
        else:
            print("Skipped STATUS filter because tcvitals-style data present")

    print(f"DEBUG: years={years} -> {df['USA_ATCF_ID'].nunique()} storms, {len(df)} points")


    counts, _, _ = np.histogram2d(df["LAT"].values, df["LON"].values, bins=[lat_bins, lon_bins])

    return counts


counts_target = calculate_grid_counts(df_raw, target_years, lon_bins=lon_bins, lat_bins=lat_bins)


counts_climo_sum = calculate_grid_counts(df_raw, climo_years, lon_bins=lon_bins, lat_bins=lat_bins)

counts_climo_mean = counts_climo_sum / float(len(climo_years))


counts_target_per_year = counts_target / float(len(target_years))


anom_abs = counts_target_per_year - counts_climo_mean
# optional percent anomaly (uncomment if wanted)
# anom_pct = (counts_target_per_year / (counts_climo_mean + 1e-12) - 1.0) * 100


sigma = 5
anom_blurred = gaussian_filter(anom_abs, sigma=sigma)

fig, ax = plt.subplots(figsize=(18, 10), subplot_kw={'projection': ccrs.PlateCarree(central_lon)}) # central_longitude=180 subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})

print(f'{lon_min}, {lon_max}')

ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.5)
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.5)
ax.add_feature(cfeature.LAND.with_scale('10m'), facecolor='0.9')
ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor='0.95')

img = ax.pcolormesh(lon_mesh[:-1, :-1], lat_mesh[:-1, :-1], anom_blurred[:, :-1],
                    cmap="RdBu_r", vmin=-np.nanmax(np.abs(anom_blurred)), vmax=np.nanmax(np.abs(anom_blurred)),
                    transform=ccrs.PlateCarree(), alpha=0.9)

ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
gl = ax.gridlines(draw_labels=True, linestyle='--', color='gray', alpha=0.6)
gl.top_labels = False
gl.right_labels = False

for spines in ax.spines:
  ax.spines[spines].set_visible(False)

cbar = plt.colorbar(img, ax=ax, orientation='vertical', shrink=0.6)
cbar.set_label("Track Density Anomaly (tracks per 1° grid, per year)")

plt.title(f"TC Track Density Anomaly\n1991-2020 climo\n{region}, {target_years} from IBTrACS\n{sigma}σ - 1x1° grid", loc='left', fontsize=10, fontweight='bold')
# plt.text(0, 0.01, f'*Note: High densities are possible in edge regions\nwhere existing TCs move into the plotted area', ha='left', va='bottom', fontsize=8, family='monospace', transform=ax.transAxes)
plt.title(f'@KacperWx', loc='right', fontsize=10)
plt.show()