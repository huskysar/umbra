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

Browse commit
https://relativeorbit.github.io/stac-browser/#/external/raw.githubusercontent.com/huskysar/umbra/0dfc3ac0578ef89c72df13cfeb5ca38c2ccbc469/stacbrowse/panama-canal-gec/catalog.json



# Troubleshoot titile woahs

http://umbra-open-data-catalog.s3.amazonaws.com/sar-data/tasks/Panama Canal, Panama/fac35699-2f8d-4c28-ab5e-638182373f34/2024-02-17-15-00-05_UMBRA-04/2024-02-17-15-00-05_UMBRA-04_GEC.tif

http://umbra-open-data-catalog.s3.amazonaws.com/sar-data/tasks/Panama%20Canal%2C%20Panama/fac35699-2f8d-4c28-ab5e-638182373f34/2024-02-17-15-00-05_UMBRA-04/2024-02-17-15-00-05_UMBRA-04_GEC.tif

https://titiler.xyz/cog/WebMercatorQuad/map?tile_scale=1&url=http%3A%2F%2Fumbra-open-data-catalog.s3.amazonaws.com%2Fsar-data%2Ftasks%2FPanama%2520Canal%252C%2520Panama%2Ffac35699-2f8d-4c28-ab5e-638182373f34%2F2024-02-17-15-00-05_UMBRA-04%2F2024-02-17-15-00-05_UMBRA-04_GEC.tif

-> requests that look like this:

https://titiler.xyz/cog/tiles/WebMercatorQuad/13/2284/3890@1x?url=http%3A%2F%2Fumbra-open-data-catalog.s3.amazonaws.com%2Fsar-data%2Ftasks%2FPanama%2520Canal%252C%2520Panama%2Ffac35699-2f8d-4c28-ab5e-638182373f34%2F2024-02-17-15-00-05_UMBRA-04%2F2024-02-17-15-00-05_UMBRA-04_GEC.tif


https://titiler.xyz/cog/tiles/WebMercatorQuad/13/2284/3890@1x?url=http%3A%2F%2Fumbra-open-data-catalog.s3.amazonaws.com%2Fsar-data%2Ftasks%2FPanama%20Canal%2C%20Panama%2Ffac35699-2f8d-4c28-ab5e-638182373f34%2F2024-02-17-15-00-05_UMBRA-04%2F2024-02-17-15-00-05_UMBRA-04_GEC.tif


Go via URL decode encode
http%3A%2F%2Fumbra-open-data-catalog.s3.amazonaws.com%2Fsar-data%2Ftasks%2FPanama%20Canal%2C%20Panama%2Ffac35699-2f8d-4c28-ab5e-638182373f34%2F2024-02-17-15-00-05_UMBRA-04%2F2024-02-17-15-00-05_UMBRA-04_GEC.tif

Compare to titiler... hmm whate is %2520 -> %20 which is a spaceT
http%3A%2F%2Fumbra-open-data-catalog.s3.amazonaws.com%2Fsar-data%2Ftasks%2FPanama%2520Canal%252C%2520Panama%2Ffac35699-2f8d-4c28-ab5e-638182373f34%2F2024-02-17-15-00-05_UMBRA-04%2F2024-02-17-15-00-05_UMBRA-04_GEC.tif


https://titiler.xyz/cog/tiles/WebMercatorQuad/13/2284/3890@1x?url=http%3A%2F%2Fumbra-open-data-catalog.s3.amazonaws.com%2Fsar-data%2Ftasks%2FPanama%2520Canal%252C%2520Panama%2Ffac35699-2f8d-4c28-ab5e-638182373f34%2F2024-02-17-15-00-05_UMBRA-04%2F2024-02-17-15-00-05_UMBRA-04_GEC.tif
