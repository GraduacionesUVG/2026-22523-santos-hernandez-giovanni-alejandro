import geopandas as gpd

archivo_entrada = "gtm_admin2.geojson"

gdf = gpd.read_file(archivo_entrada)

amg_gdf = gdf[gdf['adm1_pcode'] == 'GT01']

archivo_salida = "amg_limites.geojson"
amg_gdf.to_file(archivo_salida, driver="GeoJSON")

bbox = amg_gdf.total_bounds
conteo_municipios = len(amg_gdf)

print(f"Archivo exportado exitosamente como: {archivo_salida}")
print(f"Total de municipios filtrados: {conteo_municipios}")
print(f"Bounding Box para Sentinel Hub [min_lon, min_lat, max_lon, max_lat]:\n{bbox}")