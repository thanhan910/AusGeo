
import pandas as pd
import geopandas as gpd
import numpy as np
import json
import os


# Get all json files in folder data/geojson
geojson_files = list(os.listdir('data/geojson'))


ACT_files = [f for f in geojson_files if 'suburbs-ACT' in f]
gdf_ACT_s = []
for f in ACT_files:
    gdf_ACT_s.append(gpd.read_file('data/geojson/' + f))


states = ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT', 'Other Territories', 'Outside Australia']
gdfk = {}
for state in states:
    gdf_s = []
    state_files = [f for f in geojson_files if f'suburbs-{state}' in f]
    gdfk[state] = gpd.GeoDataFrame(pd.concat([gpd.read_file('data/geojson/' + f) for f in state_files], ignore_index=True))

    print(f'{state} has {len(gdfk[state])} files')
# 2m - 3m


original_columns = ['suburb_id', 'postcode_id', 'area_sqkm', 'state_id', 'country_id', 'suburb', 'postcode', 'state_name', 'country_name', 'state', 'geometry']


state_id = {'NSW': 1, 'VIC': 2, 'QLD': 3, 'SA': 4, 'WA': 5, 'TAS': 6, 'NT': 7, 'ACT': 8, 'Other Territories': 9, 'Outside Australia': 'Z'}


# Rename keys of gdfk map to state_id
gdfk = {state_id[k]: gdfk[k] for k in gdfk.keys()}



os.makedirs('data/suburbs', exist_ok=True)


for state, gdf in gdfk.items():
    if len(gdf) == 0:
        continue
    gdf['pc2'] = gdf['postcode'].str[:2]

    gdf.groupby('pc2').apply(lambda x: x[original_columns].to_file(f'data/suburbs/suburbs-{state}-{x.name}.geojson', driver='GeoJSON'))
    print(f'Finished {state}')
# 1m30s - 2m


