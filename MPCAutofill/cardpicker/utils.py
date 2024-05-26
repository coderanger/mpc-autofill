import json
import time
from math import floor
from typing import Any

import ratelimit
import requests

TEXT_BOLD = "\033[1m"
TEXT_END = "\033[0m"


def time_to_hours_minutes_seconds(t: float) -> tuple[int, int, int]:
    hours = int(floor(t / 3600))
    mins = int(floor(t / 60) - hours * 60)
    secs = int(t - (mins * 60) - (hours * 3600))
    return hours, mins, secs


def log_hours_minutes_seconds_elapsed(t0: float) -> None:
    hours, mins, secs = time_to_hours_minutes_seconds(time.time() - t0)
    print("Elapsed time: ", end="")
    if hours > 0:
        print(f"{hours} hour{'s' if hours != 1 else ''}, ", end="")
    print(f"{mins} minute{'s' if mins != 1 else ''} and {secs} second{'s' if secs != 1 else ''}.")


@ratelimit.sleep_and_retry  # type: ignore  # `ratelimit` does not implement decorator typing correctly
@ratelimit.limits(calls=1, period=0.1)  # type: ignore  # `ratelimit` does not implement decorator typing correctly
def get_json_endpoint_rate_limited(url: str) -> dict[str, Any]:
    return json.loads(requests.get(url).content)


def merge_tags(a: list[dict], b: list[dict]) -> list[dict]:
    a_map = {v["name"]: v for v in a}
    b_map = {v["name"]: v for v in b}
    out_tags = []
    for name in a_map.keys() | b_map.keys():
        a_val = a_map.get(name)
        b_val = b_map.get(name)
        val = a_val or b_val
        if a_val is not None and b_val is not None:
            val["children"] = merge_tags(a_val["children"], b_val["children"])
        out_tags.append(val)
    return sorted(out_tags, key=lambda x: x["name"])
