from setupext import find_packages, setup


@setup.add_extension
def make_extension():
    from p11x import Extension, configure
    return configure(
        Extension(
            "freetypybind._ft2",
            ["src/_ft2.cpp", "src/_layout.cpp", "src/_util.cpp",
             "src/_sfnt_tables.cpp"],
            depends=["setup.py", "src/_ft2.h", "src/_layout.h", "src/_util.h",
                     "src/_sfnt_tables.h"],
            language="c++1z",
        ),
        pkg_config=["freetype2"],
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
    entry_points={
        "console_scripts": [],
        "gui_scripts": [],
    },
    python_requires="",
    setup_requires=[
        "p11x",
        "setuptools_scm",
    ],
    use_scm_version=lambda: {
        "version_scheme": "post-release", "local_scheme": "node-and-date"},
    install_requires=[
    ],
)
