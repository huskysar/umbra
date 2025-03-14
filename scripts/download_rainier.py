#!/usr/bin/env python
'''
Download all our Mt Rainier Data

TODO:
- figure out progress bar (https://github.com/stac-utils/stac-asset/blob/bedce72570acc6e70a4782aeb92a04a0cdb12d74/src/stac_asset/_cli.py#L381)

Usage:
./scripts/download_rainier.py
'''
import stac_asset
import pystac_client
import pystac
import os
import argparse
import asyncio

UMBRA_STAC_API = pystac_client.Client.open("https://api.canopy.umbra.space/v2/stac/",
                                    headers={"authorization": f"Bearer {os.environ.get('UMBRA_API_TOKEN')}" }
)

def search_stac_items() -> pystac.ItemCollection:
    aoi_as_dict = {
            "coordinates": [
                -121.74456,
                46.79679,
            ],
            "type": "Point"
        }

    limit_results=2000

    stac_search = UMBRA_STAC_API.search(
        max_items=limit_results,
        limit=limit_results,
        intersects=aoi_as_dict,
    )
    items = stac_search.item_collection()
    print(f'Found {len(items)} STAC Items')
    return items


def get_signed_items(five_ids: list) -> list[pystac.Item]:
    '''
    Umbra does automatic URL signing for up to 5 Stac Items. Signed URL good fo 1 hr
    '''
    stac_search = UMBRA_STAC_API.search(
        ids=five_ids,
    )
    items = stac_search.item_collection()
    print(f'Signed {len(items)} STAC Items')
    return list(items)


def get_asset_key_map(item):
    title2assetkey = {
        'Metadata': '',
        'CPHD': '',
        'SICD': '',
        'SIDD': '',
        'GEC': '',
    }
    for title in title2assetkey.keys():
        asset_key, _ = [(a,v) for a,v in item.assets.items() if v.title == title][0]
        title2assetkey[title] = asset_key

    return title2assetkey


async def download_item(stac_item, include: list,  outdir: str) -> str:
    #How to set this CLI option? --max-concurrent-downloads
    Config = stac_asset.Config(alternate_assets=['s3_signed'],
                      http_client_timeout=3600, #up to 1hr from 5m for large SICDs on slow home wifi :( ...
                      #http_max_attempts=10, #default=10
                      #exclude = ['cphd'],
                      include = include,
                      #overwrite = False,
                      #file_name_strategy = , # can get creative w/ STAC item properties
    )
    local_item = await stac_asset.download_item(item=stac_item,
                                                directory=outdir,
                                                config=Config)
    return local_item


def main(asset: str, outdir: str):
    items = search_stac_items()
    for i in range(0, len(items), 5):
        five_ids = [item.id for item in items[i:i+5]]
        signed_items = get_signed_items(five_ids)
        # Download one at a time for starters
        for signed in signed_items:
            asset_key_map = get_asset_key_map(signed)
            # Automatically create subfolder to stay organized
            subfolder = asset_key_map['GEC'].rstrip('.tif')
            outdir_auto = os.path.join(outdir, subfolder)
            print(f'Saving {asset} to {outdir_auto}...')
            _ = asyncio.run(download_item(signed, [asset_key_map[asset]], outdir_auto))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Mt Rainier Data')
    parser.add_argument('-o', '--outdir', type=str, default='./', help='Output directory for downloaded assets')
    parser.add_argument('-a', '--asset', type=str, default='stac', choices=['Metadata','GEC','SICD'], help='Type of asset to download')
    args = parser.parse_args()

    main(args.asset, args.outdir)
