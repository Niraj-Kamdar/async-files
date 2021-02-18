import asyncio
import os
import sys


class ChangeDirContext:
    def __init__(self, destination_dir):
        self.current_dir = os.getcwd()
        self.destination_dir = destination_dir

    def __enter__(self):
        os.chdir(self.destination_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.current_dir)


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


def run_coroutine(coro):
    loop = get_event_loop()
    aws = asyncio.ensure_future(coro)
    return loop.run_until_complete(aws)
