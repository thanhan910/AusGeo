import pandas as pd
import numpy as np
import geopandas as gpd
import os


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


os.makedirs('data/blocks', exist_ok=True)


# Split df into states
states = df['STATE_CODE_2021'].unique()
for state_code in states:
    df[df['STATE_CODE_2021'] == state_code].to_csv(f'data/blocks/MB-{state_code}.csv', index=False)


