#include "_ft2.h"
#include "_layout.h"
#include "_p11x_enum.h"
#include "_sfnt_tables.h"

#define ITER_ENUM(ENUM_ITEM) \
  ENUM_ITEM(SCALABLE), \
  ENUM_ITEM(FIXED_SIZES), \
  ENUM_ITEM(FIXED_WIDTH), \
  ENUM_ITEM(SFNT), \
  ENUM_ITEM(HORIZONTAL), \
  ENUM_ITEM(VERTICAL), \
  ENUM_ITEM(KERNING), \
  ENUM_ITEM(FAST_GLYPHS), \
  ENUM_ITEM(MULTIPLE_MASTERS), \
  ENUM_ITEM(GLYPH_NAMES), \
  ENUM_ITEM(EXTERNAL_STREAM), \
  ENUM_ITEM(HINTER), \
  ENUM_ITEM(CID_KEYED), \
  ENUM_ITEM(TRICKY), \
  ENUM_ITEM(COLOR)
  #define ENUM_ITEM(name) name = FT_FACE_FLAG_##name
    enum class FaceFlag { ITER_ENUM(ENUM_ITEM) };
  #undef ENUM_ITEM
  #define ENUM_ITEM(name) {#name, FaceFlag::name}
    P11X_DECLARE_ENUM("FaceFlag", "enum.IntFlag", ITER_ENUM(ENUM_ITEM))
  #undef ENUM_ITEM
#undef ITER_ENUM

#define ITER_ENUM(ENUM_ITEM) \
  ENUM_ITEM(DEFAULT), \
  ENUM_ITEM(NO_SCALE), \
  ENUM_ITEM(NO_HINTING), \
  ENUM_ITEM(RENDER), \
  ENUM_ITEM(NO_BITMAP), \
  ENUM_ITEM(VERTICAL_LAYOUT), \
  ENUM_ITEM(FORCE_AUTOHINT), \
  ENUM_ITEM(CROP_BITMAP), \
  ENUM_ITEM(PEDANTIC), \
  ENUM_ITEM(IGNORE_GLOBAL_ADVANCE_WIDTH), \
  ENUM_ITEM(NO_RECURSE), \
  ENUM_ITEM(IGNORE_TRANSFORM), \
  ENUM_ITEM(MONOCHROME), \
  ENUM_ITEM(LINEAR_DESIGN), \
  ENUM_ITEM(NO_AUTOHINT), \
  ENUM_ITEM(TARGET_NORMAL), \
  ENUM_ITEM(TARGET_LIGHT), \
  ENUM_ITEM(TARGET_MONO), \
  ENUM_ITEM(TARGET_LCD), \
  ENUM_ITEM(TARGET_LCD_V), \
  ENUM_ITEM(COLOR), \
  ENUM_ITEM(COMPUTE_METRICS)
  // ENUM_ITEM(LOAD_BITMAP_METRICS_ONLY),  // NOTE: Not available in 2.6.1.
  #define ENUM_ITEM(name) name = FT_LOAD_##name
    enum class Load { ITER_ENUM(ENUM_ITEM) };
  #undef ENUM_ITEM
  #define ENUM_ITEM(name) {#name, Load::name}
    P11X_DECLARE_ENUM("Load", "enum.IntFlag", ITER_ENUM(ENUM_ITEM))
  #undef ENUM_ITEM
#undef ITER_ENUM

#define ITER_ENUM(ENUM_ITEM) \
  ENUM_ITEM(ITALIC), \
  ENUM_ITEM(BOLD)
  #define ENUM_ITEM(name) name = FT_STYLE_FLAG_##name
    enum class StyleFlag { ITER_ENUM(ENUM_ITEM) };
  #undef ENUM_ITEM
  #define ENUM_ITEM(name) {#name, StyleFlag::name}
    P11X_DECLARE_ENUM("StyleFlag", "enum.IntFlag", ITER_ENUM(ENUM_ITEM))
  #undef ENUM_ITEM
#undef ITER_ENUM

#define ITER_ENUM(ENUM_ITEM) \
  ENUM_ITEM(NONE), \
  ENUM_ITEM(MS_SYMBOL), \
  ENUM_ITEM(UNICODE), \
  ENUM_ITEM(SJIS), \
  ENUM_ITEM(PRC), \
  ENUM_ITEM(BIG5), \
  ENUM_ITEM(WANSUNG), \
  ENUM_ITEM(JOHAB), \
  ENUM_ITEM(ADOBE_STANDARD), \
  ENUM_ITEM(ADOBE_EXPERT), \
  ENUM_ITEM(ADOBE_CUSTOM), \
  ENUM_ITEM(ADOBE_LATIN_1), \
  ENUM_ITEM(OLD_LATIN_2), \
  ENUM_ITEM(APPLE_ROMAN)
  #define ENUM_ITEM(name) {#name, FT_ENCODING_##name}
    P11X_DECLARE_ENUM("Encoding", "enum.IntEnum", ITER_ENUM(ENUM_ITEM))
  #undef ENUM_ITEM
#undef ITER_ENUM

#define ITER_ENUM(ENUM_ITEM) \
  ENUM_ITEM(DEFAULT), \
  ENUM_ITEM(UNFITTED), \
  ENUM_ITEM(UNSCALED)
  #define ENUM_ITEM(name) {#name, FT_KERNING_##name}
    P11X_DECLARE_ENUM("Kerning", "enum.IntEnum", ITER_ENUM(ENUM_ITEM))
  #undef ENUM_ITEM
#undef ITER_ENUM

#define ITER_ENUM(ENUM_ITEM) \
  ENUM_ITEM(UNSCALED), \
  ENUM_ITEM(SUBPIXELS), \
  ENUM_ITEM(GRIDFIT), \
  ENUM_ITEM(TRUNCATE), \
  ENUM_ITEM(PIXELS)
  #define ENUM_ITEM(name) {#name, FT_GLYPH_BBOX_##name}
    P11X_DECLARE_ENUM("GlyphBbox", "enum.IntEnum", ITER_ENUM(ENUM_ITEM))
  #undef ENUM_ITEM
