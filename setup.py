import os

from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="async-files",
    version="0.1",
    description="Async Files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Niraj Kamdar",
    packages=find_packages(),
    license="MIT",
    url="https://github.com/Niraj-Kamdar/async-files",
    download_url="https://github.com/Niraj-Kamdar/async-files/archive/master.zip",
    keywords=["asyncio", "file", "aiofile"],
    classifiers=[
        "Development Status :: 4 - Beta",
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
