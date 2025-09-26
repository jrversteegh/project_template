import configparser
import os
from datetime import datetime
from pathlib import Path

import tomli
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy
from conan.tools.scm import Version

from conan import ConanFile


def get_project_name_version_and_description(source_dir):
    source_dir = Path(source_dir)
    pyproject_toml = source_dir / "pyproject.toml"
    if not pyproject_toml.exists():
        # For some reason, during install, poetry renames pyproject.toml to pyproject.tmp...
        pyproject_toml = source_dir / "pyproject.tmp"

    # Create header with version info
    with open(pyproject_toml, "rb") as f:
        project = tomli.load(f)
        name = project["tool"]["poetry"]["name"]
        version = project["tool"]["poetry"]["version"]
        description = project["tool"]["poetry"]["description"]
    return name, version, description


class PROJECTConan(ConanFile):
    name, version, description = get_project_name_version_and_description()

    license = "BSD"
    author = "AUTHOR <EMAIL>"
    url = "https://example.com"

    generators = "CMakeDeps"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = (
        "pyproject.toml",
        "CMakeLists.txt",
        "src/PROJECT/*",
        "include/PROJECT/*",
        "conanfile.txt",
    )

    def requirements(self):
        self.requires("fmt/11.2.0")

    def validate(self):
        compiler = self.settings.compiler
        version = int(str(Version(self.settings.compiler.version)))

        if compiler == "gcc" and version < 14:
            raise ConanInvalidConfiguration("GCC needs to be version 14 or up")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        version, date = get_project_version_and_date(self.source_folder)
        tc.variables["VERSION"] = version
        tc.variables["DATE"] = date
        tc.variables["BUILD_PYTHON"] = "0"
        tc.variables["BUILD_TESTS"] = "0"
        tc.variables["BUILD_SHARED"] = "1"
        tc.variables["CMAKE_BUILD_TYPE"] = self.settings.build_type
        if self.settings.os == "Windows":
            tc.variables["CMAKE_POLICY_DEFAULT_CMP0091"] = "NEW"
        tc.generate()

    def package(self):
        src = Path(self.source_folder)
        bld = Path(self.build_folder)
        pkg = Path(self.package_folder)
        copy(self, "*.h", dst=pkg / "include", src=src / "include")
        copy(self, "*.lib", dst=pkg / "lib", src=bld)
        copy(self, "*.a", dst=pkg / "lib", src=bld)
        copy(self, "*.so", dst=pkg / "lib", src=bld)

    def package_info(self):
        self.cpp_info.libs = ["PROJECT"]

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
