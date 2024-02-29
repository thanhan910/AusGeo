# Convert the tables to 3NF, removing the transitive dependencies. The functional dependencies are as follows:
# 
# MB_CODE_2021 -> SA1_CODE_2021 -> SA2_CODE_2021 -> SA3_CODE_2021 -> SA4_CODE_2021 -> GCCSA_CODE_2021 -> STATE_CODE_2021 -> AUS_CODE_2021
# 
# SA1_CODE_2021 -> ILOC_CODE_2021 -> IARE_CODE_2021 -> IREG_CODE_2021 -> STATE_CODE_2021
# 
# MB_CODE_2021 -> LGA_CODE_2023 -> STATE_CODE_2021
# MB_CODE_2021 -> LGA_CODE_2022 -> STATE_CODE_2021
# MB_CODE_2021 -> LGA_CODE_2021 -> STATE_CODE_2021
# MB_CODE_2021 -> SED_CODE_2022 -> STATE_CODE_2021
# MB_CODE_2021 -> SED_CODE_2021 -> STATE_CODE_2021
# MB_CODE_2021 -> CED_CODE_2021 -> STATE_CODE_2021
# MB_CODE_2021 -> POA_CODE_2021 -> AUS_CODE_2021
# MB_CODE_2021 -> ADD_CODE_2021 -> AUS_CODE_2021
# MB_CODE_2021 -> SAL_CODE_2021 -> STATE_CODE_2021
# 
# MB_CODE_2021 -> DZN_CODE_2021 -> SA2_CODE_2021 -> STATE_CODE_2021 -> AUS_CODE_2021
# (Not all STATE_CODE_2021 in DZN_SA2_2021_AUST and MB_DZN_2021_AUST are in STE_2021_AUST)
# 
# SA2_CODE_2021 -> TR_CODE_2021 -> STATE_CODE_2021
# 
# SA2_CODE_2021 -> SUA_CODE_2021 -> AUS_CODE_2021
# 
# SA1_CODE_2021 -> RA_CODE_2021 -> STATE_CODE_2021
# 
# SA1_CODE_2021 -> UCL_CODE_2021 -> SOSR_CODE_2021 -> SOS_CODE_2021 -> STATE_CODE_2021
# 


import pandas as pd
import geopandas as gpd
import numpy as np
import os

table_names = {
  'MB_2021_AUST': 'Mesh Blocks - 2021',
  'SA1_2021_AUST': 'Statistical Areas Level 1 - 2021',
  'SA2_2021_AUST': 'Statistical Areas Level 2 - 2021',
  'SA3_2021_AUST': 'Statistical Areas Level 3 - 2021',
  'SA4_2021_AUST': 'Statistical Areas Level 4 - 2021',
  'GCCSA_2021_AUST': 'Greater Capital City Statistical Areas - 2021',
  'STE_2021_AUST': 'States and Territories - 2021',
  'AUS_2021_AUST': 'Australia - 2021',
  'INDIGENOUS_STRUCTURE_ALLOCATION_2021': 'Indigenous Structure - 2021',
  'ILOC_2021_AUST': 'Indigenous Locations - 2021',
  'IARE_2021_AUST': 'Indigenous Areas - 2021',
  'IREG_2021_AUST': 'Indigenous Regions - 2021',
  'LGA_2023_AUST': 'Local Government Areas - 2023',
  'LGA_2022_AUST': 'Local Government Areas - 2022',
  'LGA_2021_AUST': 'Local Government Areas - 2021',
  'SED_2022_AUST': 'State Electoral Divisions - 2022',
  'SED_2021_AUST': 'State Electoral Divisions - 2021',
  'CED_2021_AUST': 'Commonwealth Electoral Divisions - 2021',
  'POA_2021_AUST': 'Postal Areas - 2021',
  'TR_2021_AUST': 'Tourism Regions - 2021',
  'ADD_2021_AUST': 'Australian Drainage Divisions - 2021',
  'SAL_2021_AUST': 'Suburbs and Localities - 2021',
  'MB_DZN_2021_AUST': 'Destination Zones - 2021',
  'DZN_SA2_2021_AUST': 'Destination Zones to Statistical Areas Level 2 - 2021',
  'SUA_2021_AUST': 'Significant Urban Areas - 2021',
  'UCL_SOSR_SOS_2021_AUST': 'Urban Centres and Localities, Section of State and Section of State Range - 2021',
  'SUA_association_2016_2021': 'Significant Urban Area association - 2016 to 2021',
  'UCL_association_2016_2021': 'Urban Centre and Locality association - 2016 to 2021',
  'RA_2021_AUST': 'Remoteness Areas - 2021'
}

