from setupext import find_packages, pkg_config, setup


@setup.add_extensions
def make_extensions():
    import p11x
    yield pkg_config(
        p11x.Extension(
            "freetypybind._ft2",
            ["src/_ft2.cpp", "src/_layout.cpp", "src/_util.cpp",
             "src/_sfnt_tables.cpp"],
            cxx_std=17,
        ),
        ["freetype2"],
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
