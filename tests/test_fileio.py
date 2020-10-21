import asyncio
import inspect
import os
import sys

import pytest

from async_files import FileIO
from async_files.fileobj import FileObj
from tests.utils import get_event_loop
from tests.utils import TempDirTest


@pytest.fixture
def event_loop():
    yield get_event_loop()


class TestFileIO(TempDirTest):
    def setup_method(self):
        self.test_read_file = os.path.join(self.tempdir, "test_read_file")
        with open(self.test_read_file, "w") as f:
            f.writelines(["Hello\n", "world!"])

    def test_signature(self):
        assert inspect.signature(FileIO) == inspect.signature(open)

    @pytest.mark.asyncio
    async def test_async_attrs(self):
        async with FileIO(self.test_read_file) as f:
            # Assert that new fileobject is instance of the FileObj
            assert isinstance(f, FileObj)

            async_attrs = [
                "close",
                "flush",
                "isatty",
                "read",
                "readline",
                "readlines",
                # "reconfigure",
                "seek",
                "tell",
                "truncate",
                "write",
                "writelines",
            ]
            for attr in async_attrs:
                coro = getattr(f, attr)
                if not coro:
                    pytest.fail(
                        msg=f"{attr} haven't been attached to FileObj!")
                # Make sure all IO methods are converted into coroutines.
                # Only coroutine or an awaitable can be converted to future.
                try:
                    future = asyncio.ensure_future(coro())
                    future.cancel()
                except TypeError:
                    pytest.fail(
                        msg=
                        f"{attr} exists but haven't been converted to coroutine!"
                    )

    @pytest.mark.asyncio
    async def test_basics(self):
        async with FileIO(self.test_read_file) as f:
            assert all([f.readable, f.seekable, f.writable])


class TestCRUD(TempDirTest):
    def setup_method(self):
        self.test_read_file = os.path.join(self.tempdir, "test_read_file")
        with open(self.test_read_file, "w") as f:
            f.writelines(["Hello\n", "world!"])

    @pytest.mark.asyncio
    async def test_seek(self):
        async with FileIO(self.test_read_file) as f:
            assert (await f.tell()) == 0
            s = await f.seek(4)
            assert s == 4 == (await f.tell())

    @pytest.mark.asyncio
    async def test_read(self):
        async with FileIO(self.test_read_file) as f:
            # Test Read whole file
            s = await f.read()
            assert s == "Hello\nworld!"

            # Test Read n characters
            await f.seek(0)
            s = await f.read(4)
            assert s == "Hell"

            expected_lines = ["Hello\n", "world!"]
            # Iterate lines
            await f.seek(0)
            lines = [line async for line in f]
            assert lines == expected_lines

            # make sure readlines are same as expected_lines
            await f.seek(0)
            assert expected_lines == await f.readlines()

    @pytest.mark.asyncio
    async def test_write(self):
        test_write_file = os.path.join(self.tempdir, "test_write_file")
        async with FileIO(test_write_file, "w") as f:
            await f.write("Hello\n")
            await f.writelines(["World\n", "This is amazing!"])
        with open(test_write_file, "r") as f:
            assert f.read() == "Hello\nWorld\nThis is amazing!"

    @pytest.mark.asyncio
    async def test_bytes_write(self):
        test_write_file = os.path.join(self.tempdir, "test_write_file")
        f = await FileIO(test_write_file, "wb")()
        await f.write(b"Hello\n")
        await f.writelines([b"World\n", b"This is amazing!"])
        await f.close()
        with open(test_write_file, "rb") as f:
            assert f.read() == b"Hello\nWorld\nThis is amazing!"

    @pytest.mark.asyncio
    async def test_bytes_read(self):
        async with FileIO(self.test_read_file, "rb") as f:
            # Test Read whole file
            lines = await f.read()
            if sys.platform.startswith("win"):
                assert lines == b"Hello\r\nworld!"
            else:
                assert lines == b"Hello\nworld!"
