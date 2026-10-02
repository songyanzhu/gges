import numpy as np
import rioxarray as rxr
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from shapely.geometry import Point

def load_tif(p, band_names, reproj = False, decode_times = True, epsg = "EPSG:4326"):
    """
    Load tif to xarray with rioxarray
    """
    rnc = rxr.open_rasterio(p, band_as_variable = True, decode_times = decode_times)
    if reproj:
        rnc = rnc.rio.reproject(epsg)
    name_dict = dict(zip(rnc.keys(), band_names))
    name_dict.update({'x': 'longitude', 'y': 'latitude'})
    rnc = rnc.rename(name_dict)
    return rnc


def clip(raster, boundary, epsg = '4326'):
    """
    Clip raster to boundary
    """
    clipped = raster.rio.write_crs(f"epsg:{epsg}", inplace = False).rio.clip(boundary.geometry.values, boundary.crs)
    return clipped

def generate_random_points(boundary, epsg=27700, num_points=100):
    """
    Generate random points within a given boundary polygon.

    Parameters:
    boundary (GeoDataFrame): A GeoDataFrame containing the boundary polygon.
    num_points (int): The number of random points to generate.

    Returns:
    GeoDataFrame: A GeoDataFrame containing the generated random points.
    """

    # Read the Southampton boundary and use coordinates in metres
    boundary = boundary.to_crs(epsg=epsg)

    # Combine all boundary polygons
    region = boundary.geometry.unary_union
    xmin, ymin, xmax, ymax = region.bounds

    # Generate random points inside the boundary
    rng = np.random.default_rng(42)
    points = []

    while len(points) < num_points:
        x = rng.uniform(xmin, xmax)
        y = rng.uniform(ymin, ymax)
        point = Point(x, y)

        if region.contains(point):
            points.append(point)

    # Create a GeoDataFrame
    random_points = gpd.GeoDataFrame(
        {"ID": range(1, len(points) + 1)},
        geometry=points,
        crs=boundary.crs
    )

    return random_points.set_index('ID')


def plot_land_cover(da, shp, ax):
    """
    Plot land cover data with custom colormap and labels.

    Parameters:
    da (xarray.DataArray): The land cover data to plot.
    shp (GeoDataFrame): The boundary shapefile to overlay on the plot.
    ax (matplotlib.axes.Axes): The axes on which to plot the data.
    """
    # Define land cover values and labels
    lc_values = list(range(9))
    lc_colors = [
        "#419bdf",  # water
        "#397d49",  # trees
        "#88b053",  # grass
        "#7a87c6",  # flooded vegetation
        "#e49635",  # crops
        "#dfc35a",  # shrub and scrub
        "#c4281b",  # built
        "#a59b8f",  # bare
        "#b39fe1",  # snow and ice
    ]
    lc_labels = [
        "water", "trees", "grass", "flooded", "crops",
        "shrub", "built", "bare", "snow & ice"
    ]

    # Create a custom colormap and normalization
    cmap = mcolors.ListedColormap(lc_colors)
    norm = mcolors.BoundaryNorm(boundaries=np.arange(-0.5, 9.5), ncolors=len(lc_colors))

    im = da.plot(
        ax = ax,
        cmap=cmap, norm=norm, add_colorbar=False
    )
    cbar = plt.colorbar(im, ticks=lc_values, shrink=0.8)
    cbar.ax.set_yticklabels(lc_labels)
    shp.plot(ax = ax, color = 'none', edgecolor = 'black')
    return ax, im
