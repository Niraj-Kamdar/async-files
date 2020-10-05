from typing import List, Dict

from async_files.utils import async_wraps, FileIOMeta, FileObj

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
    "strings_async_attrs": [],
    "strings_sync_attrs": [
        "buffer",
        "encoding",
        "errors",
        "line_buffering",
        "newlines",
    ],
    "bytes_async_attrs": ["readinto", "readinto1", "read1"],
    "bytes_sync_attrs": ["raw"],
}


class FileIO(metaclass=FileIOMeta):
    # Class Attributes for customizations
    OPEN = open
    CONFIG = DEFAULT_CONFIG

    _file: FileObj

    def __init__(self, *args, **kwargs):
        self.bound_args = self.__signature__.bind(*args, **kwargs)
        self.bound_args.apply_defaults()

    async def __call__(self):
        """Convenience method to allow call like following:
        f = await FileIO("some file path", "r")()
        Note: We can't make async __init__
        """
        return await self.open()

    async def open(self):
        file = await self.__class__.OPEN(**self.bound_args.arguments)
        self._file = FileObj(
            file, self.bound_args.arguments["mode"], self.__class__.CONFIG
        )
        return self._file

    async def __aenter__(self):
        return await self.open()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._file.close()
