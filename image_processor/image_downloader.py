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


def my_image_getter(search_term, key):
    subscription_key = key
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
def download_images(dest, urls):
    path = Path(dest)
    path.mkdir(exist_ok=True)
    counter = 0
    for url in urls:
        filepath = path / f"_{counter}"
        counter += 1
        data = requests.get(url).content
        with filepath.open('wb') as f:
            f.write(data)


@timecall
def threaded_download(dest, urls):

    path = Path(dest)
    path.mkdir(exist_ok=True)

    def _down_load(path, url):
        filepath = path / f"_{datetime.datetime.now().timestamp():.2f}.jpeg"
        data = requests.get(url).content
        with filepath.open('wb') as f:
            f.write(data)

    func = partial(_down_load, path)
    with ThreadPoolExecutor(max_workers=4) as e:
        e.map(func, urls)

async def async_download(dest, urls):

    async def _down_load(path, url):
        filepath = path / f"_{datetime.datetime.now().timestamp():.2f}.jpeg"
        data = await requests.get(url).content
        with filepath.open('wb') as f:
            f.write(data)
    tasks = []
    for url in urls:
        task = _down_load(dest, url)
        tasks.append(task)

    await asyncio.gather(*tasks)



def main():
    x = my_image_getter("teddy bear")
    print(f"number of images: {len(x)}, distinct: {len(set(x))}")
    #download_images('/tmp/testimages', x)
    #threaded_download('/tmp/testthread', x)
    async_download('/tmp/testasync', x)

    """
        with open("/tmp/test", "wb") as f:
            for url in x[:5]:
                r = requests.get(url)
                print(f"url: {url}, r: {r}")
                f.write(r.content)
                break
    """

    return "Done"


if __name__ == "__main__":
    main()
