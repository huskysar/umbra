# umbra

Code related to NASA CSDAP Umbra Project

## environment management

We use pixi.sh to manage the Python environment required to execute code and notebooks in this repository:

```
cd umbra
pixi install
```

## authentication

Set the following environment variables
```
# NOTE: currently sandbox token doesn't work for search, use standard token
export UMBRA_API_TOKEN="aaaaa"

export SPACETRACK_USER="bbbbb"
export SPACETRACK_PASS="ccccc"
```