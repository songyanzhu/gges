# Examples

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


---


### Shortest Network Distance Analysis to Greenspaces

In spatial accessibility analysis, straight-line (Euclidean) distance often underestimates travel effort across urban environments. By building a topological road network graph with `momepy` and `networkx`, we compute the exact network routing distance from student accommodations to a specified destination (e.g., an urban park).

```python
import geopandas as gpd
import momepy
import networkx as nx
from shapely.geometry import Point, LineString

# ---------------------------------------------------------
# 1. Coordinate Transformation to Projected CRS (EPSG:27700, Unit: Metres)
# ---------------------------------------------------------
target_crs = "EPSG:27700"

# Filter to the first accommodation record for evaluation
student_accommodations = student_accommodations_r.iloc[[0], :].copy()

# Reproject all spatial datasets to the British National Grid (BNG)
roads_proj = roads.to_crs(target_crs)
student_acc_proj = student_accommodations.to_crs(target_crs)
greenspace_proj = greenspace.to_crs(target_crs)

# ---------------------------------------------------------
# 2. Construct Topological Graph from Road Network
# ---------------------------------------------------------
# Convert LineString GeoDataFrame to a NetworkX Graph using segment length as edge weight
graph = momepy.gdf_to_nx(roads_proj, approach="primal", length="length")

# Extract graph nodes as a GeoDataFrame for spatial queries
nodes, edges = momepy.nx_to_gdf(graph)

# ---------------------------------------------------------
# 3. Target Greenspace Selection and Node Snapping
# ---------------------------------------------------------
target_park_name = "Mayflower Park"
target_green = greenspace_proj[greenspace_proj["name"] == target_park_name].iloc[0].geometry

# Extract boundary/exterior to find the closest network entry point
target_boundary = target_green.exterior if hasattr(target_green, "exterior") else target_green

# Identify the nearest network node to the target greenspace
nearest_node_idx = nodes.distance(target_green).idxmin()
target_node = nodes.loc[nearest_node_idx, "geometry"].coords[0]

# ---------------------------------------------------------
# 4. Shortest Network Path Computation
# ---------------------------------------------------------
distances = []
paths_geometry = []

for idx, accomm in student_acc_proj.iterrows():
    pt = accomm.geometry
    
    # Snap the origin point to the nearest road network node
    start_node_idx = nodes.distance(pt).idxmin()
    start_node = nodes.loc[start_node_idx, "geometry"].coords[0]
    
    # Calculate first-mile Euclidean distance (origin to nearest node)
    dist_first_mile = pt.distance(nodes.loc[start_node_idx, "geometry"])
    
    try:
        # Compute shortest network distance along graph edges
        network_dist = nx.shortest_path_length(
            graph, 
            source=start_node, 
            target=target_node, 
            weight="length"
        )
        total_dist = network_dist + dist_first_mile
        
        # Reconstruct path geometry as LineString
        path_nodes = nx.shortest_path(graph, source=start_node, target=target_node, weight="length")
        path_geom = LineString(path_nodes)
    except nx.NetworkXNoPath:
        # Handle disconnected subgraphs or dead-ends
        total_dist = None
        path_geom = None

    distances.append(total_dist)
    paths_geometry.append(path_geom)

# ---------------------------------------------------------
# 5. Append Results to GeoDataFrame
# ---------------------------------------------------------
student_accommodations[f"dist_to_{target_park_name}_m"] = distances

# Inspect computed routing distances
print(student_accommodations[["name", "type", "postcode", f"dist_to_{target_park_name}_m"]])
```

> **Key Notes:**
> * **Projected Coordinate Reference System (CRS)**: Distance calculations must be executed on a metric projected CRS (such as `EPSG:27700`) rather than angular geographic coordinates (`EPSG:4326`).
> * **First-Mile Metric**: Snapping a point directly to graph nodes introduces an offset; adding the Euclidean distance from the origin to the nearest node accounts for the initial access penalty.