#undef ITER_ENUM

#define ITER_ENUM(ENUM_ITEM) \
  ENUM_ITEM(NONE), \
  ENUM_ITEM(COMPOSITE), \
  ENUM_ITEM(BITMAP), \
  ENUM_ITEM(OUTLINE), \
  ENUM_ITEM(PLOTTER)
  #define ENUM_ITEM(name) {#name, FT_GLYPH_FORMAT_##name}
    P11X_DECLARE_ENUM("GlyphFormat", "enum.IntEnum", ITER_ENUM(ENUM_ITEM))
  #undef ENUM_ITEM
#undef ITER_ENUM

namespace matplotlib::ft2 {

Face::Face(
  std::string const& path, std::optional<FT_Long> index, double hinting_factor) :
  ptr{
    [&]() -> std::shared_ptr<FT_FaceRec> {
      auto face = FT_Face{};
      if (!index) {
        FT_CHECK(FT_New_Face, library, path.data(), -1, &face);
        if (face->num_faces != 1) {
          throw std::runtime_error(
            "More that one face in font file; index must be set");
        }
        *index = 0;
        FT_CHECK(FT_Done_Face, face);  // ... and continue loading.
      }
      FT_CHECK(FT_New_Face, library, path.data(), *index, &face);
      auto transform = FT_Matrix{
        FT_Fixed(65536. / hinting_factor), 0, 0, 65536};
      FT_Set_Transform(face, &transform, nullptr);
      return {face, FT_Done_Face};
    }()
  },
  path{path},
  index{index ? *index : 0},
  hinting_factor{hinting_factor}
{}

CharMap::CharMap(Face const& face, FT_Int index) :
  face{py::cast(face)},
  index{index}
{}

Glyph::Glyph(FT_Face const& face, double hinting_factor) :
  ptr{
    [&]() -> std::shared_ptr<FT_GlyphRec> {
      auto glyph = FT_Glyph{};
      FT_CHECK(FT_Get_Glyph, face->glyph, &glyph);
      return {glyph, FT_Done_Glyph};
    }()
  },
  metrics{face->glyph->metrics},
  linearHoriAdvance{face->glyph->linearHoriAdvance},
  linearVertAdvance{face->glyph->linearVertAdvance},
  hinting_factor{hinting_factor}
{}

PYBIND11_MODULE(_ft2, m)
{
  using namespace pybind11::literals;
  using namespace std::string_literals;

  m.doc() = R"__doc__(
A wrapper extension module for FreeType2.

Unless stated otherwise, all methods directly wrap a corresponding FreeType
function, and all lengths of this API are either in pixels (if FreeType
intenally uses 26.6 or 16.16 fixed point -- conversion is handled by this
module) or in font units (if FreeType internally uses font units).  The latter
case is explicitly mentioned where applicable.
)__doc__";

  FT_CHECK(FT_Init_FreeType, &library);

  auto major = FT_Int{}, minor = FT_Int{}, patch = FT_Int{};
  FT_Library_Version(library, &major, &minor, &patch);
  m.attr("__freetype_version__")
    = std::to_string(major) + "."
      + std::to_string(minor) + "."
      + std::to_string(patch);

  p11x::bind_enums(m);

  py::class_<Face>(m, "Face", R"__doc__(
A lightweight wrapper around a ``FT_Face``.

Length attributes of this class (`ascender`, `descender`, etc.) are in font
units.
)__doc__")
    .def(
      py::init(
        [](py::object path, std::optional<FT_Long> index, double hinting_factor)
        -> Face* {
          PyBytesObject* path_bytes = nullptr;
          PY_CHECK(PyUnicode_FSConverter, path.ptr(), &path_bytes);
          auto path_bytes_11 =  // For cleanup.
            py::reinterpret_steal<py::bytes>(
              reinterpret_cast<PyObject*>(path_bytes));
          return new Face{
            PY_CHECK(PyBytes_AsString, path_bytes_11.ptr()),
            index, hinting_factor};
        }),
      "path"_a, "index"_a=py::none(), "hinting_factor"_a=1,
      R"__doc__(
Load a `Face` from a bytestring path name, encoded with the file system
encoding.
)__doc__")

