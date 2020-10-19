import asyncio
import shutil
import sys
import tempfile


class TempDirTest:
    """ For tests that need a temp directory """

    @classmethod
    def setup_class(cls):
        cls.tempdir = tempfile.mkdtemp()

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.tempdir)


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if sys.platform.startswith("win") and isinstance(
            loop, asyncio.SelectorEventLoop):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    return loop
