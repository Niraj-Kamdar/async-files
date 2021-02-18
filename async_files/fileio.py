from inspect import signature

from async_files.fileobj import FileObj
from async_files.utils import async_wraps


class FileIOMeta(type):
    def __new__(mcs, name, bases, clsdict):
        cls = super().__new__(mcs, name, bases, clsdict)
        sig = signature(cls.OPEN)
        cls.OPEN = async_wraps(cls.OPEN)
        cls.__signature__ = sig
        return cls


class FileIO(metaclass=FileIOMeta):
    OPEN = open
    FILEOBJ = FileObj
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
        file = await self.__class__.OPEN(*self.bound_args.args,
                                         **self.bound_args.kwargs)
        self._file = self.__class__.FILEOBJ(file,
                                            self.bound_args.arguments["mode"])
        return self._file

    async def __aenter__(self):
        return await self.open()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._file.close()
