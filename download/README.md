# Downloading Umbra orders

Requires an environment with `pystac-client` and `stac-asset`

- https://pystac-client.readthedocs.io/en/stable/quickstart.html#cli
- https://github.com/stac-utils/stac-asset?tab=readme-ov-file#cli

Also benefits from having `jq` installed for nice JSON formatting (https://jqlang.org/download/)

## Ensure you have the pixi environment active first
```
pixi shell
```

## Check endpoint & auth
```
export UMBRA_API_TOKEN=xxxxx
stac-client collections https://api.canopy.umbra.space/v2/stac/ --headers authorization="Bearer ${UMBRA_API_TOKEN}" | jq
```

## Basic search

Note: it seems other flags need to come after '--headers'
```
stac-client search https://api.canopy.umbra.space/v2/stac/ --headers "authorization=Bearer $UMBRA_API_TOKEN" --max-items 1 | jq
```

## Bbox search
```
stac-client search https://api.canopy.umbra.space/v2/stac/ --headers "authorization=Bearer $UMBRA_API_TOKEN" --bbox -124.84 24.39 -66.88 49.38 --save items.json
```

## Specific order ID search

Note: umbra:task_id not same as "umbra:collect_id" or STAC "id"
```
stac-client search https://api.canopy.umbra.space/v2/stac/ --headers "authorization=Bearer $UMBRA_API_TOKEN" --query "umbra:task_id=644cc5e9-8702-44d8-a154-235d3c8233f2" | jq '.features[].assets | keys[]'
```

### Download a specific asset from an order

#### GEC
```
stac-client search https://api.canopy.umbra.space/v2/stac/ \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --query "umbra:task_id=644cc5e9-8702-44d8-a154-235d3c8233f2" \
   | stac-asset download -i "2024-10-28-19-13-59_UMBRA-08_MM.tif" --alternate-assets s3_signed
```

#### SICD
NOTE specifying custom output folder name with -p (otherwise uses STAC Item ID by default)
```
stac-client search https://api.canopy.umbra.space/v2/stac/ \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --query "umbra:task_id=42015e8e-9cdf-4c7c-b040-3c4537a81137" \
   | stac-asset download -p /tmp/2025-03-09-19-16-09_UMBRA-08 -i "2025-03-09-19-16-09_UMBRA-08_SICD_MM.nitf" --alternate-assets s3_signed
```

### Download everything but CPHD

Note: had to increase max time to 20min (1200s) downloading from US via wifi in Germany :)
```
stac-client search https://api.canopy.umbra.space/v2/stac/ \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --query "umbra:task_id=644cc5e9-8702-44d8-a154-235d3c8233f2" \
   | stac-asset download \
       --exclude "2024-10-28-19-13-59_UMBRA-08_MM.cphd" \
       --alternate-assets s3_signed \
       --http-timeout 1200
```
