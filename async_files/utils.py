import asyncio
from functools import wraps, partial
from inspect import signature
from typing import Callable, Union, List, Any, IO, Awaitable, Dict


def async_wraps(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


class FileIOMeta(type):
    def __new__(mcs, name, bases, clsdict):
        cls = super().__new__(mcs, name, bases, clsdict)
        sig = signature(cls.OPEN)
        cls.OPEN = async_wraps(cls.OPEN)
        cls.__signature__ = sig
        return cls


class FileObj:
    # Async attributes
    close: Callable[[], Awaitable[None]]
    flush: Callable[[], Awaitable[None]]
    isatty: Callable[[], Awaitable[bool]]
    read: Callable[[], Awaitable[Union[str, bytes]]]
    read1: Callable[[], Awaitable[bytes]]
    readinto: Callable[[bytearray], Awaitable[int]]
    readinto1: Callable[[bytearray], Awaitable[int]]
    readline: Callable[[], Awaitable[Union[str, bytes]]]
    readlines: Callable[[], Awaitable[List[Union[str, bytes]]]]
    seek: Callable[[], Awaitable[int]]
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

    def __init__(self, fobj: IO, mode: str, config: Dict[str, List[str]]):
        if "b" in mode:
            async_attrs = config["common_async_attrs"] + config["bytes_async_attrs"]
            sync_attrs = config["common_sync_attrs"] + config["bytes_sync_attrs"]
        else:
            async_attrs = config["common_async_attrs"] + config["strings_async_attrs"]
            sync_attrs = config["common_sync_attrs"] + config["strings_sync_attrs"]

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
        else:
            raise StopAsyncIteration

    def __aiter__(self):
        return self
