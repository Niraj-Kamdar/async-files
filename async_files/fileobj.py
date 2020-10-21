from typing import Any
from typing import Awaitable
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import IO
from typing import List
from typing import Union

from async_files.utils import async_wraps

DEFAULT_CONFIG: Dict[str, List[str]] = {
    "common_async_attrs": [
        "close",
        "flush",
        "isatty",
        "read",
        "readline",
        "readlines",
        "seek",
        "tell",
        "truncate",
        "write",
        "writelines",
    ],
    "common_sync_attrs": [
        "closed",
        "detach",
        "fileno",
        "readable",
        "writable",
        "seekable",
        "mode",
        "name",
    ],
    "strings_async_attrs": ["reconfigure"],
    "strings_sync_attrs": [
        "buffer",
        "encoding",
        "errors",
        "line_buffering",
        "newlines",
        "write_through",
    ],
    "bytes_async_attrs": ["peek", "readinto", "readinto1", "read1"],
    "bytes_sync_attrs": ["raw"],
}


class FileObj:
    CONFIG: ClassVar[Dict[str, List[str]]] = DEFAULT_CONFIG

    # Async attributes
    close: Callable[[], Awaitable[None]]
    flush: Callable[[], Awaitable[None]]
    isatty: Callable[[], Awaitable[bool]]
    peek: Callable[[int], Awaitable[bytes]]
    read: Callable[[], Awaitable[Union[str, bytes]]]
    read1: Callable[[], Awaitable[bytes]]
    readinto: Callable[[bytearray], Awaitable[int]]
    readinto1: Callable[[bytearray], Awaitable[int]]
    readline: Callable[[], Awaitable[Union[str, bytes]]]
    readlines: Callable[[], Awaitable[List[Union[str, bytes]]]]
    reconfigure: Callable[[], Awaitable[None]]
    seek: Callable[[int], Awaitable[int]]
    tell: Callable[[], Awaitable[int]]
    truncate: Callable[[], Awaitable[int]]
    write: Callable[[Union[str, bytes]], Awaitable[int]]
    writelines: Callable[[List[Union[str, bytes]]], Awaitable[None]]

    # Sync Attributes
    buffer: Callable[[], object]
    closed: bool
    detach: Callable[[], object]
    encoding: str
    errors: str
    fileno: Callable[[], int]
    line_buffering: bool
    mode: str
    name: str
    newlines: Any
    raw: object
    readable: Callable[[], bool]
    seekable: Callable[[], bool]
    writable: Callable[[], bool]
    write_through: bool

    def __init__(self, fobj: IO, mode: str):
        if "b" in mode:
            async_attrs = (self.__class__.CONFIG["common_async_attrs"] +
                           self.__class__.CONFIG["bytes_async_attrs"])
            sync_attrs = (self.__class__.CONFIG["common_sync_attrs"] +
                          self.__class__.CONFIG["bytes_sync_attrs"])
        else:
            async_attrs = (self.__class__.CONFIG["common_async_attrs"] +
                           self.__class__.CONFIG["strings_async_attrs"])
            sync_attrs = (self.__class__.CONFIG["common_sync_attrs"] +
                          self.__class__.CONFIG["strings_sync_attrs"])

        for attr in async_attrs:
            if hasattr(fobj, attr):
                setattr(self, attr, async_wraps(getattr(fobj, attr)))

        for attr in sync_attrs:
            if hasattr(fobj, attr):
                setattr(self, attr, getattr(fobj, attr))

    async def __anext__(self):
        line = await self.readline()
        if line:
            return line
        raise StopAsyncIteration

    def __aiter__(self):
        return self
