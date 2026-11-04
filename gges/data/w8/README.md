# Week 8 Data

All files are supplied locally in `data/w8/`. Students do not need to download data or use an API key.

| File | Contents | Source |
|---|---|---|
| `london_weather_stations.csv` | Names, IDs and coordinates of six London-area weather stations | NOAA/NCEI |
| `london_weather_hourly_2024.csv` | Cleaned hourly weather observations for 2024 | NOAA/NCEI Global Hourly (ISD) |
| `london_boundary.geojson` | London administrative boundary | Supplied teaching boundary |
| `london_boroughs.geojson` | London borough boundaries and names | Greater London Authority / London Datastore |
| `london_thames_edges.geojson` | Thames water-body edges for mapping and distance calculations | Derived from Environment Agency water-body polygons |
| `station_landcover_2021.csv` | Station names, land-cover names and class codes at station locations | ESA WorldCover 2021, retrieved through Google Earth Engine |
| `london_landsat8/*.tif` | Annual mean red and near-infrared reflectance for 2016 - 2025 | Landsat 8 Collection 2 Level 2, processed through Google Earth Engine |

## Notes

- Keep station IDs as strings to preserve leading zeros.
- Missing values remain missing unless explicitly excluded from an analysis.
- Each Landsat raster contains **Band 1: red** and **Band 2: near-infrared (NIR)**, with reflectance scaling already applied.
- Raster filenames identify the year of the annual composite, not a single image acquisition date.
- The notebook calculates the Two-band Enhanced Vegetation Index (EVI2) from annual mean reflectance. This differs from averaging EVI2 calculated for individual images.
- Land cover represents one raster pixel at each station in **2021**, whereas weather observations cover **2024**.
- Thames edge distances do not represent distances to a river centreline or access point.
- Keep only the three input rasters in `london_landsat8/`: the notebook reads every `.tif` in this folder.

## Sources

- [NOAA/NCEI Global Hourly](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database)
- [London borough boundaries](https://data.london.gov.uk/dataset/london_boroughs_515)
- [Environment Agency Catchment Data Explorer](https://environment.data.gov.uk/catchment-planning/)
- [ESA WorldCover 2021](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200)
- [Landsat 8 Collection 2 Level 2](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2)