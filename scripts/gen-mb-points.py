
import pandas as pd
import geopandas as gpd
import shapely.geometry as geom
import numpy as np
import json
import os



gdf : gpd.GeoDataFrame = gpd.read_file('local/MB_2021_AUST_SHP_GDA2020/MB_2021_AUST_GDA2020.shp')
# 4m - 9m


gdf : gpd.GeoDataFrame = gdf[['MB_CODE21', 'geometry']].rename(columns={'MB_CODE21': 'id'})


gdfn : gpd.GeoDataFrame = gdf.dropna().copy()
# 10s


gdf_geom : gpd.GeoSeries = gdfn.boundary
# 30s


# Combine multiple linestring and multilinestring geometries into single multilinestring geometry
gdml = gdf_geom.apply(lambda x: geom.MultiLineString([x]) if isinstance(x, geom.LineString) else x)
# 1m
# 30s


gdfn['multilinestring'] = gdml


gdfn['line_order'] = gdfn['multilinestring'].apply(lambda x: np.array(range(len(x.geoms))))
# 15s


gdfn['linestring'] = gdfn['multilinestring'].apply(lambda x: x.geoms)
# 5s


gd_line_order = gdfn[['id', 'line_order']].explode('line_order')
# 1m 30s


gd_linestring = gdfn['linestring'].explode()
# 1m


df_lines = pd.concat([gd_line_order, gd_linestring], axis=1)


df_lines['linestring'] = df_lines['linestring'].apply(lambda x: np.array(x.coords))
# 30s - 1m


df_points = df_lines.explode('linestring')
# 4m


# Split the linestring into lon and lat
df_points['lon'] = df_points['linestring'].apply(lambda x: x[0])
df_points['lat'] = df_points['linestring'].apply(lambda x: x[1])
# 3m - 4m

df_points['point_order'] = df_lines['linestring'].apply(lambda x: np.array(range(len(x)))).explode()
# 30s - 1m


df_points = df_points[['id', 'line_order', 'point_order', 'lon', 'lat']]
# 30s - 1m


os.makedirs('data/mb-points', exist_ok=True)


df_points['id5'] = df_points['id'].str[:5]
# 30s - 1m30s


df_points['id5'].value_counts()


df_points.groupby('id5').apply(lambda x: x[['id', 'line_order', 'point_order', 'lon', 'lat']].to_csv(f'data/mb-points/mb-{x.name}.csv', index=False))
# 7m -8m


