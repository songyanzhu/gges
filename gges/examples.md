### Converting a DataFrame to a GeoDataFrame

In spatial data science, tabular data containing coordinates (such as a pandas `DataFrame` with latitude and longitude columns) needs to be converted into a `GeoDataFrame` to perform spatial operations, overlay analysis, or export to standard GIS formats (e.g., GeoJSON, Shapefile).

```python
import pandas as pd
import geopandas as gpd

# Example: assuming 'df' is a pandas DataFrame with coordinate columns
# df = pd.DataFrame({
#     "name": ["Point A", "Point B"],
#     "latitude": [50.9388, 50.9069],
#     "longitude": [-1.3995, -1.4087]
# })

# Convert pandas DataFrame to GeoDataFrame (WGS84 / EPSG:4326)
gdf = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df.longitude, df.latitude), 
    crs="EPSG:4326"
)

# Inspect spatial metadata and geometry
print(gdf.head())
print("Coordinate Reference System:", gdf.crs)
```

> **Key Notes:**
> * `gpd.points_from_xy()` strictly follows the **(X, Y)** convention, which maps to **(longitude, latitude)**.
> * `crs="EPSG:4326"` assigns the standard World Geodetic System 1984 (WGS84) geographic coordinate system.