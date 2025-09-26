/**
 * \file
 * \brief Provide python bindings for C++ objects and functions
 *
 * \author AUTHOR <EMAIL>
 */

#include <pybind11/pybind11.h>

#include "PROJECT/config.h"
#include "PROJECT/version.h"

namespace py = pybind11;

using namespace PROJECT;

PYBIND11_MODULE(pycxxPROJECT, m) {
  m.doc() = "PROJECT C++ module";
  m.attr("__version__") = STRINGIFY(VERSION);
}
