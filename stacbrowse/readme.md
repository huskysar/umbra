# Customized STAC Browser for public data

Umbra's open data program is great, but currently the 'browseable' static catalog does not match dynamically generated metdata from their search:


https://radiantearth.github.io/stac-browser/#/external/s3.us-west-2.amazonaws.com/umbra-open-data-catalog/stac/catalog.json?.language=en

vs

https://docs.canopy.umbra.space/docs/archive-catalog-searching-via-stac-api

https://docs.canopy.umbra.space/docs/archive-catalog-searching-via-stac-api#finding-data-in-the-umbra-open-data-s3-bucket


Maybe this will be fixed by Umbra at some point... Until then, this folder has an example of creating a new public static STAC catalog for a particular site, adding additional metadata fields of interest.

## Additional useful metadata (not implemented yet...)


We'll retrieve this by actually reading TIFs & Metadata JSONs for each item
* proj extension
* assets + roles
```
"sat:orbit_state": str #ascending/descending
"sar:observation_direction': str #left/right
"sar:center_frequency": float # Hz
"umbra:sceneSize": "5x5_KM" # or 4x4KM
"huskysar:duration": float # s
"huskysar:rpcs": bool # weather or not RPCs in TIFs
"huskysar:dayofyear: int # day
"processing:software": {
    "Umbra SAR Processor": "2.61.0" # example
    },
"locale:datetime": "2024-09-21T22:19:34.112664-0600", # looked up based on lon/lat of point
#"umbra:image_formation_algorithm": "PFA" #  Polar Format Algorithm?
```

## Browsing

Point STACBrowser at this static catalog:
https://raw.githubusercontent.com/huskysar/umbra/main/stacbrowse/panama-canal/catalog.json

Like this!
https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/huskysar/umbra/main/stacbrowse/panama-canal/catalog.json

Or this (our own stacbrowser w/ titiler for rendering instead of geotiff.js)
https://relativeorbit.github.io/stac-browser/#/external/raw.githubusercontent.com/huskysar/umbra/main/stacbrowse/panama-canal-gec/catalog.json
