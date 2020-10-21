# async-files
![Test Runner](https://github.com/Niraj-Kamdar/async-files/workflows/Test%20Runner/badge.svg)
[![codecov](https://codecov.io/gh/Niraj-Kamdar/async-files/branch/main/graph/badge.svg?token=cyY0uU5JB5)](https://codecov.io/gh/Niraj-Kamdar/async-files/branch/main)
[![CodeFactor](https://www.codefactor.io/repository/github/niraj-kamdar/async-files/badge)](https://www.codefactor.io/repository/github/niraj-kamdar/async-files)

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

You can do same for any other IO classes like `gzip.GzipFile`, `zipfile.ZipFile`, etc. 
I have added async version of tempfile and gzip modules in the `v0.2` 
since they are commonly used modules and I will add more modules in the future releases. 
You can use these modules just like you use standard library module, only difference is you need to await coroutine methods.
You can request for support for new modules by [creating new issue](https://github.com/Niraj-Kamdar/async-files/issues/new).

You can also create coroutine from any blocking function by using async-files's utility function `async_wraps`. For example:
```python
import shutil
from async_files.utils import async_wraps
async_rmtree = async_wraps(shutil.rmtree)
```
You can also use `async_wraps` as a decorator for your custom function. 
> Note: Only use `async_wraps` if target function is IO-bound.

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

## Feedback & Contributions
Bugs and feature requests can be made via [GitHub issues](https://github.com/Niraj-Kamdar/async-files/issues/new). 
Be aware that these issues are not private, so take care when providing output to make sure you are not disclosing security issues in other products.

Pull requests are also welcome via git.

The async-files uses `sourcery`, `restyled` and `code factor` bots to ensure code quality of the PR.
