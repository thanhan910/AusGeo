import geopandas as gpd
import pandas as pd
import numpy as np
import os

SUBURBS_DATA_DIR = '../data/suburbs'
MB_DATA_DIR = '../data/mb-info'
GDF : dict[str, gpd.GeoDataFrame] = { f.split('.')[0] : gpd.read_file(os.path.join(SUBURBS_DATA_DIR, f)) for f in os.listdir(SUBURBS_DATA_DIR) }
# 1m 30s

DF = { f.split('.')[0] : pd.read_csv(os.path.join(MB_DATA_DIR, f,), dtype=str) for f in os.listdir(MB_DATA_DIR) }
# 4s - 10s

for k, df in DF.items():
    for col in df.columns:
        if 'AREA' in col:
            df[col] = df[col].astype(np.float64)

df = pd.merge(DF['MB_2021_AUST'], DF['MB_SAL_2021_AUST'], on='MB_CODE_2021', how='left')
df = pd.merge(df, DF['MB_POA_2021_AUST'], on='MB_CODE_2021', how='left')
df = pd.merge(df, DF['SA1_2021_AUST'][['SA1_CODE_2021', 'SA2_CODE_2021']], on='SA1_CODE_2021', how='left')
df = pd.merge(df, DF['SA2_2021_AUST'][['SA2_CODE_2021', 'SA3_CODE_2021']], on='SA2_CODE_2021', how='left')
df = pd.merge(df, DF['SA3_2021_AUST'][['SA3_CODE_2021', 'SA4_CODE_2021']], on='SA3_CODE_2021', how='left')
df = pd.merge(df, DF['SA4_2021_AUST'][['SA4_CODE_2021', 'GCCSA_CODE_2021']], on='SA4_CODE_2021', how='left')
df = pd.merge(df, DF['GCCSA_2021_AUST'][['GCCSA_CODE_2021', 'STATE_CODE_2021']], on='GCCSA_CODE_2021', how='left')
df = pd.merge(df, DF['STE_2021_AUST'][['STATE_CODE_2021', 'STATE_NAME_2021']], on='STATE_CODE_2021', how='left')
df = df[['MB_CODE_2021', 'SAL_CODE_2021', 'POA_CODE_2021', 'GCCSA_CODE_2021', 'STATE_CODE_2021', 'STATE_NAME_2021', 'AREA_ALBERS_SQKM']]
df = df.groupby(['SAL_CODE_2021', 'POA_CODE_2021']).agg({'AREA_ALBERS_SQKM': 'sum', 'GCCSA_CODE_2021': 'unique', 'STATE_CODE_2021': 'first', 'STATE_NAME_2021' : 'first'}).reset_index()
df = pd.merge(df, DF['SAL_2021_AUST'], on='SAL_CODE_2021', how='left')
df = pd.merge(df, DF['POA_2021_AUST'], on='POA_CODE_2021', how='left')

STATE_CODES = {
    '1': 'NSW',
    '2': 'VIC',
    '3': 'QLD',
    '4': 'SA',
    '5': 'WA',
    '6': 'TAS',
    '7': 'NT',
    '8': 'ACT',
    '9': 'OT',
    'Z': 'ZZZ'
}
df['state'] = df['STATE_CODE_2021'].map(STATE_CODES)

df.rename(columns={
    'SAL_CODE_2021' : 'suburb_id',
    'POA_CODE_2021' : 'postcode_id',
    'AREA_ALBERS_SQKM' : 'area_sqkm',
    'GCCSA_CODE_2021' : 'gccsa_code',
    'SAL_NAME_2021' : 'suburb',
    'POA_NAME_2021': 'postcode',
    'STATE_CODE_2021': 'state_id',
    'STATE_NAME_2021': 'state_name'
}, inplace=True)

df = df[['suburb_id', 'postcode_id', 'suburb', 'postcode', 'state', 'area_sqkm']]

for k, gdf in GDF.items():
    gdf = gdf[['suburb_id', 'postcode_id', 'geometry']]
    GDF[k] = pd.merge(gdf, df, left_on=['suburb_id', 'postcode_id'], right_on=['suburb_id', 'postcode_id'], how='left')

os.makedirs('../local/suburbs', exist_ok=True)

for k, gdf in GDF.items():
    GDF[k].to_file(os.path.join('../local/suburbs', f'{k}.geojson'), driver='GeoJSON')
# 1m 30s




