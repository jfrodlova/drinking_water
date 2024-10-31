import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
from shapely.geometry import Point

# Load the text file and create a DataFrame
df = pd.read_csv('locations_unique_cleaned.txt', header=None, names=['Collection_point'])

# Fetch GPS for the collection points in the dataframe
for index, row in df.iterrows():
    try:
        information = geocode(row['Collection_point'], provider = 'nominatim', user_agent = 'xyz', timeout = 5)
        df.loc[index, 'Longitude'] = information.geometry.loc[0].x
        df.loc[index, 'Latitude'] = information.geometry.loc[0].y
        
    except Exception as e:
        print(f"Geocoding failed for {row['Collection_point']}: {e}")
        df.loc[index, 'Longitude'] = None
        df.loc[index, 'Latitude'] = None

# Convert the DataFrame to a GeoDataFrame with points
gdf_points = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
    crs="EPSG:4326" 
)

# Load the shapefile (shapefile.json) for districts and regions
gdf_boundaries = gpd.read_file("shapefile.json", encoding="utf-8")
gdf_boundaries.crs = "EPSG:4326"

# Perform spatial join to find the district and region for each collection point
gdf_joined = gpd.sjoin(gdf_points, gdf_boundaries, how="left", predicate="within")

# Create a final DataFrame with the desired columns
final_df = gdf_joined[['Collection_point', 'Longitude', 'Latitude', 'NAZ_LAU1', 'NAZ_CZNUTS3']].copy()
final_df.rename(columns={'NAZ_LAU1': 'District_name', 'NAZ_CZNUTS3': 'Region_name'}, inplace=True)

# Save the final DataFrame to CSV
final_df.to_csv('locations_gps_table.csv', index=False, encoding="utf-8")
