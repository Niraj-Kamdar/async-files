import gzip
from typing import Awaitable, Callable

from . import FileIO, async_wraps


class open(FileIO):
    OPEN = gzip.open


class GzipFile(FileIO):
    OPEN = gzip.GzipFile


compress: Callable[[], Awaitable[bytes]] = async_wraps(gzip.compress)
decompress: Callable[[], Awaitable[bytes]] = async_wraps(gzip.decompress)
