import glob
import os
from datetime import datetime
from pathlib import Path

import tomli
from invoke import task

# Run from project root directory
script_dir = Path(__file__).absolute().parent
os.chdir(script_dir)
conan_dir = script_dir / "conan"

import build

version, date = build.get_project_version_and_date()


@task
def format(ctx):
    """Run black and isort"""
    cpp_files = " ".join(
        [
            " ".join(glob.glob(d))
            for d in [
                "include/PROJECT/*.h",
                "src/cxx/*.cpp",
                "src/cxx/app/*.cpp",
                "src/cxxPROJECT/*.cpp",
                "tests/cxx/*.cpp",
                "tests/benchmarks/*.cpp",
            ]
        ]
    )

    for cmd in (
        "black .",
        "isort .",
        f"clang-format -i {cpp_files}",
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
        ctx.run(cmd, echo=True, env={})


@task
def create_build_dir(ctx):
    """Build"""
    for cmd in ("mkdir -p build",):
        ctx.run(cmd, echo=True)


@task(create_build_dir)
def build(ctx):
    """Build"""
    for cmd in (
        "poetry build -vv",
        f"conan create . --build=missing --profile={conan_dir}/profiles/default -o boost/*:without_cobalt=True",
    ):
        ctx.run(cmd, echo=True)


@task
def build_docs(ctx):
    """Build docs"""
    doc_dir = script_dir / "docs"
    build_dir = script_dir / "build" / "docs"
    build_dir.mkdir(parents=True, exists_ok=True)
    with ctx.cd(build_dir):
        for cmd in (
            f"cmake -DVERSION={version} {doc_dir}",
            "cmake --build build",
            f"sphinx-apidoc -P -f -o {doc_dir / '_source'} {script_dir}/src/cxx",
            f"sphinx-build -Dversion={version} -Drelease={version} "
            f"-Aversion={version} -Aversions={','.join(versions)} -b html {doc_dir} .",
        ):
            with ctx.cd(d):
                ctx.run(cmd, echo=True)


@task
def clean(ctx):
    """Clean"""
    for cmd in ("rm -rf build",):
        ctx.run(cmd, echo=True)


@task(clean, build)
def rebuild(ctx): ...
