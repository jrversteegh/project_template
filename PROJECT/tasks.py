import glob
import os
from datetime import datetime
from pathlib import Path

import tomli
from invoke import task

# Run from project root directory
script_dir = Path(__file__).absolute().parent
os.chdir(script_dir)


@task
def format(ctx):
    """Run black and isort"""
    for cmd in (
        "black .",
        "isort .",
        f"clang-format -i {' '.join(glob.glob('include/PROJECT/*.h'))}",
        f"clang-format -i {' '.join(glob.glob('src/PROJECT/*.cpp'))}",
        f"clang-format -i {' '.join(glob.glob('src/pycxxPROJECT/*.cpp'))}",
        f"clang-format -i {' '.join(glob.glob('tests/PROJECT/*.cpp'))}",
        f"clang-format -i {' '.join(glob.glob('tests/benchmarks/*.cpp'))}",
        "pandoc -s -o README.md README.rst",
    ):
        ctx.run(cmd, echo=True)


@task
def check(ctx):
    """Run flake8"""
    for cmd in ("flake8 .",):
        ctx.run(cmd, echo=True)


@task
def test(ctx):
    """Run tests"""
    for cmd in (
        "ctest --output-junit ctest_tests.xml --test-dir build",
        "pytest --cov --junitxml=build/reports/tests.xml",
    ):
        ctx.run(cmd, echo=True)


@task
def benchmark(ctx):
    """Run tests"""
    for cmd in ("build/benchmarks/test_PROJECT",):
        num_threads = 1
        ctx.run(
            cmd,
            echo=True,
            env={
            },
        )


@task
def create_build_dir(ctx):
    """Build"""
    for cmd in ("mkdir -p build",):
        ctx.run(cmd, echo=True)


@task(update_revision, create_build_dir)
def build(ctx):
    """Build"""
    for cmd in (
        "poetry build -vv",
        f"conan create . --build=missing --profile={script_dir}/conan/PROJECT.profile",
    ):
        ctx.run(cmd, echo=True)


@task
def clean(ctx):
    """Clean"""
    for cmd in ("rm -rf build",):
        ctx.run(cmd, echo=True)


@task(clean, build)
def rebuild(ctx): ...
