# Generate GeoJSON files of suburbs-postcodes areas in Australia

import pandas as pd
import geopandas as gpd
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import numpy as np


df_MB = pd.read_csv('../data/mb-info/MB_2021_AUST.csv', dtype=str)
df_SAL = pd.read_csv('../data/mb-info/SAL_2021_AUST.csv', dtype=str)
df_POA = pd.read_csv('../data/mb-info/POA_2021_AUST.csv', dtype=str)
df_MB_SAL = pd.read_csv('../data/mb-info/MB_SAL_2021_AUST.csv', dtype=str)
df_MB_POA = pd.read_csv('../data/mb-info/MB_POA_2021_AUST.csv', dtype=str)
# 1s - 2s


df_MB = pd.merge(df_MB, df_MB_SAL, on='MB_CODE_2021', how='left')
df_MB = pd.merge(df_MB, df_MB_POA, on='MB_CODE_2021', how='left')
# 1s - 2s


GDF : gpd.GeoDataFrame = gpd.read_file('../local/mb.geojson')


GDF.dropna(subset=['geometry'], inplace=True)


GDF = GDF.merge(df_MB[['MB_CODE_2021', 'SAL_CODE_2021', 'POA_CODE_2021']], left_on='id', right_on='MB_CODE_2021', how='left')
# 1s - 2s
GDF.drop(columns=['MB_CODE_2021'], inplace=True)
GDF.rename(columns={'SAL_CODE_2021': 'suburb_id', 'POA_CODE_2021': 'postcode_id'}, inplace=True)


GDF = gpd.GeoDataFrame(GDF, crs='EPSG:4326', geometry='geometry')


# GRoup by postcode_id and suburb_id
GDF = GDF.dissolve(by=['suburb_id', 'postcode_id'], aggfunc='first')
# 3m -4m


GDF.reset_index(inplace=True)


GDF = GDF[['postcode_id', 'suburb_id', 'geometry']]


df_SA1 = pd.read_csv('../data/mb-info/SA1_2021_AUST.csv', dtype=str)
df_SA2 = pd.read_csv('../data/mb-info/SA2_2021_AUST.csv', dtype=str)
df_SA3 = pd.read_csv('../data/mb-info/SA3_2021_AUST.csv', dtype=str)
df_SA4 = pd.read_csv('../data/mb-info/SA4_2021_AUST.csv', dtype=str)
df_GCCSA = pd.read_csv('../data/mb-info/GCCSA_2021_AUST.csv', dtype=str)
df_MB = df_MB[['MB_CODE_2021', 'SAL_CODE_2021', 'POA_CODE_2021', 'SA1_CODE_2021']]
df_MB = pd.merge(df_MB, df_SA1[['SA1_CODE_2021', 'SA2_CODE_2021']], on='SA1_CODE_2021', how='left')
df_MB = pd.merge(df_MB, df_SA2[['SA2_CODE_2021', 'SA3_CODE_2021']], on='SA2_CODE_2021', how='left')
df_MB = pd.merge(df_MB, df_SA3[['SA3_CODE_2021', 'SA4_CODE_2021']], on='SA3_CODE_2021', how='left')
df_MB = pd.merge(df_MB, df_SA4[['SA4_CODE_2021', 'GCCSA_CODE_2021']], on='SA4_CODE_2021', how='left')
df_MB = pd.merge(df_MB, df_GCCSA[['GCCSA_CODE_2021', 'STATE_CODE_2021']], on='GCCSA_CODE_2021', how='left')


df_SP_GCCSA = df_MB[['SAL_CODE_2021', 'POA_CODE_2021', 'GCCSA_CODE_2021']].drop_duplicates().reset_index(drop=True)
# # Partition df_SP_GCCSA by GCCSA_CODE_2021
# df_SP_GCCSA = df_SP_GCCSA.groupby('GCCSA_CODE_2021').apply(lambda x: x[['SAL_CODE_2021', 'POA_CODE_2021']].reset_index(drop=True))
# df_SP_GCCSA = df_SP_GCCSA.groupby(['SAL_CODE_2021', 'POA_CODE_2021'])['GCCSA_CODE_2021'].unique().reset_index()


gdf_SP_GCCSA = pd.merge(df_SP_GCCSA, GDF, left_on=['SAL_CODE_2021', 'POA_CODE_2021'], right_on=['suburb_id', 'postcode_id']).drop(columns=['SAL_CODE_2021', 'POA_CODE_2021'])


gdf_SP_GCCSA = gpd.GeoDataFrame(gdf_SP_GCCSA, crs='EPSG:4326', geometry='geometry')


os.makedirs('../local/suburbs', exist_ok=True)


gdf_SP_GCCSA.groupby('GCCSA_CODE_2021').apply(lambda x: x[['suburb_id', 'postcode_id', 'geometry']].to_file(f'../local/suburbs/suburbs-{x.name}.geojson', driver='GeoJSON'))
# 1m 30s - 4m


gdf_1RNSW = gdf_SP_GCCSA[gdf_SP_GCCSA['GCCSA_CODE_2021'] == '1RNSW'].reset_index(drop=True)


gdf_1RNSW['postcode_id'].str[:2].value_counts().sort_index()


# Partition gdf_1RNSW by postcode_id < 2500 and >= 2500
gdf_1RNSW_2500 = gdf_1RNSW[gdf_1RNSW['postcode_id'].str[:2] >= '25'].reset_index(drop=True)
gdf_1RNSW_2499 = gdf_1RNSW[gdf_1RNSW['postcode_id'].str[:2] < '25'].reset_index(drop=True)


gdf_1RNSW_2499.to_file('../local/suburbs/suburbs-1RNSW-2499.geojson', driver='GeoJSON')
gdf_1RNSW_2500.to_file('../local/suburbs/suburbs-1RNSW-2500.geojson', driver='GeoJSON')
# 30s - 1m