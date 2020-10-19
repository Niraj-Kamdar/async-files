import gzip
import inspect
import tempfile

import pytest

from async_files import gzip as agzip
from async_files.tempfile import mkstemp
from async_files.tempfile import NamedTemporaryFile
from async_files.tempfile import SpooledTemporaryFile
from async_files.tempfile import TemporaryFile


class TestBasic:
    @pytest.mark.parametrize(
        "actual_class, expected_class",
        (
            (TemporaryFile, tempfile.TemporaryFile),
            (NamedTemporaryFile, tempfile.NamedTemporaryFile),
            (SpooledTemporaryFile, tempfile.SpooledTemporaryFile),
            (mkstemp, tempfile.mkstemp),
            (agzip.GzipFile, gzip.GzipFile),
            (agzip.open, gzip.open),
        ),
    )
    def test_signature(self, actual_class, expected_class):
        assert inspect.signature(actual_class) == inspect.signature(expected_class)
