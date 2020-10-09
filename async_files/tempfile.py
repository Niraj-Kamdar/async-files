import tempfile
from typing import Awaitable
from typing import Callable

from .fileio import FileIO
from .utils import async_wraps


class TemporaryFile(FileIO):
    OPEN = tempfile.TemporaryFile


class NamedTemporaryFile(FileIO):
    OPEN = tempfile.NamedTemporaryFile


class SpooledTemporaryFile(FileIO):
    OPEN = tempfile.SpooledTemporaryFile


class mkstemp(FileIO):
    OPEN = tempfile.mkstemp


mkdtemp: Callable[[], Awaitable[str]] = async_wraps(tempfile.mkdtemp)
gettempdir: Callable[[], Awaitable[str]] = async_wraps(tempfile.gettempdir)
gettempdirb: Callable[[], Awaitable[bytes]] = async_wraps(tempfile.gettempdirb)
gettempprefix: Callable[[], str] = tempfile.gettempprefix
gettempprefixb: Callable[[], bytes] = tempfile.gettempprefixb
tempdir: str = tempfile.tempdir
