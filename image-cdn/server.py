import datetime as dt
import os
from pathlib import Path

from flask import Flask, Response, redirect, send_file
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from worker import download_image_and_listen_for_updates

# region constants
GOOGLE_DRIVE = "google_drive"
SMALL = "small"
SMALL_IMAGE_HEIGHT = 400
LARGE = "large"
LARGE_IMAGE_HEIGHT = 800
IMAGE_EXPIRY = dt.timedelta(days=14)

# endregion

# region environment

redis_host = os.environ.get("REDIS_HOST" or "localhost")

# endregion

# region setup

redis_connection = Redis(host=redis_host)
queue = Queue(connection=redis_connection)
scheduler = Scheduler(connection=redis_connection)
app = Flask(__name__)

# endregion

# region api


def get_url_for_image(image_id: str, image_type: str, image_size: str) -> str:
    sizes_to_height = {SMALL: SMALL_IMAGE_HEIGHT, LARGE: LARGE_IMAGE_HEIGHT}
    height = sizes_to_height.get(image_size)
    if not height:
        raise KeyError(f"Unknown size {image_size}")
    if image_type == GOOGLE_DRIVE:
        return f"https://drive.google.com/thumbnail?sz=w{height}-h{height}&id={image_id}"
    raise KeyError(f"Unknown type {image_type}")


def get_image_path() -> Path:
    cwd = Path(os.getcwd())
    return cwd / "images"


def get_path_for_image(image_id: str, image_type: str, image_size: str) -> Path:
    return get_image_path() / image_type / image_size / f"{image_id}.jpg"


def handle_google_drive_image(image_id: str, image_size: str) -> Response:
    image_path = get_path_for_image(image_id=image_id, image_type=GOOGLE_DRIVE, image_size=image_size)

    # images expire after 2 weeks (in case any updates from google drive are missed)
    if image_path.exists():
        modified_time = dt.datetime.fromtimestamp(os.path.getmtime(image_path))
        if (dt.datetime.now() - modified_time) > IMAGE_EXPIRY:
            os.remove(image_path)

    if image_path.exists():  # just in case this isn't handled by nginx correctly for whatever reason
        return send_file(image_path)

    image_url = get_url_for_image(image_id=image_id, image_type=GOOGLE_DRIVE, image_size=image_size)
    queue.enqueue(download_image_and_listen_for_updates, image_id, image_url, GOOGLE_DRIVE, image_path)
    return redirect(image_url)


@app.route(f"/{GOOGLE_DRIVE}/{SMALL}/<image_id>.jpg", methods=["GET"])
def handle_small_google_drive_image(image_id) -> Response:
    return handle_google_drive_image(image_id=image_id, image_size=SMALL)


@app.route(f"/{GOOGLE_DRIVE}/{LARGE}/<image_id>.jpg", methods=["GET"])
def handle_large_google_drive_image(image_id) -> Response:
    return handle_google_drive_image(image_id=image_id, image_size=LARGE)


# endregion


if __name__ == "__main__":
    # scheduler.cron(
    #     cron_string="",
    #     func=delete_stale_images,
    #     kwargs=
    # )
    app.run()
