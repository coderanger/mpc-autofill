import os
import shutil
from pathlib import Path

import requests
from redis import Redis
from rq import Worker

redis_host = os.environ.get("REDIS_HOST" or "localhost")


def delete_stale_images(path: Path):
    file_tuples = os.walk(path)
    for dirpath, dirnames, filenames in file_tuples:
        ...


def download_image(image_url: str, image_path: Path) -> None:
    response = requests.get(image_url, timeout=5, stream=True)
    if response.status_code == 200:
        if not os.path.exists(image_path.parent):
            os.makedirs(image_path.parent)
        with open(image_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)


def download_image_and_listen_for_updates(image_id: str, image_url: str, image_type: str, image_path: Path) -> None:
    download_image(image_url=image_url, image_path=image_path)
    if image_type == "google_drive":
        ...  # TODO: listen for updates


if __name__ == "__main__":
    w = Worker(["default"], connection=Redis(host="redis"))
    w.work()
