# async-files
async-files is a fast, lightweight, and extensible asyncio file library, written in pure python and inspired by [aiofiles](https://github.com/Tinche/aiofiles). This works just like aiofiles which delegates file IO operations to a separate thread pool. Although, async-files have been completely re-written from scratch to use modern `async...await...` syntax and with extensibility and flexibility in mind.

## Usage

Files can be opened with async context manager or by calling FileIO instance.
```python
async with FileIO("README.md") as f:
    s = await f.read()
    print(s)
```
or
```python
f = await FileIO("README.md")()  # __init__ can't be asynchronous.
s = await f.read()
print(s)
await f.close()
```

Asynchronous iteration is also supported.

```python
async with FileIO("README.md") as f:
    async for line in f:
        print(line, end="")
```

You can also extend functionality of FileIO to support other classes like `tempfile.TemporaryFile` very easily:
```python
from tempfile import TemporaryFile as _TemporaryFile
from async_files import FileIO

class TemporaryFile(FileIO):
    OPEN = _TemporaryFile
```

You can do same for any IO classes like `GzipFile`, `SpooledTemporaryFile`, etc.

Following are asynchronous attributes of the FileIO object.
```python
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
```
Other attributes are synchronous just like standard library fileobj.
