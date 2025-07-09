import re
import time
from pathlib import Path
from typing import Any

from loguru import logger

from config import config

USER_TO_SMS: dict[int, dict[str:Any]] = {}  # id: {count, time}
MINUTE = 60
TIMEOUT = 10 * MINUTE


def get_project_root() -> Path:
    path_ = Path(__file__).parent

    while path_.name != config["project"]["name"]:
        if path_.__fspath__() == path_.anchor:
            return path_ / config["project"]["name"]
        path_ = path_.parent

    return path_.parent / config["project"]["name"]