DFS = { file.split('.')[0] : pd.read_csv(f'../local/mb-info/{file}', dtype=str) for file in os.listdir('../local/mb-info')}
# 15s - 30s



# Convert the AREA_ALBERS_SQKM columns to np.float64
# Assert all columns that contains "AREA" are named AREA_ALBERS_SQKM
for df_name, df in DFS.items():
    for col in df.columns:
        if 'AREA' in col:
            assert (col == 'AREA_ALBERS_SQKM' or 'AREA_ALBERS_SQKM_' in col), df_name
            df[col] = df[col].astype(np.float64)


# Check uniqueness of keys. We expect these keys to be the primary keys for the tables
assert DFS['MB_2021_AUST']['MB_CODE_2021'].is_unique
assert DFS['SA1_2021_AUST']['SA1_CODE_2021'].is_unique
assert DFS['SA2_2021_AUST']['SA2_CODE_2021'].is_unique
assert DFS['SA3_2021_AUST']['SA3_CODE_2021'].is_unique
assert DFS['SA4_2021_AUST']['SA4_CODE_2021'].is_unique
assert DFS['GCCSA_2021_AUST']['GCCSA_CODE_2021'].is_unique
assert DFS['STE_2021_AUST']['STATE_CODE_2021'].is_unique
assert DFS['AUS_2021_AUST']['AUS_CODE_2021'].is_unique

assert DFS['INDIGENOUS_STRUCTURE_ALLOCATION_2021']['SA1_CODE_2021'].is_unique
assert DFS['ILOC_2021_AUST']['ILOC_CODE_2021'].is_unique
assert DFS['IARE_2021_AUST']['IARE_CODE_2021'].is_unique
assert DFS['IREG_2021_AUST']['IREG_CODE_2021'].is_unique

assert DFS['LGA_2023_AUST']['MB_CODE_2021'].is_unique
assert DFS['LGA_2022_AUST']['MB_CODE_2021'].is_unique
assert DFS['LGA_2021_AUST']['MB_CODE_2021'].is_unique
assert DFS['SED_2022_AUST']['MB_CODE_2021'].is_unique
assert DFS['SED_2021_AUST']['MB_CODE_2021'].is_unique
assert DFS['CED_2021_AUST']['MB_CODE_2021'].is_unique
assert DFS['POA_2021_AUST']['MB_CODE_2021'].is_unique
assert DFS['ADD_2021_AUST']['MB_CODE_2021'].is_unique
assert DFS['SAL_2021_AUST']['MB_CODE_2021'].is_unique
assert DFS['MB_DZN_2021_AUST']['MB_CODE_2021'].is_unique

assert DFS['DZN_SA2_2021_AUST']['DZN_CODE_2021'].is_unique
assert DFS['TR_2021_AUST']['SA2_CODE_2021'].is_unique
assert DFS['SUA_2021_AUST']['SA2_CODE_2021'].is_unique

assert DFS['RA_2021_AUST']['SA1_CODE_2021'].is_unique

