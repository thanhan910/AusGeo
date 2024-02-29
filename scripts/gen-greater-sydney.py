
import pandas as pd
import geopandas as gpd
import numpy as np
import json
import os
import requests
import io
import zipfile


dfMB = pd.concat([pd.read_csv(f'data/core/mb-info/MB-{state_code}.csv', dtype=str) for state_code in [1, 2, 4, 5, 6, 8, 9, 'Z']], ignore_index=True)


dfMB['AREA_ALBERS_SQKM'] = dfMB['AREA_ALBERS_SQKM'].astype(float)


dfMB.columns


dfMB['GCCSA_NAME_2021'].value_counts()



df_suburbs = dfMB.groupby(['SAL_CODE_2021', 'POA_CODE_2021']).aggregate({
    'SAL_NAME_2021' : 'first',
    'POA_NAME_2021' : 'first',
    'GCCSA_NAME_2021' : 'unique',
    'LGA_NAME_2023' : 'unique',
    'STATE_CODE_2021' : 'first',
    'STATE_NAME_2021' : 'first',
    'AUS_CODE_2021' : 'first',
    'AUS_NAME_2021' : 'first',
    'AREA_ALBERS_SQKM' : 'sum',
    'MB_CATEGORY_2021' : 'unique',
}).reset_index().rename(columns={
    'SAL_CODE_2021' : 'suburb_id',
    'POA_CODE_2021' : 'postcode_id',
    'SAL_NAME_2021' : 'suburb_name',
    'POA_NAME_2021' : 'postcode',
    'GCCSA_NAME_2021' : 'capital_city',
    'LGA_NAME_2023' : 'lgas',
    'STATE_CODE_2021' : 'state_id',
    'STATE_NAME_2021' : 'state_name',
    'AUS_CODE_2021' : 'country_id',
    'AUS_NAME_2021' : 'country_name',
    'AREA_ALBERS_SQKM' : 'area_sqkm',
    'MB_CATEGORY_2021' : 'categories',
})


# Temporary analyses
df_suburbs['lga'] = df_suburbs['lgas'].apply(lambda x: x[0] if len(x) == 1 else x)
df_suburbs['lga_count'] = df_suburbs['lgas'].apply(len)
df_suburbs['gccsa_count'] = df_suburbs['capital_city'].apply(len)
df_suburbs['lga_count'].value_counts()

greater_capital_city_area = 'Greater Sydney'

postcodes_first_2_digits = df_suburbs[(df_suburbs['capital_city'].apply(lambda x: greater_capital_city_area in x))]['postcode_id'].str[:2].unique()
postcodes_first_2_digits.sort()


gdf : gpd.GeoDataFrame = gpd.GeoDataFrame(pd.concat([gpd.read_file(f'data/core/suburbs/suburbs-1-{p2}.geojson') for p2 in postcodes_first_2_digits], ignore_index=True))
# 20s - 30s


df_greater_melbourne_ids = df_suburbs[(df_suburbs['capital_city'].apply(lambda x: greater_capital_city_area in x))][['suburb_id', 'postcode_id']]


df_greater_melbourne_ids[greater_capital_city_area] = True


gdf = gdf.merge(df_greater_melbourne_ids, on=['suburb_id', 'postcode_id'], how='left')


gdf = gdf[gdf[greater_capital_city_area] == True]


gdf.drop(columns=[greater_capital_city_area], inplace=True)


os.makedirs('data/custom', exist_ok=True)


gdf.to_file('data/custom/suburbs-greater-sydney.geojson', driver='GeoJSON')