    .def_property_readonly(
      "path",
      [](Face const& pyface) -> std::string const& { return pyface.path; },
      R"__doc__(
The path from which the `Face` was loaded.
)__doc__")

#define DECLARE_FIELD(prop, ...) \
  .def_property_readonly( \
    #prop, [](Face const& pyface) { return __VA_ARGS__(pyface.ptr->prop); })
    DECLARE_FIELD(num_faces)
    DECLARE_FIELD(face_index, [](auto i) { return i & 0xffff; })
    .def_property_readonly(
      "named_instance_index",
      [](Face const& pyface) {
        return pyface.ptr->face_index >> 16;
      })
    DECLARE_FIELD(face_flags, FaceFlag)
    DECLARE_FIELD(style_flags, [](auto s) { return StyleFlag(s & 0xffff); })
    .def_property_readonly(
      "num_named_instances",
      [](Face const& pyface) {
        return pyface.ptr->style_flags >> 16;
      })
    DECLARE_FIELD(num_glyphs)
    DECLARE_FIELD(family_name)
    DECLARE_FIELD(style_name)
    DECLARE_FIELD(num_fixed_sizes)
    .def_property_readonly(
      "available_sizes",
      [](Face const& pyface) -> std::vector<py::dict> {
        auto sizes = std::vector<py::dict>{};
        for (auto i = 0; i < pyface.ptr->num_fixed_sizes; ++i) {
          auto c_size = pyface.ptr->available_sizes[i];
          auto size = py::dict{};
          size["height"] = c_size.height;
          size["width"] = c_size.width;
          size["size"] = c_size.size;
          size["x_ppem"] = c_size.x_ppem / 64.;
          size["y_ppem"] = c_size.y_ppem / 64.;
          sizes.push_back(size);
        }
        return sizes;
      })
    DECLARE_FIELD(num_charmaps)
    .def_property_readonly(
      "charmaps",
      [](Face& pyface) -> std::vector<CharMap> {
        auto charmaps = std::vector<CharMap>{};
        for (auto i = 0; i < pyface.ptr->num_charmaps; ++i) {
          charmaps.emplace_back(pyface, i);
        }
        return charmaps;
      })
    // generic -> not supported.
    .def_property_readonly(
      "bbox",
      [](Face const& pyface) -> std::tuple<FT_Pos, FT_Pos, FT_Pos, FT_Pos> {
        auto [xmin, ymin, xmax, ymax] = pyface.ptr->bbox;
        return {xmin, ymin, xmax, ymax};
      })
    DECLARE_FIELD(units_per_EM)
    DECLARE_FIELD(ascender)
    DECLARE_FIELD(descender)
    DECLARE_FIELD(height)
    DECLARE_FIELD(max_advance_width)
    DECLARE_FIELD(max_advance_height)
    DECLARE_FIELD(underline_position)
    DECLARE_FIELD(underline_thickness)
    .def_property_readonly(
      "glyph",
      [](Face const& pyface) -> Glyph {
        return {pyface.ptr.get(), pyface.hinting_factor};
      })
    .def_property_readonly(
      "size",
      [](Face const& pyface) -> py::dict {
        auto metrics = pyface.ptr->size->metrics;
        return py::dict(
          "x_ppem"_a=metrics.x_ppem,
          "y_ppem"_a=metrics.y_ppem,
          "x_scale"_a=metrics.x_scale / 65536. / 64.,
          "y_scale"_a=metrics.y_scale / 65536. / 64.,
          "ascender"_a=metrics.ascender / 64.,
          "descender"_a=metrics.descender / 64.,
          "height"_a=metrics.height / 64.,
          "max_advance"_a=metrics.max_advance / 64.);
      })
    .def_property_readonly(
      "charmap",
      [](Face& pyface) -> CharMap {
        auto idx = FT_Get_Charmap_Index(pyface.ptr->charmap);
        if (idx == -1) {
          throw std::runtime_error("Failed to retrieve charmap index");
        }
        return {pyface, idx};
      })
#undef DECLARE_FIELD

    .def(
      "attach_file",
      [](Face const& pyface, py::bytes path) -> void {
        FT_CHECK(
          FT_Attach_File, pyface.ptr.get(), path.cast<std::string>().data());
      },
      "path"_a)
    .def(
      "face_get_chars_of_variant",
      [](Face const& pyface, FT_ULong variantSelector) -> std::vector<FT_UInt32> {
        auto cs = FT_Face_GetCharsOfVariant(pyface.ptr.get(), variantSelector);
        return {cs, std::find(cs, cs + 0x10ffff, 0)};
      },
      "variant_selector"_a)
    .def(
      "face_get_variant_selectors",
      [](Face const& pyface) -> std::vector<FT_UInt32> {
        auto vs = FT_Face_GetVariantSelectors(pyface.ptr.get());
        return {vs, std::find(vs, vs + 0x10ffff, 0)};
      })
    .def(
      "get_advance",
      [](Face const& pyface, FT_UInt gindex, FT_Int32 flags) {
        auto advance = FT_Fixed{};
        FT_CHECK(FT_Get_Advance, pyface.ptr.get(), gindex, flags, &advance);
        auto pyadvance = std::variant<double, FT_Fixed>{};
        if (flags & FT_LOAD_NO_SCALE) {
          pyadvance = advance;
        } else {
          pyadvance = advance / 65536.;
        }
        return pyadvance;
      })
    .def(
      "get_char_index",
      [](Face const& pyface, FT_ULong codepoint) -> FT_UInt {
        return FT_Get_Char_Index(pyface.ptr.get(), codepoint);
      },
      "codepoint"_a)
    .def(  // Only one glyph per codepoint is listed, not (e.g.) variants!
      "_get_chars",
      [](Face const& pyface) -> std::vector<std::tuple<FT_ULong, FT_UInt, std::string>> {
        auto face = pyface.ptr.get();
        auto names = std::vector<std::tuple<FT_ULong, FT_UInt, std::string>>{};
        auto index = FT_UInt{};
        auto charcode = FT_Get_First_Char(face, &index);
        while (index) {
          char buffer[64];  // AFDKO Feature File Specification;
          FT_CHECK(FT_Get_Glyph_Name, face, index, buffer, 64);
          names.emplace_back(charcode, index, buffer);
          charcode = FT_Get_Next_Char(face, charcode, &index);
        }
        return names;
      })
    .def(
      "get_font_format",
      [](Face const& pyface) -> std::string {
        // NOTE Deprecated & renamed to FT_Get_Font_Format in FreeType 2.6.
        return FT_Get_X11_Font_Format(pyface.ptr.get());
      })
    .def(
      "get_glyph_name",
      [](Face const& pyface, FT_UInt index) -> std::string {
        char buf[128];  // Limit to PS identifier size.
        FT_CHECK(  // This will throw if !FT_HAS_GLYPH_NAMES(face).
          FT_Get_Glyph_Name, pyface.ptr.get(), index, buf, 128);
        return buf;
      },
      "index"_a)
    .def(
      "get_kerning",
      [](Face const& pyface, FT_UInt left, FT_UInt right, FT_Kerning_Mode mode)
      -> std::tuple<double, double> {
        if (FT_HAS_KERNING(pyface.ptr.get())) {
          if (mode == FT_KERNING_UNSCALED) {
            // So that whoever *actually* needs this can implement the correct
            // conversion factor.
            throw
              std::runtime_error("Unknown conversion for FT_KERNING_UNSCALED");
          }
          auto delta = FT_Vector{};
          FT_CHECK(
            FT_Get_Kerning, pyface.ptr.get(), left, right, mode, &delta);
          return {delta.x / 64., delta.y / 64.};
        } else {
          return {0, 0};
        }
      },
      "left"_a, "right"_a, "mode"_a)
    .def(
      "get_name_index",
      [](Face const& pyface, std::string glyph_name) -> FT_UInt {
        return FT_Get_Name_Index(pyface.ptr.get(), glyph_name.data());
      },
      "glyph_name"_a)
    .def(
      "get_postscript_name",
      [](Face const& pyface) -> char const* {
        return FT_Get_Postscript_Name(pyface.ptr.get());
      })
#define COPY_FIELD(field) { \
    using type = decltype(ptr->field); \
    if constexpr (std::is_array_v<type>) { \
      table[#field] = \
        *std::launder(reinterpret_cast< \
          std::array<std::remove_extent_t<type>, std::extent_v<type>>*>( \
            &ptr->field)); \
    } else { \
      table[#field] = ptr->field; \
    } \
  }
    .def(
      "get_ps_font_info",
      [](Face const& pyface) -> py::dict {
        auto psfontinfo = PS_FontInfoRec{};
        auto ptr = &psfontinfo;
        FT_CHECK(FT_Get_PS_Font_Info, pyface.ptr.get(), ptr);
        auto table = py::dict{};
        COPY_FIELD(version);
        COPY_FIELD(notice);
        COPY_FIELD(full_name);
        COPY_FIELD(family_name);
        COPY_FIELD(weight);
        COPY_FIELD(italic_angle);
        COPY_FIELD(is_fixed_pitch);
        COPY_FIELD(underline_position);
        COPY_FIELD(underline_thickness);
        return table;
      })
    .def(
      "get_ps_font_private",
      [](Face const& pyface) -> py::dict {
        auto psfontprivate = PS_PrivateRec{};
        auto ptr = &psfontprivate;
        FT_CHECK(FT_Get_PS_Font_Private, pyface.ptr.get(), ptr);
        auto table = py::dict{};
        COPY_FIELD(unique_id);
        COPY_FIELD(lenIV);
        COPY_FIELD(num_blue_values);
        COPY_FIELD(num_other_blues);
        COPY_FIELD(num_family_blues);
        COPY_FIELD(num_family_other_blues);
        COPY_FIELD(blue_values);
        COPY_FIELD(other_blues);
        COPY_FIELD(family_blues);
        COPY_FIELD(family_other_blues);
        table["blue_scale"] = psfontprivate.blue_scale / 65536.;
        COPY_FIELD(blue_shift);
        COPY_FIELD(blue_fuzz);
        COPY_FIELD(standard_width);
        COPY_FIELD(standard_height);
        COPY_FIELD(num_snap_widths);
        COPY_FIELD(num_snap_heights);
        COPY_FIELD(force_bold);
        COPY_FIELD(round_stem_up);
        COPY_FIELD(snap_widths);
        COPY_FIELD(snap_heights);
        table["expansion_factor"] = psfontprivate.expansion_factor / 65536.;
        COPY_FIELD(language_group);
        COPY_FIELD(password);
        COPY_FIELD(min_feature);
        return table;
      })
    .def(
      "get_sfnt_name_table",
      // See also https://www.microsoft.com/typography/otspec/name.htm wrt
      // encoding.
      [](Face const& pyface) -> py::dict {
        auto face = pyface.ptr.get();
        if (!FT_IS_SFNT(face)) {
          throw std::runtime_error("Font not using the SFNT storage scheme");
        }
        auto table = py::dict{};
        auto name_count = FT_Get_Sfnt_Name_Count(face);
        for (auto i = 0u; i < name_count; ++i) {
          auto sfnt_name = FT_SfntName{};
          FT_CHECK(FT_Get_Sfnt_Name, face, i, &sfnt_name);
          py::object
            entry = py::bytes((char*)(sfnt_name.string), sfnt_name.string_len),
            encoding_id = py::cast(sfnt_name.encoding_id),
            language_id = py::cast(sfnt_name.language_id);
          if (sfnt_name.language_id >= 0x8000) {
            auto lang_tag = FT_SfntLangTag{};
            // Can also fail for 'name' table format 0...
            if (!FT_Get_Sfnt_LangTag(face, sfnt_name.language_id, &lang_tag)) {
              language_id =
                py::bytes((char*)lang_tag.string, lang_tag.string_len);
            }
          }
          switch (sfnt_name.platform_id) {
            case TT_PLATFORM_APPLE_UNICODE:
              if (sfnt_name.language_id == 0) {  // Should always be the case.
                language_id = py::cast("");
              }
              entry = entry.attr("decode")("utf-16-be");
              break;
            case TT_PLATFORM_MACINTOSH:
              if (sfnt_name.language_id < 0x8000) {
                language_id =
                  py::cast(detail::tt_mac_langids.at(sfnt_name.language_id));
              }
              if (sfnt_name.encoding_id == sfnt_name.language_id) {
                // This seems to happen quite often; then the encoding is
                // usually wrong and the language is correct (fc just gives up
                // after some fudging)...
                // https://en.wikipedia.org/wiki/Code_page#Macintosh_emulation_code_pages_2
                switch (sfnt_name.language_id) {
                  case TT_MAC_LANGID_ENGLISH:
                    // e.g. Corsiva.ttc claims (incorrectly) to use Hebrew
                    // encoding...
                    encoding_id = py::cast("MAC_ROMAN");
                    break;
                  case TT_MAC_LANGID_JAPANESE:  // 11
                    encoding_id = py::cast("X_MAC_JAPANESE");
                    break;
                  case TT_MAC_LANGID_ARABIC:  // 12
                    encoding_id = py::cast("MAC_ARABIC");
                    break;
                  case TT_MAC_LANGID_CHINESE_TRADITIONAL:  // 19
                    encoding_id = py::cast("X_MAC_TRAD_CHINESE");
                    break;
                  case TT_MAC_LANGID_KOREAN:  // 23
                    encoding_id = py::cast("X_MAC_KOREAN");
                    break;
                  // http://www.unicode.org/Public/MAPPINGS/VENDORS/APPLE/CENTEURO.TXT
                  case TT_MAC_LANGID_LITHUANIAN:  // 24
                  case TT_MAC_LANGID_POLISH:  // 25
                  case TT_MAC_LANGID_HUNGARIAN:  // 26
                  case TT_MAC_LANGID_ESTONIAN:  // 27
                  case TT_MAC_LANGID_LETTISH:  // 28
                  case TT_MAC_LANGID_CZECH:  // 38
                  case TT_MAC_LANGID_SLOVAK:  // 39
                    encoding_id = py::cast("MAC_CENTEURO");
                    break;
                  case TT_MAC_LANGID_FARSI:  // 31
                    encoding_id = py::cast("MAC_FARSI");
                    break;
                  case TT_MAC_LANGID_RUSSIAN:  // 32
                  case TT_MAC_LANGID_BULGARIAN:  // 44
                  case TT_MAC_LANGID_UKRAINIAN:  // 45
                  case TT_MAC_LANGID_BYELORUSSIAN:  // 46
                    encoding_id = py::cast("MAC_CYRILLIC");
                    break;
                  case TT_MAC_LANGID_CHINESE_SIMPLIFIED:  // 33
                    encoding_id = py::cast("X_MAC_SIMP_CHINESE");
                    break;
                  default:
                    goto skip_decode;
                }
                entry = entry.attr("decode")(encoding_id, "backslashreplace");
                // If encoding_id == language_id == 0, then the encoding was
                // actually correct.
                if (sfnt_name.encoding_id != 0) {
                  // Not += which doesn't actually update the immutable string.
                  encoding_id = encoding_id + py::cast(" <inferred>");
                }
              } else {
                switch (sfnt_name.encoding_id) {
                  case TT_MAC_ID_ROMAN:  // 0
                    encoding_id = py::cast("MAC_ROMAN");
                    break;
                  case TT_MAC_ID_JAPANESE:  // 1
                    encoding_id = py::cast("X_MAC_JAPANESE");
                    break;
                  case TT_MAC_ID_TRADITIONAL_CHINESE:  // 2
                    encoding_id = py::cast("X_MAC_TRAD_CHINESE");
                    break;
                  case TT_MAC_ID_KOREAN:  // 3
                    encoding_id = py::cast("X_MAC_KOREAN");
                    break;
                  case TT_MAC_ID_ARABIC:  // 4
                    encoding_id = py::cast("MAC_ARABIC");
                    break;
                  case TT_MAC_ID_HEBREW:  // 5
                    encoding_id = py::cast("X_MAC_HEBREW");
                    entry =
                      py::module::import("freetypybind._x_mac_hebrew")
                      .attr("Codec")().attr("decode")(entry, "backslashreplace")[py::int_(0)];
                    goto skip_decode;
                  case TT_MAC_ID_RUSSIAN:  // 7
                    encoding_id = py::cast("MAC_CYRILLIC");
                    break;
                  case TT_MAC_ID_SIMPLIFIED_CHINESE:  // 25
                    encoding_id = py::cast("X_MAC_SIMP_CHINESE");
                    break;
                  case TT_MAC_ID_SLAVIC:  // 29
                    encoding_id = py::cast("MAC_CENTEURO");
                    break;
                  default:
                    goto skip_decode;
                }
                entry = entry.attr("decode")(encoding_id, "backslashreplace");
              }
              break;
            case TT_PLATFORM_MICROSOFT:
              if (sfnt_name.language_id < 0x8000) {
                language_id =
                  py::cast(detail::tt_ms_langids.at(sfnt_name.language_id));
              }
              // https://www.microsoft.com/typography/otspec/name.htm ("string
              // data must be encoded in UTF-16BE").
              entry = entry.attr("decode")("utf-16-be");
              break;
          }
          skip_decode: ;
          py::object name_id =
            sfnt_name.name_id < detail::tt_name_ids.size()
            ? py::cast(detail::tt_name_ids[sfnt_name.name_id])
            // Future expansions or font-specific features.
            : py::cast(sfnt_name.name_id);
          table[py::make_tuple(detail::tt_platforms.at(sfnt_name.platform_id),
                               encoding_id,
                               language_id,
                               name_id)]
            = entry;
        }
        return table;
      }, R"__doc__(
Return the SFNT names table.

The returned dict maps ``(platform_id, encoding_id, language_id, name_id)``
keys to the corresponding 'name' bytestrings.
)__doc__")
    .def(
      "get_sfnt_table",
      [](Face const& pyface, std::string tag) -> std::optional<py::dict> {
        auto face = pyface.ptr.get();
        if (!FT_IS_SFNT(face)) {
          throw std::runtime_error("Font not using the SFNT storage scheme");
        }
        auto table = py::dict{};
        if (tag == "head") {
          auto ptr =
            static_cast<TT_Header*>(FT_Get_Sfnt_Table(face, FT_SFNT_HEAD));
          if (!ptr) {
            return {};
          }
          COPY_FIELD(Table_Version);
          COPY_FIELD(Font_Revision);
          COPY_FIELD(CheckSum_Adjust);
          COPY_FIELD(Magic_Number);
          COPY_FIELD(Flags);
          COPY_FIELD(Units_Per_EM);
          COPY_FIELD(Created);
          COPY_FIELD(Modified);
          COPY_FIELD(xMin);
          COPY_FIELD(yMin);
          COPY_FIELD(xMax);
          COPY_FIELD(yMax);
          COPY_FIELD(Mac_Style);
          COPY_FIELD(Lowest_Rec_PPEM);
          COPY_FIELD(Font_Direction);
          COPY_FIELD(Index_To_Loc_Format);
          COPY_FIELD(Glyph_Data_Format);
        } else if (tag == "maxp") {
          auto ptr =
            static_cast<TT_MaxProfile*>(FT_Get_Sfnt_Table(face, FT_SFNT_MAXP));
          COPY_FIELD(version);
          COPY_FIELD(numGlyphs);
          COPY_FIELD(maxPoints);
          COPY_FIELD(maxContours);
          COPY_FIELD(maxCompositePoints);
          COPY_FIELD(maxCompositeContours);
          COPY_FIELD(maxZones);
          COPY_FIELD(maxTwilightPoints);
          COPY_FIELD(maxStorage);
          COPY_FIELD(maxFunctionDefs);
          COPY_FIELD(maxInstructionDefs);
          COPY_FIELD(maxStackElements);
          COPY_FIELD(maxSizeOfInstructions);
          COPY_FIELD(maxComponentElements);
          COPY_FIELD(maxComponentDepth);
        } else if (tag == "OS/2") {
          auto ptr =
            static_cast<TT_OS2*>(FT_Get_Sfnt_Table(face, FT_SFNT_OS2));
          if (!ptr) {
            return {};
          }
          // NOTE: Don't bother with optional tags.
          COPY_FIELD(version);
          COPY_FIELD(xAvgCharWidth);
          COPY_FIELD(usWeightClass);
          COPY_FIELD(usWidthClass);
          COPY_FIELD(fsType);
          COPY_FIELD(ySubscriptXSize);
          COPY_FIELD(ySubscriptYSize);
          COPY_FIELD(ySubscriptXOffset);
          COPY_FIELD(ySubscriptYOffset);
          COPY_FIELD(ySuperscriptXSize);
          COPY_FIELD(ySuperscriptYSize);
          COPY_FIELD(ySuperscriptXOffset);
          COPY_FIELD(ySuperscriptYOffset);
          COPY_FIELD(yStrikeoutSize);
          COPY_FIELD(yStrikeoutPosition);
          COPY_FIELD(sFamilyClass);
          table["panose"] = py::bytes((char*)(ptr->panose), 10);
          auto unicode_range = std::vector<uint8_t>{};
          for (auto i = 0; i < 32; ++i) {
            if ((ptr->ulUnicodeRange1 >> i) & 1) {
              unicode_range.push_back(i);
            }
          }
          for (auto i = 0; i < 32; ++i) {
            if ((ptr->ulUnicodeRange2 >> i) & 1) {
              unicode_range.push_back(i + 32);
            }
          }
          for (auto i = 0; i < 32; ++i) {
            if ((ptr->ulUnicodeRange3 >> i) & 1) {
              unicode_range.push_back(i + 64);
            }
          }
          for (auto i = 0; i < 32; ++i) {
            if ((ptr->ulUnicodeRange4 >> i) & 1) {
              unicode_range.push_back(i + 96);
            }
          }
          table["unicodeRange"] = unicode_range;
          table["achVendID"] =
            // Technically a key into a registry of vendors; all values so far
            // are ASCII.
            py::bytes((char*)(ptr->achVendID), 4).attr("decode")("latin-1");
          COPY_FIELD(fsSelection);
          COPY_FIELD(usFirstCharIndex);
          COPY_FIELD(usLastCharIndex);
          COPY_FIELD(sTypoAscender);
          COPY_FIELD(sTypoDescender);
          COPY_FIELD(sTypoLineGap);
          COPY_FIELD(usWinAscent);
          COPY_FIELD(usWinDescent);
        } else if (tag == "hhea") {
          auto ptr =
            static_cast<TT_HoriHeader*>(FT_Get_Sfnt_Table(face, FT_SFNT_HHEA));
          if (!ptr) {
            return {};
          }
          // NOTE: Skip reserved, {long,short}_metrics.
          COPY_FIELD(Version);
          COPY_FIELD(Ascender);
          COPY_FIELD(Descender);
          COPY_FIELD(Line_Gap);
          COPY_FIELD(advance_Width_Max);
          COPY_FIELD(min_Left_Side_Bearing);
          COPY_FIELD(min_Right_Side_Bearing);
          COPY_FIELD(xMax_Extent);
          COPY_FIELD(caret_Slope_Rise);
          COPY_FIELD(caret_Slope_Run);
          COPY_FIELD(caret_Offset);
          COPY_FIELD(metric_Data_Format);
          COPY_FIELD(number_Of_HMetrics);
        } else if (tag == "vhea") {
          auto ptr =
            static_cast<TT_VertHeader*>(FT_Get_Sfnt_Table(face, FT_SFNT_VHEA));
          if (!ptr) {
            throw std::runtime_error("No \"vhea\" table");
          }
          // NOTE: Skip reserved, {long,short}_metrics.
          COPY_FIELD(Version);
          COPY_FIELD(Ascender);
          COPY_FIELD(Descender);
          COPY_FIELD(Line_Gap);
          COPY_FIELD(advance_Height_Max);
          COPY_FIELD(min_Top_Side_Bearing);
          COPY_FIELD(min_Bottom_Side_Bearing);
          COPY_FIELD(yMax_Extent);
          COPY_FIELD(caret_Slope_Rise);
          COPY_FIELD(caret_Slope_Run);
          COPY_FIELD(caret_Offset);
          COPY_FIELD(metric_Data_Format);
          COPY_FIELD(number_Of_VMetrics);
        } else if (tag == "post") {
          auto ptr =
            static_cast<TT_Postscript*>(FT_Get_Sfnt_Table(face, FT_SFNT_POST));
          if (!ptr) {
            return {};
          }
          COPY_FIELD(FormatType);
          // NOTE: ft2font splits italicAngle into two uint16s but this seems wrong.
          COPY_FIELD(italicAngle);
          COPY_FIELD(underlinePosition);
          COPY_FIELD(underlineThickness);
          COPY_FIELD(isFixedPitch);
          COPY_FIELD(minMemType42);
          COPY_FIELD(maxMemType42);
          COPY_FIELD(minMemType1);
          COPY_FIELD(maxMemType1);
        } else if (tag == "pclt") {
          auto ptr =
            static_cast<TT_PCLT*>(FT_Get_Sfnt_Table(face, FT_SFNT_PCLT));
          if (!ptr) {
            return {};
          }
          // NOTE: Skip reserved.
          COPY_FIELD(Version);
          COPY_FIELD(FontNumber);
          COPY_FIELD(Pitch);
          COPY_FIELD(xHeight);
          COPY_FIELD(Style);
          COPY_FIELD(TypeFamily);
          COPY_FIELD(CapHeight);
          COPY_FIELD(SymbolSet);
          table["TypeFace"] = py::bytes((char*)(ptr->TypeFace), 16);
          table["CharacterComplement"] =
            py::bytes((char*)(ptr->CharacterComplement), 8);
          table["FileName"] = py::bytes((char*)(ptr->FileName), 6);
          COPY_FIELD(StrokeWeight);
          COPY_FIELD(WidthType);
          COPY_FIELD(SerifStyle);
        } else {
          throw std::runtime_error("Invalid SFNT table");
        }
        return table;
      })
#undef COPY_FIELD
    .def(
      "load_char",
      [](Face const& pyface, FT_ULong codepoint, FT_Int32 flags) -> void {
        FT_CHECK(FT_Load_Char, pyface.ptr.get(), codepoint, flags);
      },
      "codepoint"_a, "flags"_a)
    .def(
      "load_glyph",
      [](Face const& pyface, FT_UInt glyph_index, FT_Int32 flags) -> void {
        FT_CHECK(FT_Load_Glyph, pyface.ptr.get(), glyph_index, flags);
      },
      "glyph_index"_a, "flags"_a)
    .def(
      "set_char_size",
      [](Face const& pyface, double pt_size, double dpi) -> void {
        auto face = pyface.ptr.get();
        FT_CHECK(FT_Set_Char_Size,
                 face, pt_size * 64, 0, dpi * pyface.hinting_factor, dpi);
        auto transform =
          FT_Matrix{FT_Fixed(65536. / pyface.hinting_factor), 0, 0, 65536};
        FT_Set_Transform(face, &transform, nullptr);
      },
      "pt_size"_a, "dpi"_a)
    .def(
      "set_charmap",
      [](Face const& pyface, CharMap const& pycharmap) -> void {
        FT_CHECK(
          FT_Set_Charmap,
          pyface.ptr.get(),
          pycharmap.face.cast<Face>().ptr->charmaps[pycharmap.index])
      })
    .def(
      "_list_sfnt_tables",
      [](Face const& pyface) -> std::vector<std::string> {
        auto n_tables = FT_ULong{}, table_length = FT_ULong{};
        FT_CHECK(FT_Sfnt_Table_Info, pyface.ptr.get(), 0, nullptr, &n_tables);
        auto tags = std::vector<std::string>{};
        for (auto i = FT_ULong{}; i < n_tables; ++i) {
          auto tag = FT_ULong{};
          FT_CHECK(
            FT_Sfnt_Table_Info, pyface.ptr.get(), i, &tag, &table_length);
          tags.push_back(
            {char(tag >> 24), char(tag >> 16), char(tag >> 8), char(tag)});
        }
        return tags;
      });

  py::class_<CharMap>(m, "CharMap", R"__doc__(
A lightweight wrapper around a ``FT_CharMap``.
)__doc__")
    .def(
      "__repr__",
      [](CharMap const& pycharmap) -> std::string {
        auto charmap = pycharmap.face.cast<Face>().ptr->charmaps[pycharmap.index];
        return
          "<CharMap "s +
          "encoding="s + py::repr(py::cast(charmap->encoding)).cast<std::string>() + ", "s +
          "platform_id='"s + detail::tt_platforms.at(charmap->platform_id) + "', "s +
          "encoding_id="s + std::to_string(charmap->encoding_id) +
          ">"s;
      })
    .def_property_readonly(
      "face",
      [](CharMap const& pycharmap) -> py::object {
        return pycharmap.face;
      })
    .def_property_readonly(
      "encoding",
      [](CharMap const& pycharmap) -> FT_Encoding {
        return pycharmap.face.cast<Face>().ptr->charmaps[pycharmap.index]->encoding;
      })
    .def_property_readonly(
      "platform_id",
      [](CharMap const& pycharmap) -> std::string {
        return
          detail::tt_platforms.at(
            pycharmap.face.cast<Face>().ptr->charmaps[pycharmap.index]->platform_id);
      })
    .def_property_readonly(
      "encoding_id",
      [](CharMap const& pycharmap) -> FT_UShort {
        return pycharmap.face.cast<Face>().ptr->charmaps[pycharmap.index]->encoding_id;
      });

  py::class_<Glyph>(m, "Glyph", R"__doc__(
A lightweight wrapper around a ``FT_Glyph``.

This object cannot be constructed directly.  Instead, load a glyph in a face's
glyph slot with `Face.load_char` or `Face.load_glyph`, then access the face's
`glyph` property (which calls ``FT_Get_Glyph``).

This class exposes the attributes of the original glyph slot and its glyph
metrics.  Length attibutes are in pixels (this module handles conversion from
26.6 and 16.16 fixed point formats internally).
)__doc__")
    .def_property_readonly(
      "width",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.width / 64. / pyglyph.hinting_factor;
      })
    .def_property_readonly(
      "height",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.height / 64.;
      })
    .def_property_readonly(
      "horiBearingX",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.horiBearingX / 64. / pyglyph.hinting_factor;
      })
    .def_property_readonly(
      "horiBearingY",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.horiBearingY / 64.;
      })
    .def_property_readonly(
      "horiAdvance",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.horiAdvance / 64.;
      })
    .def_property_readonly(
      "vertBearingX",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.vertBearingX / 64.;
      })
    .def_property_readonly(
      "vertBearingY",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.vertBearingY / 64.;
      })
    .def_property_readonly(
      "vertAdvance",
      [](Glyph& pyglyph) -> double {
        return pyglyph.metrics.vertAdvance / 64.;
      })
    .def_property_readonly(
      "linearHoriAdvance",
      [](Glyph& pyglyph) -> double {
        return pyglyph.linearHoriAdvance / 65536. / pyglyph.hinting_factor;
      })
    .def_property_readonly(
      "linearVertAdvance",
      [](Glyph& pyglyph) -> double {
        return pyglyph.linearVertAdvance / 65536.;
      })
    .def(
      "get_cbox",
      [](Glyph& pyglyph, FT_UInt mode)
      -> std::tuple<double, double, double, double> {
        auto bbox = FT_BBox{};
        FT_Glyph_Get_CBox(pyglyph.ptr.get(), mode, &bbox);
        auto conv = ((mode == FT_GLYPH_BBOX_SUBPIXELS)
                     || mode == FT_GLYPH_BBOX_GRIDFIT) ? 1. / 64 : 1.;
        return {bbox.xMin * conv, bbox.xMax * conv,
                bbox.yMin * conv, bbox.yMax * conv};
      });

  py::class_<Layout>(m, "Layout", R"__doc__(
A text (and rectangles) layout engine.

Use as follows::

   # Construct a layout.
   layout = Layout.simple(...)
   # or
   layout = Layout.manual(...)
   # Access the layout's bounds:
   layout.xMin, layout.xMax, layout.yMin, layout.yMax
   # Render the text into a numpy array:
   result = layout.render()
)__doc__")
    .def("render", &Layout::render, R"__doc__(
Render the laid out text into a numpy array.
)__doc__")
    .def_property_readonly(
      "xMin",
      [](Layout& layout) -> double { return layout.bbox.xMin / 64.; })
    .def_property_readonly(
      "xMax",
      [](Layout& layout) -> double { return layout.bbox.xMax / 64.; })
    .def_property_readonly(
      "yMin",
      [](Layout& layout) -> double { return layout.bbox.yMin / 64.; })
    .def_property_readonly(
      "yMax",
      [](Layout& layout) -> double { return layout.bbox.yMax / 64.; })
    .def_static(
      "simple",
      [](std::u32string const& string, Face const& pyface, FT_Int32 flags)
      -> Layout {
        return Layout::simple(string, pyface.ptr.get(), flags);
      },
      "string"_a, "face"_a, "flags"_a, R"__doc__(
Layout a string by positioning individual glyphs one after the other.

After each glyph, the current position is advanced by the glyph's advance and
the kerning between this glyph and the next one.
)__doc__")
    .def_static(
      "manual",
      [](std::vector<std::tuple<Glyph, double, double>> const& positioned_pyglyphs,
         std::vector<rect_t> const& rectangles,
         FT_Int32 flags)
      -> Layout {
        auto positioned_glyphs
          = std::vector<std::tuple<FT_Glyph, double, double>>{};
        std::transform(
          positioned_pyglyphs.begin(), positioned_pyglyphs.end(),
          std::back_inserter(positioned_glyphs),
          [](std::tuple<Glyph, double, double> const& positioned_pyglyph)
          -> std::tuple<FT_Glyph, double, double> {
            auto& [pyglyph, x, y] = positioned_pyglyph;
            return {pyglyph.ptr.get(), x, y};
          });
        return Layout::manual(positioned_glyphs, rectangles, flags);
      },
      "positioned_glyphs"_a, "rectangles"_a, "flags"_a, R"__doc__(
Prepare a list of manually laid out glyphs and rectangles for rendering.
)__doc__");

  m.def(
    "glyph_to_path",
    [](Glyph const& glyph)
    -> std::tuple<std::vector<std::tuple<double, double>>, std::vector<int>> {
      if (glyph.ptr->format != FT_GLYPH_FORMAT_OUTLINE) {
        throw std::runtime_error(
          "Glyph format is "
          + py::cast(glyph.ptr->format).attr("name").cast<std::string>()
          + ", not OUTLINE");
      }
      // outline.n_points seems invalid :-(
      auto path = std::tuple<std::vector<std::tuple<double, double>>,
                             std::vector<int>>{};
      auto& [vertices, codes] = path;
      auto move_to =
        [](FT_Vector const* to, void* raw) -> int {
        auto& [vertices, codes] = *static_cast<decltype(&path)>(raw);
        if (vertices.size()) {
          vertices.push_back({NAN, NAN});
          codes.push_back(79);
        }
        vertices.push_back({to->x / 64., to->y / 64.});
        codes.push_back(1);
        return 0;
      };
      auto line_to =
        [](FT_Vector const* to, void* raw) -> int {
        auto& [vertices, codes] = *static_cast<decltype(&path)>(raw);
        vertices.push_back({to->x / 64., to->y / 64.});
        codes.push_back(2);
        return 0;
      };
      auto conic_to =
        [](FT_Vector const* control, FT_Vector const* to, void* raw) -> int {
        auto& [vertices, codes] = *static_cast<decltype(&path)>(raw);
        vertices.push_back({control->x / 64., control->y / 64.});
        vertices.push_back({to->x / 64., to->y / 64.});
        codes.push_back(3);
        codes.push_back(3);
        return 0;
      };
      auto cubic_to =
        [](FT_Vector const* control1, FT_Vector const* control2,
           FT_Vector const* to, void* raw) -> int {
        auto& [vertices, codes] = *static_cast<decltype(&path)>(raw);
        vertices.push_back({control1->x / 64., control1->y / 64.});
        vertices.push_back({control2->x / 64., control2->y / 64.});
        vertices.push_back({to->x / 64., to->y / 64.});
        codes.push_back(4);
        codes.push_back(4);
        codes.push_back(4);
        return 0;
      };
      auto outline_funcs =
        FT_Outline_Funcs{move_to, line_to, conic_to, cubic_to, 0, 0};
      FT_Outline_Decompose(
        &reinterpret_cast<FT_OutlineGlyph>(glyph.ptr.get())->outline,
        &outline_funcs,
        &path);
      if (vertices.size()) {
        vertices.push_back({NAN, NAN});
        codes.push_back(79);
      } else {
        vertices.push_back({0, 0});
        codes.push_back(1);
      }
      return path;
    },
    "glyph"_a, R"__doc__(
Extract a glyph's outline in Matplotlib's ``(vertices, codes)`` format.
)__doc__");
}

}
