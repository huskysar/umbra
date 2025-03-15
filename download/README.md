# Downloading Umbra orders

Requires an environment with `pystac-client` and `stac-asset`

- https://pystac-client.readthedocs.io/en/stable/quickstart.html#cli
- https://github.com/stac-utils/stac-asset?tab=readme-ov-file#cli

Also benefits from having `jq` installed for nice JSON formatting (https://jqlang.org/download/)

## Ensure you have the pixi environment active first & set environment variables
```
pixi shell
# NOTE: trailing slash seems to matter here!
export STAC_API_URL=https://api.canopy.umbra.space/v2/stac/
export UMBRA_API_TOKEN=xxxxx
```

## Check endpoint & auth
```
stac-client collections $STAC_API_URL --headers authorization="Bearer ${UMBRA_API_TOKEN}" | jq
```

## Basic search

Note: it seems other flags need to come after '--headers', this searches all orders in your organization
```
stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --max-items 1 | jq
```

### specific ID search
Umbra uses at least 3 different IDs (STAC ID, task ID, collect ID), be sure to use the STAC ID:
```
stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --ids 855f94e8-6d9b-4586-af13-b12053d905d1 | jq
```

### bbox search

Output results to a FeatureCollection GeoJSON
```
stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --bbox -124.84 24.39 -66.88 49.38 --save items.json
```

### datetime search
```
stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --datetime 2024-11-06 | jq '.features[].properties'
```

### geometry search

Just report properties, or ids etc: (.features[].id, .features[].properties, .features[].properties["umbra:task_id"])
```
stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --intersects ../utqiagvik.geojson | jq '.features[].properties["umbra:task_id"]'
```

### filtering by properties

--query is shorthand and --filter is full CQL2 filtering (via JSON)
#### task ID
Note: umbra:task_id not same as "umbra:collect_id" or STAC "id"
```
stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --query "umbra:task_id=$TASKID" | jq '.features[].assets | keys[]'
```

#### resolution
pipe to `wc` to quickly count the number of matches
```
stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --query "sar:resolution_range=1.0" | jq '.features[].id' | wc

stac-client search $STAC_API_URL --headers "authorization=Bearer $UMBRA_API_TOKEN" --filter='{"op": "=", "args": [{"property": "sar:looks_azimuth"}, 1]}' | jq '.features[].id' | wc
```

**IMPORTANT The API only returns SIGNED URLs for downloading for 5 or less STACIDs**

### DOWNLOAD

#### GEC

By default downloads to current working directory
```
stac-client search $STAC_API_URL \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --query "umbra:task_id=644cc5e9-8702-44d8-a154-235d3c8233f2" \
   | stac-asset download -i "2024-10-28-19-13-59_UMBRA-08_MM.tif" --alternate-assets s3_signed | jq
```

or by STAC ID instead of task_id:
```
stac-client search $STAC_API_URL \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --ids 19800433-b6f8-40ef-aa9e-7c51f384c638 \
   | stac-asset download \
      -p /tmp/2025-03-13-06-17-26_UMBRA-08_MM \
      -i "2025-03-13-06-17-26_UMBRA-08_MM.tif" \
      --http-timeout 1200 \
      --alternate-assets s3_signed | jq
```


#### SICD
NOTE specifying custom output folder name with -p (otherwise uses STAC Item ID by default)
```
stac-client search $STAC_API_URL \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --query "umbra:task_id=42015e8e-9cdf-4c7c-b040-3c4537a81137" \
   | stac-asset download \
      -p /tmp/2025-03-09-19-16-09_UMBRA-08 \
      -i "2025-03-09-19-16-09_UMBRA-08_SICD_MM.nitf" \
      --http-timeout 1200 \
      --alternate-assets s3_signed | jq
```

### Download everything but CPHD

Note: had to increase max time to 20min (1200s) downloading from US via wifi in Germany :)
```
stac-client search $STAC_API_URL \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --query "umbra:task_id=644cc5e9-8702-44d8-a154-235d3c8233f2" \
   | stac-asset download \
       --exclude "2024-10-28-19-13-59_UMBRA-08_MM.cphd" \
       --alternate-assets s3_signed \
       --http-timeout 1200
```
