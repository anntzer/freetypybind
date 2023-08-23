import os
from pathlib import Path
import shlex
import subprocess

from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup


ext = Pybind11Extension(
    "freetypybind._ft2",
    [
        "ext/_ft2.cpp",
        "ext/_layout.cpp",
        "ext/_util.cpp",
        "ext/_sfnt_tables.cpp",
    ],
    cxx_std=17,
)
pkgs = ["freetype2"]

# pkg-config
cmd = {"posix": ["pkg-config"], "nt": ["pkg-config", "--msvc-syntax"]}[os.name]
for pkg in pkgs:
    for attr, flag in [("extra_compile_args", "--cflags"),
                       ("extra_link_args", "--libs")]:
        getattr(ext, attr).extend(shlex.split(subprocess.check_output(
            [*cmd, flag, pkg], universal_newlines=True)))

# conda
conda_prefix = os.environ.get("CONDA_PREFIX")
if conda_prefix:
    ext.include_dirs.append(
        {"posix": str(Path(conda_prefix, "include")),
         "nt": str(Path(conda_prefix, "Library/include"))}[os.name])
    ext.library_dirs.append(
        {"posix": str(Path(conda_prefix, "lib")),
         "nt": str(Path(conda_prefix, "Library/lib"))}[os.name])


setup(ext_modules=[ext])
