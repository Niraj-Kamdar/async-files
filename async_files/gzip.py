import gzip
from typing import Awaitable
from typing import Callable

from . import async_wraps
from . import FileIO


class open(FileIO):
    OPEN = gzip.open


class GzipFile(FileIO):
    OPEN = gzip.GzipFile


compress: Callable[[], Awaitable[bytes]] = async_wraps(gzip.compress)
decompress: Callable[[], Awaitable[bytes]] = async_wraps(gzip.decompress)