assert DFS['UCL_SOSR_SOS_2021_AUST']['SA1_CODE_2021'].is_unique
assert DFS['UCL_SOSR_SOS_2021_AUST'][['UCL_CODE_2021', 'UCL_NAME_2021', 'SOSR_CODE_2021', 'SOSR_NAME_2021', 'SOS_CODE_2021', 'SOS_NAME_2021', 'STATE_CODE_2021']].drop_duplicates()['UCL_CODE_2021'].is_unique
assert DFS['UCL_SOSR_SOS_2021_AUST'][['SOSR_CODE_2021', 'SOSR_NAME_2021', 'SOS_CODE_2021', 'SOS_NAME_2021', 'STATE_CODE_2021']].drop_duplicates()['SOSR_CODE_2021'].is_unique
assert DFS['UCL_SOSR_SOS_2021_AUST'][['SOS_CODE_2021', 'SOS_NAME_2021', 'STATE_CODE_2021']].drop_duplicates()['SOS_CODE_2021'].is_unique

assert 'SA1_CODE_2021' in DFS['MB_2021_AUST'].columns
assert 'SA2_CODE_2021' in DFS['SA1_2021_AUST'].columns
assert 'SA3_CODE_2021' in DFS['SA2_2021_AUST'].columns
assert 'SA4_CODE_2021' in DFS['SA3_2021_AUST'].columns
assert 'GCCSA_CODE_2021' in DFS['SA4_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['GCCSA_2021_AUST'].columns
assert 'AUS_CODE_2021' in DFS['STE_2021_AUST'].columns

assert 'ILOC_CODE_2021' in DFS['INDIGENOUS_STRUCTURE_ALLOCATION_2021'].columns
assert 'IARE_CODE_2021' in DFS['ILOC_2021_AUST'].columns
assert 'IREG_CODE_2021' in DFS['IARE_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['IREG_2021_AUST'].columns

assert 'LGA_CODE_2023' in DFS['LGA_2023_AUST'].columns
assert 'LGA_CODE_2022' in DFS['LGA_2022_AUST'].columns
assert 'LGA_CODE_2021' in DFS['LGA_2021_AUST'].columns
assert 'SED_CODE_2022' in DFS['SED_2022_AUST'].columns
assert 'SED_CODE_2021' in DFS['SED_2021_AUST'].columns
assert 'CED_CODE_2021' in DFS['CED_2021_AUST'].columns
assert 'POA_CODE_2021' in DFS['POA_2021_AUST'].columns
assert 'ADD_CODE_2021' in DFS['ADD_2021_AUST'].columns
assert 'SAL_CODE_2021' in DFS['SAL_2021_AUST'].columns
assert 'DZN_CODE_2021' in DFS['MB_DZN_2021_AUST'].columns

assert 'SA2_CODE_2021' in DFS['DZN_SA2_2021_AUST'].columns
assert 'TR_CODE_2021' in DFS['TR_2021_AUST'].columns
assert 'SUA_CODE_2021' in DFS['SUA_2021_AUST'].columns
assert 'RA_CODE_2021' in DFS['RA_2021_AUST'].columns
assert 'UCL_CODE_2021' in DFS['UCL_SOSR_SOS_2021_AUST'].columns
assert 'SOSR_CODE_2021' in DFS['UCL_SOSR_SOS_2021_AUST'].columns
assert 'SOS_CODE_2021' in DFS['UCL_SOSR_SOS_2021_AUST'].columns


assert 'STATE_CODE_2021' in DFS['LGA_2023_AUST'].columns
assert 'STATE_CODE_2021' in DFS['LGA_2022_AUST'].columns
assert 'STATE_CODE_2021' in DFS['LGA_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['SED_2022_AUST'].columns
assert 'STATE_CODE_2021' in DFS['SED_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['CED_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['SAL_2021_AUST'].columns

assert 'STATE_CODE_2021' in DFS['MB_DZN_2021_AUST'].columns
assert 'SA2_CODE_2021' in DFS['MB_DZN_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['DZN_SA2_2021_AUST'].columns
assert 'SA2_CODE_2021' in DFS['DZN_SA2_2021_AUST'].columns

assert 'STATE_CODE_2021' in DFS['TR_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['UCL_SOSR_SOS_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['UCL_SOSR_SOS_2021_AUST'].columns
assert 'STATE_CODE_2021' in DFS['RA_2021_AUST'].columns

assert 'STATE_CODE_2021' not in DFS['POA_2021_AUST'].columns
assert 'STATE_CODE_2021' not in DFS['ADD_2021_AUST'].columns
assert 'STATE_CODE_2021' not in DFS['SUA_2021_AUST'].columns

assert 'AUS_CODE_2021' in DFS['POA_2021_AUST'].columns
assert 'AUS_CODE_2021' in DFS['ADD_2021_AUST'].columns
assert 'AUS_CODE_2021' in DFS['SUA_2021_AUST'].columns

assert len(DFS['MB_DZN_2021_AUST'].drop(columns=['MB_CODE_2021', 'AREA_ALBERS_SQKM', 'ASGS_LOCI_URI_2021']).drop_duplicates()) == len(DFS['DZN_SA2_2021_AUST'])
assert DFS['MB_DZN_2021_AUST'].drop(columns=['MB_CODE_2021', 'AREA_ALBERS_SQKM', 'ASGS_LOCI_URI_2021']).drop_duplicates()['DZN_CODE_2021'].is_unique




for df_name, df in DFS.items():
    if 'ASGS_LOCI_URI_2021' in df.columns:
        assert df['ASGS_LOCI_URI_2021'].str.contains('://linked.data.gov.au/dataset/asgsed3/').all()
        if not df['ASGS_LOCI_URI_2021'].is_unique:
            assert df['ASGS_LOCI_URI_2021'].dropna().is_unique
    else:
        print(df_name)
# 5s - 10s
        
# It's safe to remove ASGS_LOCI_URI_2021 from the dataframes, since they are the same as the primary keys
for df_name, df in DFS.items():
    if 'ASGS_LOCI_URI_2021' in df.columns:
        df.drop(columns=['ASGS_LOCI_URI_2021'], inplace=True)
# 2s - 5s
        
# AREA_ALBERS_SQKM is consistent with the primary key, so we can safely remove it from some dataframes
# Proof that AREA_ALBERS_SQKM is consistent with the primary key SA1_CODE_2021 in INDIGENOUS_STRUCTURE_ALLOCATION_2021 and SA1_2021_AUST:
dfindi = pd.merge(DFS['SA1_2021_AUST'], DFS['INDIGENOUS_STRUCTURE_ALLOCATION_2021'], on='SA1_CODE_2021').dropna(subset=['AREA_ALBERS_SQKM_y'])
assert (dfindi['AREA_ALBERS_SQKM_x'] == dfindi['AREA_ALBERS_SQKM_y']).all()

# Not all state codes are in the state table
for df_name, df in DFS.items():
    if 'STATE_CODE_2021' in df.columns:
        if not all(state_code in DFS['STE_2021_AUST']['STATE_CODE_2021'].unique() for state_code in df['STATE_CODE_2021'].unique()):
            print(df_name, 'Not all state codes are in the state table')
            assert df_name in ['MB_DZN_2021_AUST', 'DZN_SA2_2021_AUST']
            # 0&&&&&&&&,,&&&&&&&&&
            # 0@@@@@@@@,,@@@@@@@@@
            # 0VVVVVVVV,,VVVVVVVVV
    else:
        print(df_name, 'No state code')

# There is no Destination Zone Name "DZN_NAME_2021"
assert "DZN_NAME_2021" not in DFS['MB_DZN_2021_AUST'].columns
assert "DZN_NAME_2021" not in DFS['DZN_SA2_2021_AUST'].columns

DF_CHANGE_FLAGS = pd.DataFrame()
for df_name, df in DFS.items():
    if 'CHANGE_FLAG_2021' in df.columns:
        print(df_name, df['CHANGE_FLAG_2021'].unique(), df['CHANGE_LABEL_2021'].unique())
        DF_CHANGE_FLAGS = pd.concat([DF_CHANGE_FLAGS, df[['CHANGE_FLAG_2021', 'CHANGE_LABEL_2021']].drop_duplicates()])
DF_CHANGE_FLAGS.drop_duplicates(inplace=True)
DF_CHANGE_FLAGS.reset_index(drop=True, inplace=True)
assert DF_CHANGE_FLAGS['CHANGE_FLAG_2021'].is_unique

DFS['CHANGE_FLAGS_2021'] = DF_CHANGE_FLAGS

DFS['MB_2021_AUST'] = DFS['MB_2021_AUST'][['MB_CODE_2021', 'MB_CATEGORY_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM', 'SA1_CODE_2021']]

DFS['SA1_2021_AUST'] = DFS['SA1_2021_AUST'][['SA1_CODE_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM', 'SA2_CODE_2021']]

DFS['SA2_2021_AUST'] = DFS['SA2_2021_AUST'][['SA2_CODE_2021', 'SA2_NAME_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM', 'SA3_CODE_2021']]

DFS['SA3_2021_AUST'] = DFS['SA3_2021_AUST'][['SA3_CODE_2021', 'SA3_NAME_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM', 'SA4_CODE_2021']]

DFS['SA4_2021_AUST'] = DFS['SA4_2021_AUST'][['SA4_CODE_2021', 'SA4_NAME_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM', 'GCCSA_CODE_2021']]

DFS['GCCSA_2021_AUST'] = DFS['GCCSA_2021_AUST'][['GCCSA_CODE_2021', 'GCCSA_NAME_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM', 'STATE_CODE_2021']]

DFS['STE_2021_AUST'] = DFS['STE_2021_AUST'][['STATE_CODE_2021', 'STATE_NAME_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM', 'AUS_CODE_2021']]

DFS['AUS_2021_AUST'] = DFS['AUS_2021_AUST'][['AUS_CODE_2021', 'AUS_NAME_2021', 'CHANGE_FLAG_2021', 'AREA_ALBERS_SQKM']]




DFS['MB_ILOC_2021_AUST'] = DFS['INDIGENOUS_STRUCTURE_ALLOCATION_2021'][['SA1_CODE_2021', 'ILOC_CODE_2021']]
DFS['ILOC_2021_AUST'] = DFS['ILOC_2021_AUST'][['ILOC_CODE_2021', 'ILOC_NAME_2021', 'AREA_ALBERS_SQKM', 'IARE_CODE_2021']]
DFS['IARE_2021_AUST'] = DFS['IARE_2021_AUST'][['IARE_CODE_2021', 'IARE_NAME_2021', 'AREA_ALBERS_SQKM', 'IREG_CODE_2021']]
DFS['IREG_2021_AUST'] = DFS['IREG_2021_AUST'][['IREG_CODE_2021', 'IREG_NAME_2021', 'AREA_ALBERS_SQKM', 'STATE_CODE_2021']]

DFS['LGA_2023_AUST'] = DFS['LGA_2023_AUST'][['MB_CODE_2021', 'LGA_CODE_2023', 'LGA_NAME_2023']]
DFS['LGA_2022_AUST'] = DFS['LGA_2022_AUST'][['MB_CODE_2021', 'LGA_CODE_2022', 'LGA_NAME_2022']]
DFS['LGA_2021_AUST'] = DFS['LGA_2021_AUST'][['MB_CODE_2021', 'LGA_CODE_2021', 'LGA_NAME_2021']]
DFS['SED_2022_AUST'] = DFS['SED_2022_AUST'][['MB_CODE_2021', 'SED_CODE_2022', 'SED_NAME_2022']]
DFS['SED_2021_AUST'] = DFS['SED_2021_AUST'][['MB_CODE_2021', 'SED_CODE_2021', 'SED_NAME_2021']]
DFS['CED_2021_AUST'] = DFS['CED_2021_AUST'][['MB_CODE_2021', 'CED_CODE_2021', 'CED_NAME_2021']]
DFS['POA_2021_AUST'] = DFS['POA_2021_AUST'][['MB_CODE_2021', 'POA_CODE_2021', 'POA_NAME_2021']]
DFS['ADD_2021_AUST'] = DFS['ADD_2021_AUST'][['MB_CODE_2021', 'ADD_CODE_2021', 'ADD_NAME_2021']]
DFS['SAL_2021_AUST'] = DFS['SAL_2021_AUST'][['MB_CODE_2021', 'SAL_CODE_2021', 'SAL_NAME_2021']]
DFS['MB_DZN_2021_AUST'] = DFS['MB_DZN_2021_AUST'][['MB_CODE_2021', 'DZN_CODE_2021']]
DFS['DZN_SA2_2021_AUST'] = DFS['DZN_SA2_2021_AUST'][['DZN_CODE_2021', 'AREA_ALBERS_SQKM', 'SA2_CODE_2021']]
DFS['TR_2021_AUST'] = DFS['TR_2021_AUST'][['SA2_CODE_2021', 'TR_CODE_2021', 'TR_NAME_2021']]
DFS['SUA_2021_AUST'] = DFS['SUA_2021_AUST'][['SA2_CODE_2021', 'SUA_CODE_2021', 'SUA_NAME_2021']]
DFS['RA_2021_AUST'] = DFS['RA_2021_AUST'][['SA1_CODE_2021', 'RA_CODE_2021', 'RA_NAME_2021']]
DFS['UCL_SOSR_SOS_2021_AUST'] = DFS['UCL_SOSR_SOS_2021_AUST'][['SA1_CODE_2021', 'UCL_CODE_2021', 'UCL_NAME_2021', 'SOSR_CODE_2021', 'SOSR_NAME_2021', 'SOS_CODE_2021', 'SOS_NAME_2021', 'STATE_CODE_2021', 'STATE_NAME_2021', 'AUS_CODE_2021', 'AUS_NAME_2021', 'AREA_ALBERS_SQKM']]

# 3s - 10s


DFS['MB_LGA_2023_AUST'] = DFS['LGA_2023_AUST'][['MB_CODE_2021', 'LGA_CODE_2023']]
DFS['LGA_2023_AUST'] = DFS['LGA_2023_AUST'][['LGA_CODE_2023', 'LGA_NAME_2023']].drop_duplicates()

DFS['MB_LGA_2022_AUST'] = DFS['LGA_2022_AUST'][['MB_CODE_2021', 'LGA_CODE_2022']]
DFS['LGA_2022_AUST'] = DFS['LGA_2022_AUST'][['LGA_CODE_2022', 'LGA_NAME_2022']].drop_duplicates()

DFS['MB_LGA_2021_AUST'] = DFS['LGA_2021_AUST'][['MB_CODE_2021', 'LGA_CODE_2021']]
DFS['LGA_2021_AUST'] = DFS['LGA_2021_AUST'][['LGA_CODE_2021', 'LGA_NAME_2021']].drop_duplicates()

DFS['MB_SED_2022_AUST'] = DFS['SED_2022_AUST'][['MB_CODE_2021', 'SED_CODE_2022']]
DFS['SED_2022_AUST'] = DFS['SED_2022_AUST'][['SED_CODE_2022', 'SED_NAME_2022']].drop_duplicates()

DFS['MB_SED_2021_AUST'] = DFS['SED_2021_AUST'][['MB_CODE_2021', 'SED_CODE_2021']]
DFS['SED_2021_AUST'] = DFS['SED_2021_AUST'][['SED_CODE_2021', 'SED_NAME_2021']].drop_duplicates()

DFS['MB_CED_2021_AUST'] = DFS['CED_2021_AUST'][['MB_CODE_2021', 'CED_CODE_2021']]
DFS['CED_2021_AUST'] = DFS['CED_2021_AUST'][['CED_CODE_2021', 'CED_NAME_2021']].drop_duplicates()

DFS['MB_POA_2021_AUST'] = DFS['POA_2021_AUST'][['MB_CODE_2021', 'POA_CODE_2021']]
DFS['POA_2021_AUST'] = DFS['POA_2021_AUST'][['POA_CODE_2021', 'POA_NAME_2021']].drop_duplicates()

DFS['MB_ADD_2021_AUST'] = DFS['ADD_2021_AUST'][['MB_CODE_2021', 'ADD_CODE_2021']]
DFS['ADD_2021_AUST'] = DFS['ADD_2021_AUST'][['ADD_CODE_2021', 'ADD_NAME_2021']].drop_duplicates()

DFS['MB_SAL_2021_AUST'] = DFS['SAL_2021_AUST'][['MB_CODE_2021', 'SAL_CODE_2021']]
DFS['SAL_2021_AUST'] = DFS['SAL_2021_AUST'][['SAL_CODE_2021', 'SAL_NAME_2021']].drop_duplicates()

DFS['SA2_TR_2021_AUST'] = DFS['TR_2021_AUST'][['SA2_CODE_2021', 'TR_CODE_2021']]
DFS['TR_2021_AUST'] = DFS['TR_2021_AUST'][['TR_CODE_2021', 'TR_NAME_2021']].drop_duplicates()

DFS['MB_DZN_2021_AUST'] = DFS['MB_DZN_2021_AUST'][['MB_CODE_2021', 'DZN_CODE_2021']]
DFS['DZN_SA2_2021_AUST'] = DFS['DZN_SA2_2021_AUST'][['DZN_CODE_2021', 'AREA_ALBERS_SQKM', 'SA2_CODE_2021']]

DFS['SA2_SUA_2021_AUST'] = DFS['SUA_2021_AUST'][['SA2_CODE_2021', 'SUA_CODE_2021']]
DFS['SUA_2021_AUST'] = DFS['SUA_2021_AUST'][['SUA_CODE_2021', 'SUA_NAME_2021']].drop_duplicates()

DFS['SA1_RA_2021_AUST'] = DFS['RA_2021_AUST'][['SA1_CODE_2021', 'RA_CODE_2021']]
DFS['RA_2021_AUST'] = DFS['RA_2021_AUST'][['RA_CODE_2021', 'RA_NAME_2021']].drop_duplicates()

DFS['SA1_UCL_2021_AUST'] = DFS['UCL_SOSR_SOS_2021_AUST'][['SA1_CODE_2021', 'UCL_CODE_2021']].drop_duplicates()

DFS['UCL_2021_AUST'] = DFS['UCL_SOSR_SOS_2021_AUST'][['UCL_CODE_2021', 'UCL_NAME_2021', 'SOSR_CODE_2021']].drop_duplicates()
DFS['SOSR_2021_AUST'] = DFS['UCL_SOSR_SOS_2021_AUST'][['SOSR_CODE_2021', 'SOSR_NAME_2021', 'SOS_CODE_2021']].drop_duplicates()
DFS['SOS_2021_AUST'] = DFS['UCL_SOSR_SOS_2021_AUST'][['SOS_CODE_2021', 'SOS_NAME_2021']].drop_duplicates()

# 1s - 3s


for df_name, df in DFS.items():
    df.reset_index(drop=True, inplace=True)

# Remove INDIGENOUS_STRUCTURE_ALLOCATION_2021, UCL_SOSR_SOS_2021_AUST
for df_name in ['INDIGENOUS_STRUCTURE_ALLOCATION_2021', 'UCL_SOSR_SOS_2021_AUST']:
    del DFS[df_name]


os.makedirs('../data/mb-info', exist_ok=True)

for df_name, df in DFS.items():
    df.to_csv(f'../data/mb-info/{df_name}.csv', index=False)


