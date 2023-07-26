from datetime import datetime, timezone
import json
import os
from functools import lru_cache
import logging
from logging import handlers
from os.path import basename, splitext, abspath, dirname, join, exists, sep, isabs

import sys
import threading
import time
from typing import Any, Dict, Optional
from typing import Self


def now() -> datetime:
    return datetime.now()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_s() -> int:
    return int(time.time())


def now_ms() -> int:
    return int(time.time() * 1000)


def timestamp_to_date_str(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S %Z")


# === file
def base_name(file_path):
    # basename with removed file extension
    return splitext(basename(file_path))[0]


def get_project_root():
    file_path = abspath(dirname(__file__))
    res = file_path
    # file_path_parts = file_path.split(os.path.sep)
    while len(list(filter(lambda p: p != "", res.split(sep)))) > 1:
        if (not exists(join(res, "requirements.txt"))) and (
            not exists(join(res, "pyproject.toml"))
        ):
            res = dirname(res)
            continue
        else:
            return res
    raise Exception(f"get_root_root(): unable to find the project root for {file_path}")


# load json file with line comment '//' support
def load_json_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        new_lines = list(filter(lambda l: not l.strip().startswith("//"), lines))
        contents = "\n".join(new_lines)
        return json.loads(contents)


def merge_dict(dest: Dict, *args):
    for obj in args:
        for key, value in obj.items():
            if type(value) == dict:
                dest[key] = merge_dict(dest.get(key, {}), value)
            else:
                dest[key] = value
    return dest


#  == logger
@lru_cache(maxsize=64)
def init_logger(
    name: str,
    level: str = "info",
    dir: str = "logs",
):
    dir = str(join(get_project_root(), dir))

    logger = logging.getLogger()
    logger.name = name
    logger.setLevel(getattr(logging, level.upper()))

    logger.addHandler(logging.StreamHandler(stream=sys.stdout))

    path = join(dir, f"{name}.log")
    os.makedirs(dir, exist_ok=True)

    file_handler = handlers.TimedRotatingFileHandler(
        path if isabs(path) else abspath(path),
        when="D",
        interval=1,
        utc=True,
    )
    logger.addHandler(file_handler)

    for handler in logger.handlers:
        handler.setFormatter(
            logging.Formatter(
                fmt=r"%(asctime)s::%(name)s::%(funcName)s::%(levelname)s: %(message)s",
                datefmt=r"%Y-%m-%d %H:%M:%S %z",
            )
        )
    return logger


# ==  context
class Context:
    forward: Optional[Self]

    mapping: Dict[str, Any]

    rlock = threading.RLock()
    lock = threading.Lock()

    def __init__(self, ctx: Optional[Self] = None):
        self.forward = ctx
        self.mapping = {}

    def get(self, name, default=None):
        with Context.rlock:
            if name in self.mapping:
                return self.mapping[name]
            if self.forward is not None:
                return self.forward.get(name, default)
            return default

    def set(self, name, value):
        with self.rlock and self.lock:
            self.mapping[name] = value

    def remove(self, name):
        with self.rlock and self.lock:
            if name in self.mapping:
                del self.mapping[name]


class CancelContext(Context):
    _cancel: bool

    def __init__(self, ctx: Optional[Self] = None):
        super().__init__(ctx)
        self._cancel = False

    def cancel(self):
        with self.rlock and self.lock:
            self._cancel = True

    def uncancel(self):
        with self.rlock and self.lock:
            self._cancel = False

    def is_canceled(self):
        with self.rlock:
            is_canceled = self._cancel
            if is_canceled:
                return True

            # if one of `forward` context is `CancelContext` and is cancle, return True
            forward = self.forward
            while forward is not None:
                if isinstance(forward, CancelContext) and forward.is_canceled():
                    return True
                forward = forward.forward
        return False

    def sleep(self, seconds: float, interval: float = 0.1):
        start = time.time()
        while not self.is_canceled():
            if time.time() - start > seconds:
                return

            time.sleep(interval)


def sleep_with_context(ctx: CancelContext, seconds: float, interval: float = 0.1):
    start = time.time()
    while not ctx.is_canceled():
        if time.time() - start > seconds:
            return

        time.sleep(interval)
