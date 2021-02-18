import os
import tarfile
import tempfile

from async_files import FileIO
from async_files.fileobj import DEFAULT_CONFIG, FileObj
from .utils import run_coroutine, ChangeDirContext

TARBALL_CONFIG = DEFAULT_CONFIG
TARBALL_CONFIG["strings_async_attrs"].extend(["add", "extract", "extractall"])


class TarballFileObj(FileObj):
    CONFIG = TARBALL_CONFIG
    add: callable
    extract: callable
    extractall: callable


class async_open(FileIO):
    OPEN = tarfile.TarFile.open
    FILEOBJ = TarballFileObj


async def make_tarfile_from_dir(output_filename, source_dir):
    if not output_filename.endswith('.gz'):
        output_filename += '.tar.gz'
    async with async_open(output_filename, "w:gz") as tar:
        await tar.add(source_dir, arcname=".")

    return output_filename


async def main():
    # create a test directory
    tempdir = tempfile.mkdtemp()
    testdir = os.path.join(tempdir, "test")
    os.makedirs(testdir) if not os.path.isdir(testdir) else None
    with open(os.path.join(testdir, "test.txt"), "w") as f:
        f.write("Hello World!")

    with ChangeDirContext(tempdir):
        testtar = await make_tarfile_from_dir("test", testdir)
        print(testtar)


if __name__ == "__main__":
    run_coroutine(main())
