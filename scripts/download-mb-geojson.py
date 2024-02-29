import geopandas as gpd
import pandas as pd
import os
import zipfile
import requests
import io
import time
import logging

logging.basicConfig(level=logging.INFO)

start_time = time.perf_counter()
logging.info("Downloading and loading the shapefile...")

# Download the shp.zip file to a temporary folder and extract the contents
url = 'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/MB_2021_AUST_SHP_GDA2020.zip'

response = requests.get(url, stream=True)

if response.status_code == 200:
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as shp_zip:

        # Save the shp_zip to a temporary folder
        shp_zip.extractall('../local/MB-SHP')

# 60s - 1m - 1m30s

end_time = time.perf_counter()
logging.info(f"Time taken to download and load the shapefile: {end_time - start_time} seconds")
start_time = time.perf_counter()
logging.info("Loading shapefile and selectig only columns of interest...")

# Load the shapefile into a GeoDataFrame
gdf : gpd.GeoDataFrame = gpd.read_file('../local/MB-SHP/MB_2021_AUST_GDA2020.shp')

# Select only the columns of interest and rename the 'MB_CODE21' column to 'id'
gdf = gdf[['MB_CODE21', 'geometry', 'SA4_CODE21']].rename(columns={'MB_CODE21': 'id'})

# 200s - 3m - 4m - 6m - 10m

end_time = time.perf_counter()
logging.info(f"Time taken: {end_time - start_time} seconds")
start_time = time.perf_counter()
logging.info("Saving to a single GeoJSON file...")

os.makedirs('../local/mb-geojson', exist_ok=True)

gdf[['id', 'geometry']].to_file('../local/mb-geojson/MB.geojson', driver='GeoJSON')

# 360s - 6m - 8m
end_time = time.perf_counter()
logging.info(f"Time taken: {end_time - start_time} seconds")
start_time = time.perf_counter()
logging.info("Saving to multiple chunks of GeoJSON files...")

# Save the GeoDataFrame to multiple chunks of GeoJSON files if saving to GitHub
gdf.groupby('SA4_CODE21').apply(lambda x: x[['id', 'geometry']].to_file(f'../local/mb-geojson/MB-SA4-{x.name}.geojson', driver='GeoJSON'))

# 426s - 7m - 10m
end_time = time.perf_counter()
logging.info(f"Time taken: {end_time - start_time} seconds")

# Total time taken: 20m - 30m