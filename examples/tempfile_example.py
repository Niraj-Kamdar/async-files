from .utils import run_coroutine
from async_files.tempfile import TemporaryFile


async def main():
    async with TemporaryFile("r+") as f:
        await f.write("whatever it takes!")
        await f.seek(0)
        s = await f.read()
        print(s)


if __name__ == "__main__":
    run_coroutine(main())
