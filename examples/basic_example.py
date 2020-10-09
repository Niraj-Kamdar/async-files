from .utils import run_coroutine
from async_files import FileIO


async def main():
    async with FileIO("README.md") as f:
        s = await f.read()
        print(s)
        await f.seek(0)
        print("#" * 50)
        async for line in f:
            print(line, end="")


if __name__ == "__main__":
    run_coroutine(main())
