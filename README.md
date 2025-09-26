Project Template
=

This template sets up the scaffolding for a C++/Python project.

Requirements
-

Installation of the template only requires a valid python interpreter on the path, 
but the resulting project requires the following to be build:
 * Python 3.12 or newer
 * Poetry 2.0 or newer. See https://python-poetry.org/docs/#installation
 * GCC 14, Clang 19 or VS 2022 C++ compiler or newer versions of these
 * Additional tooling for building installers

Usage
-
Run `<path_to_this_repo>/install.py <your_project_name> <your_name> <your_email> [<your_project_description>]`
in the directory where you want to create a project based on this template

Contents
-
This template contains boiler plate for the following:
  * Building static and shared libraries from C++ code and optionally and executable binary
  * Creating a conan recipe for installation in local cache (so other projects can use this one)
  * Building a python binding for the C++ project
  * Maintaining a python project that includes the C++ binding
  * Creating Sphinx documentation that combines python doc strings and C++ doxygen documentation
  * Building installers for Windows `(*.msi)` and Linux `(*.deb)`
 
Getting started
-
After the project has been created, the first step is to create a python virtual environment
and install the projects requirements. This can be done with `poetry install`. After that
a shell can be created in the new environment with `poetry shell`. Now you can run tasks from 
`tasks.py` using invoke. Run `inv -l` to show a list of available tasks.
