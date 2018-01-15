import shlex
import subprocess

from setupext import Extension, find_packages, get_pybind_include, setup


def get_pkg_config(info, lib):
    return shlex.split(subprocess.check_output(["pkg-config", info, lib],
                                               universal_newlines=True))


EXTENSION = Extension(
    "freetypybind._ft2",
    ["src/_ft2.cpp", "src/_layout.cpp", "src/_util.cpp",
     "src/_sfnt_tables.cpp"],
    depends=
        ["setup.py", "src/_ft2.h", "src/_layout.h", "src/_util.h",
         "src/_sfnt_tables.h"],
    language=
        "c++",
    include_dirs=
        [get_pybind_include(), get_pybind_include(user=True)],
    extra_compile_args=
        ["-std=c++1z", "-Wextra", "-Wpedantic"]
        + get_pkg_config("--cflags", "freetype2"),
    extra_link_args=
        get_pkg_config("--libs", "freetype2"),
)


setup(
    name="freetypybind",
    description="",
    long_description=open("README.rst", encoding="utf-8").read(),
    author="Antony Lee",
    author_email="",
    url="",
    license="MIT",
    classifiers=[],
    packages=find_packages("lib"),
    package_dir={"": "lib"},
    ext_modules=[EXTENSION],
    entry_points={
        "console_scripts": [],
        "gui_scripts": [],
    },
    python_requires="",
    setup_requires=["setuptools_scm"],
    use_scm_version=lambda: {
        "version_scheme": "post-release", "local_scheme": "node-and-date"},
    install_requires=[
    ],
)
