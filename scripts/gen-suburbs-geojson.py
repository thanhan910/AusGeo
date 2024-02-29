# %%
import pandas as pd
import numpy as np
import geopandas as gpd


base_url = 'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files'


df_MB = pd.read_excel(f'{base_url}/MB_2021_AUST.xlsx')
# 3m 30s


df_LGA = pd.read_excel(f'{base_url}/LGA_2023_AUST.xlsx')
# 2m


df_SAL = pd.read_excel(f'{base_url}/SAL_2021_AUST.xlsx')
# 3m 30s


df_POA = pd.read_excel(f'{base_url}/POA_2021_AUST.xlsx')
# 2m


df = pd.merge(df_MB, df_LGA, on='MB_CODE_2021', how='left', suffixes=('', '_LGA'))
df = pd.merge(df, df_SAL, on='MB_CODE_2021', how='left', suffixes=('', '_SAL'))
df = pd.merge(df, df_POA, on='MB_CODE_2021', how='left', suffixes=('', '_POA'))
# 10s

# Drop duplicate columns
df.drop(columns=['STATE_CODE_2021_LGA', 'STATE_NAME_2021_LGA', 'AUS_CODE_2021_LGA', 'AUS_NAME_2021_LGA', 'AREA_ALBERS_SQKM_LGA', 'ASGS_LOCI_URI_2021_LGA', 'STATE_CODE_2021_SAL', 'STATE_NAME_2021_SAL', 'AUS_CODE_2021_SAL', 'AUS_NAME_2021_SAL', 'AREA_ALBERS_SQKM_SAL', 'ASGS_LOCI_URI_2021_SAL', 'AUS_CODE_2021_POA', 'AUS_NAME_2021_POA', 'AREA_ALBERS_SQKM_POA', 'ASGS_LOCI_URI_2021_POA'], inplace=True)


gdf : gpd.GeoDataFrame = gpd.read_file('local/MB_2021_AUST_SHP_GDA2020/MB_2021_AUST_GDA2020.shp')
# 8m

gdf : gpd.GeoDataFrame = gdf[['MB_CODE21', 'geometry']].rename(columns={'MB_CODE21': 'MB_CODE_2021'}).merge(df, on='MB_CODE_2021', how='left')
# 10s

gdf_suburbs : gpd.GeoDataFrame = gdf[['SAL_CODE_2021', 'POA_CODE_2021', 'geometry']].dissolve(by=['SAL_CODE_2021', 'POA_CODE_2021']).reset_index()
# 3m 30s


df_suburbs = df[['SAL_CODE_2021', 'POA_CODE_2021', 'STATE_CODE_2021', 'AUS_CODE_2021']].drop_duplicates().reset_index(drop=True)


# %%
df_suburbs_info = df[[
    'SAL_CODE_2021',
    'POA_CODE_2021',
    'STATE_CODE_2021',
    'AUS_CODE_2021',
    'SAL_NAME_2021',
    'POA_NAME_2021',
    'STATE_NAME_2021',
    'AUS_NAME_2021',
]].drop_duplicates().reset_index(drop=True)

# %%
df_suburbs_area = df.groupby(['SAL_CODE_2021','POA_CODE_2021'])['AREA_ALBERS_SQKM'].sum().reset_index()


# %%
gdf_suburbs : gpd.GeoDataFrame = gdf_suburbs.merge(df_suburbs_area, on=['SAL_CODE_2021', 'POA_CODE_2021'], how='left').merge(df_suburbs_info, on=['SAL_CODE_2021', 'POA_CODE_2021'], how='left')

# %%

gdf_suburbs.rename(columns={
    'SAL_CODE_2021' : 'suburb_id',
    'POA_CODE_2021' : 'postcode_id',
    'STATE_CODE_2021' : 'state_id',
    'AUS_CODE_2021' : 'country_id',
    'SAL_NAME_2021' : 'suburb',
    'POA_NAME_2021' : 'postcode',
    'STATE_NAME_2021' : 'state_name',
    'AUS_NAME_2021' : 'country_name',
    'AREA_ALBERS_SQKM' : 'area_sqkm',
}, inplace=True)

# %%
states = {
    '1' : 'NSW',
    '2' : 'VIC',
    '3' : 'QLD',
    '4' : 'SA',
    '5' : 'WA',
    '6' : 'TAS',
    '7' : 'NT',
    '8' : 'ACT',
    '9' : 'Other Territories',
    'Z' : 'Outside Australia',
}
gdf_suburbs['state'] = gdf_suburbs['state_id'].map(states)

# %%
gdf_suburbs
# %%
# Split the suburbs into separate states, and for each state, split into 5 geojson files
for state_id in states.keys():
    gdfs = gdf_suburbs[gdf_suburbs['state_id'] == state_id].sort_values('postcode').reset_index(drop=True)
    # Split into 5 geojson files
    n = len(gdfs)
    n_per_file = n // 5
    for i in range(5):
        gdfs[i*n_per_file:(i+1)*n_per_file].to_file(f'local/suburbs-{states[state_id]}-{i}.geojson', driver='GeoJSON')
        print(f'local/suburbs-{states[state_id]}-{i}.geojson')


# %%
