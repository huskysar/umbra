# Downloading Umbra orders

Requires an environment with `pystac-client` and `stac-asset`

- https://pystac-client.readthedocs.io/en/stable/quickstart.html#cli
- https://github.com/stac-utils/stac-asset?tab=readme-ov-file#cli


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
stac-client search https://api.canopy.umbra.space/v2/stac/ --headers "authorization=Bearer $UMBRA_API_TOKEN" --query "umbra:task_id=644cc5e9-8702-44d8-a154-235d3c8233f2"
```

### Download a specific asset from an order
```
stac-client search https://api.canopy.umbra.space/v2/stac/ \
   --headers "authorization=Bearer $UMBRA_API_TOKEN" \
   --query "umbra:task_id=644cc5e9-8702-44d8-a154-235d3c8233f2" \
   | stac-asset download -i "2024-10-28-19-13-59_UMBRA-08_MM.tif" --alternate-assets s3_signed
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
