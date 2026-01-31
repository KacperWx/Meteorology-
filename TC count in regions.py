# !pip install cartopy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter

import regionfile as rf

# === CONFIGURATION ===
csv_path = "ibtracs.ALL.list.v04r01.csv"
years = np.arange(1991, 2021)
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
minwind = 34

climo_years = np.arange(1991, 2021) # climatology base period (1991-2020 inclusive)

# -----------------------
region = 'global'
# dataset = "hurdat_atl" # "nhc_working_bt"

# -----------------------
# region selector function:
lat_min, lat_max, lon_min, lon_max, region, dataset = rf.regionselector(region)

# -------------------------

# === LOAD RAW CSV (unchanged) ===
df = pd.read_csv(csv_path, low_memory=False)

df = df.copy()

# -- type conversions --
df["SEASON"] = pd.to_numeric(df["SEASON"], errors="coerce")
df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
df["USA_WIND"] = pd.to_numeric(df["USA_WIND"], errors="coerce")
df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"], errors="coerce")

# -- dataset selection (keeps tcvitals if present) --
if dataset == "all":
    df = df[df["USA_AGENCY"].notna()].copy()
else:
    df = df[df["USA_AGENCY"] == dataset].copy()

# -- spatial/temporal filters --
df = df[
    (df["SEASON"].isin(years)) &
    (df["LON"].notna()) & (df["LAT"].notna()) &
    (df["LON"] >= lon_min) & (df["LON"] <= lon_max) &
    (df["LAT"] >= lat_min) & (df["LAT"] <= lat_max) &
    (df["ISO_TIME"].notna()) &
    (df["ISO_TIME"].dt.hour.isin([0, 6, 12, 18])) &
    (df["USA_WIND"] >= minwind)
].copy()
# (df["ISO_TIME"].dt.month.isin(months)) &

# -- conditional classification filtering --

# Apply filtering for 'USA_AGENCY' and 'USA_STATUS'
df_filtered_agency = df[~df["USA_AGENCY"].isin(["tcvitals", "tcvightals"])].copy()
if not df_filtered_agency.empty:
    df = df[~df_filtered_agency["USA_STATUS"].isin(['EX', 'MD', 'WV', 'LO', 'DB'])].copy()

# Compute first genesis points *before* month filtering
first_points = (
    df.sort_values("ISO_TIME")
      .groupby("USA_ATCF_ID")
      .first()
      .reset_index()
)

# === Filter storms that FORMED (not just existed) in target months ===
genesis_ids = first_points[first_points["ISO_TIME"].dt.month.isin(months)]["USA_ATCF_ID"]

# Keep only those storms in the main dataframe
df = df[df["USA_ATCF_ID"].isin(genesis_ids)].copy()

# === Count how many storms formed per month ===
genesis = first_points[first_points["USA_ATCF_ID"].isin(genesis_ids)]
genesis = genesis["ISO_TIME"].dt.month.value_counts().sort_index()

print(f"DEBUG: years={years} -> storm list: {genesis_ids}, {len(df)} points")
print("Storms forming per month:\n", genesis)
print(f"{len(first_points)} total formations in {years.min()}–{years.max()}")

fig, ax = plt.subplots(figsize=(12, 7))

for spines in ax.spines:
  ax.spines[spines].set_visible(False)

print(genesis.index)

bars = ax.bar(genesis.index, genesis.values, color='lightgreen')

# Force x-axis ticks to only show the months you have data for
ax.set_xticks(genesis.index)
ax.set_xticklabels(genesis.index)
ax.set_xlabel('Month')
ax.set_ylabel('Number of storms')

# Add text labels above each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center') # va: vertical alignment, ha: horizontal alignment

plt.text(0, 1.01, f"TC count for months {months}\n{years.min()}-{years.max()}\nMinimum Wind = {minwind}\n{region}\nfrom IBTrACS", ha='left', va='bottom', fontsize=10, fontweight='bold', transform=plt.gca().transAxes)
plt.text(1, 1.01, f'@KacperWx', ha='right', va='bottom', fontsize=10, family='monospace', transform=plt.gca().transAxes)
plt.show()