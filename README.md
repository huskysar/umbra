# UMBRA

Code related to NASA CSDAP [Umbra Space](https://umbra.space) evaluation

## rendered notebooks

1. [Order Summary](https://nbviewer.org/github/huskysar/umbra/blob/main/notebooks/order_summary.ipynb)
1. [Public Archive Search](https://nbviewer.org/github/huskysar/umbra/blob/main/notebooks/public-archive-search.ipynb)
1. [Basic Task Submission](https://nbviewer.org/github/huskysar/umbra/blob/main/notebooks/basic-task.ipynb)
1. [Constrained Task Submission](https://nbviewer.org/github/huskysar/umbra/blob/main/notebooks/constrained-task.ipynb)
1. [Space-track Orbits](https://nbviewer.org/github/huskysar/umbra/blob/main/notebooks/spacetrack.ipynb)

## environment management

We recommend using [pixi.sh](https://pixi.sh/latest/) to manage the Python environment required to execute code and notebooks in this repository

```
cd umbra
pixi install
```

## downloading tasked data via API

See [./download/README.md](./download/README.md)


## authentication

Set the following environment variables
```
# NOTE: currently sandbox token doesn't work for search, use standard token
export UMBRA_API_TOKEN="aaaaa"

export SPACETRACK_USER="bbbbb"
export SPACETRACK_PASS="ccccc"
```
