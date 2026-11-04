# Week 8 data

All observation and geometry files are supplied locally. Students do not need to download data or use an API key.

| File | Contents | Source |
|---|---|---|
| `london_weather_hourly_2024.csv` | Cleaned hourly observations for six London-area stations in 2024 | NOAA/NCEI Global Hourly (ISD) |
| `london_weather_stations.csv` | Station names, IDs, coordinates and teaching subset flag | NOAA/NCEI station history and Global Hourly |
| `london_weather_coverage_2024.csv` | Coverage summary | Derived from the supplied NOAA observations |
| `london_boroughs.geojson` | 33 London borough polygons | Greater London Authority / London Datastore |
| `london_green_sites.csv` | Coordinates of three named London green spaces | Teaching site list using real locations |
| `london_modis_gpp_weather_2024.csv` | MODIS EVI and GPP joined to nearby NOAA weather | NASA MODIS via ORNL DAAC TESViS; NOAA/NCEI |
| `station_region_lookup_incomplete.csv` | A deliberately incomplete teaching lookup | Derived categories; London City is intentionally omitted so students can diagnose a missing attribute match |

Notes:

- Missing values remain missing unless the notebook explicitly removes them for a stated analysis.
- Rain is labelled `rain` when the supplied hourly precipitation is greater than 0 mm.
- The MODIS table uses 16-day EVI matched to 8-day GPP periods and nearby-station weather summaries. It is a small teaching dataset, not a definitive ecological model.
- Source pages: https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database ; https://data.london.gov.uk/dataset/london_boroughs_515 ; https://modis.ornl.gov/data/modis_webservice.html
