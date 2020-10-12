import gzip
from typing import Awaitable, Callable

from .fileio import FileIO
from .fileobj import FileObj, DEFAULT_CONFIG
from .utils import async_wraps

GZIP_CONFIG = DEFAULT_CONFIG
GZIP_CONFIG["bytes_sync_attrs"].append("mtime")


class GzipFileObj(FileObj):
    CONFIG = GZIP_CONFIG
    mtime: int


class open(FileIO):
    OPEN = gzip.open
    FILEOBJ = GzipFileObj


class GzipFile(FileIO):
    OPEN = gzip.GzipFile
    FILEOBJ = GzipFileObj


compress: Callable[[], Awaitable[bytes]] = async_wraps(gzip.compress)
decompress: Callable[[], Awaitable[bytes]] = async_wraps(gzip.decompress)
