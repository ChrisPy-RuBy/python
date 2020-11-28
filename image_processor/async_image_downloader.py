#!/usr/bin/env python3

"""Download, process, and upload images
"""
import asyncio
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from io import BytesIO
from pathlib import Path
from profilehooks import timecall, profile
import datetime
import matplotlib.pyplot as plt
import requests


def my_image_getter(search_term):
    subscription_key = "5c1dac441ae542cbbb435e3a7a44c083"
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    print(f"searching  for {search_term}")
    params = {"q": search_term, "license": "public",
              "imageType": "photo",
              "count": "150",
              "offset": "35"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    thumbnail_urls = [img["thumbnailUrl"]
                      for img in search_results["value"][:150]]
    return thumbnail_urls


def plot():
    f, axes = plt.subplots(10, 10)
    for i in range(10):
        for j in range(10):
            image_data = requests.get(x[i+4*j])
            image_data.raise_for_status()
            image = Image.open(BytesIO(image_data.content))
            axes[i][j].imshow(image)
            axes[i][j].axis("off")
    plt.show()


@timecall
async def async_download(dest, urls):

    path = Path(dest)
    print(f'path: {path}')
    path.mkdir(exist_ok=True)

    def _down_load(path, url):
        print("{:<30} {:>20}".format(url, datetime.datetime.now().isoformat()))
        filepath = path / f"_{datetime.datetime.now().timestamp():.2f}.jpeg"
        data = requests.get(url).content
        with filepath.open('wb') as f:
            f.write(data)

    func = partial(_down_load, path)
    with ThreadPoolExecutor(max_workers=10) as e:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                e,
                func,
                url
            ) for url in urls
        ]
        for response in await asyncio.gather(*tasks):
            pass


def main():
    x = my_image_getter("teddy bear")
    print(f"number of images: {len(x)}, distinct: {len(set(x))}")
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(async_download('/tmp/testasync/', x))
    loop.run_until_complete(future)


if __name__ == "__main__":
    main()
