# UMBRA

Code related to NASA CSDAP [Umbra Space](https://umbra.space) evaluation 

## environment management

We recommend using [pixi.sh](https://pixi.sh/latest/) to manage the Python environment required to execute code and notebooks in this repository

```
cd umbra
pixi install
```

Alternatively you can use conda/mamba:
```
conda env create -f environment.yml
```

## authentication

Set the following environment variables
```
# NOTE: currently sandbox token doesn't work for search, use standard token
export UMBRA_API_TOKEN="aaaaa"

export SPACETRACK_USER="bbbbb"
export SPACETRACK_PASS="ccccc"
```