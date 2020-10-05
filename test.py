import asyncio
import sys
from tempfile import TemporaryFile as _TemporaryFile

from async_files import FileIO


class TemporaryFile(FileIO):
    OPEN = _TemporaryFile


async def main():
    async with TemporaryFile("r+") as f:
        await f.write("whatever it takes!")
        await f.seek(0)
        s = await f.read()
        print(s)


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if sys.platform.startswith("win"):
        if isinstance(loop, asyncio.SelectorEventLoop):
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
    return loop


def run_coroutine(coro):
    loop = get_event_loop()
    aws = asyncio.ensure_future(coro)
    result = loop.run_until_complete(aws)
    return result


if __name__ == "__main__":
    run_coroutine(main())
