from tempfile import TemporaryFile as _TemporaryFile

from async_files import FileIO
from .utils import run_coroutine


class TemporaryFile(FileIO):
    OPEN = _TemporaryFile


async def main():
    async with TemporaryFile("r+") as f:
        await f.write("whatever it takes!")
        await f.seek(0)
        s = await f.read()
        print(s)


if __name__ == "__main__":
    run_coroutine(main())
