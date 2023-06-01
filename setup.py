#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Setup this SWIG library."""
import argparse
import runpy

from setuptools import Distribution, Extension, find_packages, setup
from setuptools.command.build_py import build_py

EXAMPLE_EXT = Extension(
    name="_example",
    sources=[
        "src/example/example.c",
        "src/example/example.i",
    ],
)

STD_EXT = Extension(
    name="_stl_example",
    swig_opts=["-c++"],
    sources=[
        "src/example/stl_example.cpp",
        "src/example/stl_example.i",
    ],
    include_dirs=[
        "src/example",
    ],
    extra_compile_args=[  # The g++ (4.8) in Travis needs this
        "-std=c++11",
    ],
)


# Build extensions before python modules,
# or the generated SWIG python files will be missing.
class BuildPy(build_py):
    def run(self):
        self.run_command("build_ext")
        super(build_py, self).run()


INFO = runpy.run_path("src/example/_meta.py")

setup_info=dict(
    name="swig-example-demo",
    description="A Python demo for SWIG",
    version=INFO["__version__"],
    keywords=["SWIG", "demo"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["*.pyd"]},
    ext_modules=[EXAMPLE_EXT, STD_EXT],
    cmdclass={
        "build_py": BuildPy,
    },
    python_requires=">=3.4",
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-flake8",
    ],
)

def get_package_wheel_name() -> str:
    """Get the right wheel name for Basilisk
    Example: Basilisk_Sim-2.2.0b0-cp310-cp310-linux_x86_64.whl

    From https://stackoverflow.com/a/60773383

    Returns:
        The wheel name

    """
    # create a fake distribution from arguments
    dist = Distribution(attrs=setup_info)

    # finalize bdist_wheel command
    bdist_wheel_cmd = dist.get_command_obj("bdist_wheel")
    bdist_wheel_cmd.ensure_finalized()

    # assemble wheel file name
    distname = bdist_wheel_cmd.wheel_dist_name
    tag = "-".join(bdist_wheel_cmd.get_tag())

    return f"{distname}-{tag}.whl"


def main():
    parser = argparse.ArgumentParser("Builder helper")
    parser.add_argument(
        "-n", "--name", help="Get the right wheel filename", action="store_true"
    )
    args = parser.parse_args()

    if args.name:
        print(get_package_wheel_name())
    else:
        setup(**setup_info)


if __name__=='__main__':
    main()
    