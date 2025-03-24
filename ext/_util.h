#pragma once

#include <ft2build.h>
#include FT_ADVANCES_H
#include FT_FONT_FORMATS_H
#include FT_FREETYPE_H
#include FT_GLYPH_H
#include FT_OUTLINE_H
#include FT_SFNT_NAMES_H
#include FT_TRUETYPE_IDS_H
#include FT_TRUETYPE_TABLES_H
#include FT_TYPE1_TABLES_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <unordered_map>
#include <vector>

namespace matplotlib::ft2 {

namespace py = pybind11;

namespace detail {

extern std::unordered_map<FT_Error, std::string> ft_errors;

}

}

#define FT_CHECK(func, ...) { \
  if (auto error_ = func(__VA_ARGS__)) { \
    throw \
      std::runtime_error( \
        #func " (" __FILE__ " line " + std::to_string(__LINE__) + ") failed " \
        "with error: " + ft2::detail::ft_errors.at(error_)); \
  } \
}

#define PY_CHECK(func, ...) [&] { \
  auto const value_ = func(__VA_ARGS__); \
  if (PyErr_Occurred()) { \
    throw pybind11::error_already_set{}; \
  } else { \
    return value_; \
  } \
}()
