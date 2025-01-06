# Constants are based off fontconfig 2.12.92.

from enum import IntEnum
import re
import warnings

import numpy as np

from . import _ft2


# Had to be fixed:
# BASQUE_SPAIN -> BASQUE_BASQUE
# CHINESE_MACAU -> CHINESE_MACAO
# CATALAN_SPAIN -> CATALAN_CATALAN
# SLOVENE_SLOVENIAN -> SLOVENIAN_SLOVENIA
# SPANISH_SPAIN_INTERNATIONAL_SORT -> SPANISH_SPAIN_MODERN_SORT
_language_codes = {
    ("MACINTOSH", 0xffff): "",
    ("MACINTOSH", "ENGLISH"): "en",
    ("MACINTOSH", "FRENCH"): "fr",
    ("MACINTOSH", "GERMAN"): "de",
    ("MACINTOSH", "ITALIAN"): "it",
    ("MACINTOSH", "DUTCH"): "nl",
    ("MACINTOSH", "SWEDISH"): "sv",
    ("MACINTOSH", "SPANISH"): "es",
    ("MACINTOSH", "DANISH"): "da",
    ("MACINTOSH", "PORTUGUESE"): "pt",
    ("MACINTOSH", "NORWEGIAN"): "no",
    ("MACINTOSH", "HEBREW"): "he",
    ("MACINTOSH", "JAPANESE"): "ja",
    ("MACINTOSH", "ARABIC"): "ar",
    ("MACINTOSH", "FINNISH"): "fi",
    ("MACINTOSH", "GREEK"): "el",
    ("MACINTOSH", "ICELANDIC"): "is",
    ("MACINTOSH", "MALTESE"): "mt",
    ("MACINTOSH", "TURKISH"): "tr",
    ("MACINTOSH", "CROATIAN"): "hr",
    ("MACINTOSH", "CHINESE_TRADITIONAL"): "zh-tw",
    ("MACINTOSH", "URDU"): "ur",
    ("MACINTOSH", "HINDI"): "hi",
    ("MACINTOSH", "THAI"): "th",
    ("MACINTOSH", "KOREAN"): "ko",
    ("MACINTOSH", "LITHUANIAN"): "lt",
    ("MACINTOSH", "POLISH"): "pl",
    ("MACINTOSH", "HUNGARIAN"): "hu",
    ("MACINTOSH", "ESTONIAN"): "et",
    ("MACINTOSH", "LETTISH"): "lv",
    ("MACINTOSH", "FAEROESE"): "fo",
    ("MACINTOSH", "FARSI"): "fa",
    ("MACINTOSH", "RUSSIAN"): "ru",
    ("MACINTOSH", "CHINESE_SIMPLIFIED"): "zh-cn",
    ("MACINTOSH", "FLEMISH"): "nl",
    ("MACINTOSH", "IRISH"): "ga",
    ("MACINTOSH", "ALBANIAN"): "sq",
    ("MACINTOSH", "ROMANIAN"): "ro",
    ("MACINTOSH", "CZECH"): "cs",
    ("MACINTOSH", "SLOVAK"): "sk",
    ("MACINTOSH", "SLOVENIAN"): "sl",
    ("MACINTOSH", "YIDDISH"): "yi",
    ("MACINTOSH", "SERBIAN"): "sr",
    ("MACINTOSH", "MACEDONIAN"): "mk",
    ("MACINTOSH", "BULGARIAN"): "bg",
    ("MACINTOSH", "UKRAINIAN"): "uk",
    ("MACINTOSH", "BYELORUSSIAN"): "be",
    ("MACINTOSH", "UZBEK"): "uz",
    ("MACINTOSH", "KAZAKH"): "kk",
    ("MACINTOSH", "AZERBAIJANI"): "az",
    ("MACINTOSH", "AZERBAIJANI_CYRILLIC_SCRIPT"): "az",
    ("MACINTOSH", "AZERBAIJANI_ARABIC_SCRIPT"): "ar",
    ("MACINTOSH", "ARMENIAN"): "hy",
    ("MACINTOSH", "GEORGIAN"): "ka",
    ("MACINTOSH", "MOLDAVIAN"): "mo",
    ("MACINTOSH", "KIRGHIZ"): "ky",
    ("MACINTOSH", "TAJIKI"): "tg",
    ("MACINTOSH", "TURKMEN"): "tk",
    ("MACINTOSH", "MONGOLIAN"): "mo",
    ("MACINTOSH", "MONGOLIAN_MONGOLIAN_SCRIPT"): "mo",
    ("MACINTOSH", "MONGOLIAN_CYRILLIC_SCRIPT"): "mo",
    ("MACINTOSH", "PASHTO"): "ps",
    ("MACINTOSH", "KURDISH"): "ku",
    ("MACINTOSH", "KASHMIRI"): "ks",
    ("MACINTOSH", "SINDHI"): "sd",
    ("MACINTOSH", "TIBETAN"): "bo",
    ("MACINTOSH", "NEPALI"): "ne",
    ("MACINTOSH", "SANSKRIT"): "sa",
    ("MACINTOSH", "MARATHI"): "mr",
    ("MACINTOSH", "BENGALI"): "bn",
    ("MACINTOSH", "ASSAMESE"): "as",
    ("MACINTOSH", "GUJARATI"): "gu",
    ("MACINTOSH", "PUNJABI"): "pa",
    ("MACINTOSH", "ORIYA"): "or",
    ("MACINTOSH", "MALAYALAM"): "ml",
    ("MACINTOSH", "KANNADA"): "kn",
    ("MACINTOSH", "TAMIL"): "ta",
    ("MACINTOSH", "TELUGU"): "te",
    ("MACINTOSH", "SINHALESE"): "si",
    ("MACINTOSH", "BURMESE"): "my",
    ("MACINTOSH", "KHMER"): "km",
    ("MACINTOSH", "LAO"): "lo",
    ("MACINTOSH", "VIETNAMESE"): "vi",
    ("MACINTOSH", "INDONESIAN"): "id",
    ("MACINTOSH", "TAGALOG"): "tl",
    ("MACINTOSH", "MALAY_ROMAN_SCRIPT"): "ms",
    ("MACINTOSH", "MALAY_ARABIC_SCRIPT"): "ms",
    ("MACINTOSH", "AMHARIC"): "am",
    ("MACINTOSH", "TIGRINYA"): "ti",
    ("MACINTOSH", "GALLA"): "om",
    ("MACINTOSH", "SOMALI"): "so",
    ("MACINTOSH", "SWAHILI"): "sw",
    ("MACINTOSH", "RUANDA"): "rw",
    ("MACINTOSH", "RUNDI"): "rn",
    ("MACINTOSH", "CHEWA"): "ny",
    ("MACINTOSH", "MALAGASY"): "mg",
    ("MACINTOSH", "ESPERANTO"): "eo",
    ("MACINTOSH", "WELSH"): "cy",
    ("MACINTOSH", "BASQUE"): "eu",
    ("MACINTOSH", "CATALAN"): "ca",
    ("MACINTOSH", "LATIN"): "la",
    ("MACINTOSH", "QUECHUA"): "qu",
    ("MACINTOSH", "GUARANI"): "gn",
    ("MACINTOSH", "AYMARA"): "ay",
    ("MACINTOSH", "TATAR"): "tt",
    ("MACINTOSH", "UIGHUR"): "ug",
    ("MACINTOSH", "DZONGKHA"): "dz",
    ("MACINTOSH", "JAVANESE"): "jw",
    ("MACINTOSH", "SUNDANESE"): "su",
    ("MACINTOSH", "GALICIAN"): "gl",
    ("MACINTOSH", "AFRIKAANS"): "af",
    ("MACINTOSH", "BRETON"): "br",
    ("MACINTOSH", "INUKTITUT"): "iu",
    ("MACINTOSH", "SCOTTISH_GAELIC"): "gd",
    ("MACINTOSH", "MANX_GAELIC"): "gv",
    ("MACINTOSH", "IRISH_GAELIC"): "ga",
    ("MACINTOSH", "TONGAN"): "to",
    ("MACINTOSH", "GREEK_POLYTONIC"): "el",
    ("MACINTOSH", "GREELANDIC"): "ik",
    ("MACINTOSH", "AZERBAIJANI_ROMAN_SCRIPT"): "az",
    ("MICROSOFT", "ARABIC_SAUDI_ARABIA"): "ar",
    ("MICROSOFT", "ARABIC_IRAQ"): "ar",
    ("MICROSOFT", "ARABIC_EGYPT"): "ar",
    ("MICROSOFT", "ARABIC_LIBYA"): "ar",
    ("MICROSOFT", "ARABIC_ALGERIA"): "ar",
    ("MICROSOFT", "ARABIC_MOROCCO"): "ar",
    ("MICROSOFT", "ARABIC_TUNISIA"): "ar",
    ("MICROSOFT", "ARABIC_OMAN"): "ar",
    ("MICROSOFT", "ARABIC_YEMEN"): "ar",
    ("MICROSOFT", "ARABIC_SYRIA"): "ar",
    ("MICROSOFT", "ARABIC_JORDAN"): "ar",
    ("MICROSOFT", "ARABIC_LEBANON"): "ar",
    ("MICROSOFT", "ARABIC_KUWAIT"): "ar",
    ("MICROSOFT", "ARABIC_UAE"): "ar",
    ("MICROSOFT", "ARABIC_BAHRAIN"): "ar",
    ("MICROSOFT", "ARABIC_QATAR"): "ar",
    ("MICROSOFT", "BULGARIAN_BULGARIA"): "bg",
    ("MICROSOFT", "CATALAN_CATALAN"): "ca",
    ("MICROSOFT", "CHINESE_TAIWAN"): "zh-tw",
    ("MICROSOFT", "CHINESE_PRC"): "zh-cn",
    ("MICROSOFT", "CHINESE_HONG_KONG"): "zh-hk",
    ("MICROSOFT", "CHINESE_SINGAPORE"): "zh-sg",
    ("MICROSOFT", "CHINESE_MACAO"): "zh-mo",
    ("MICROSOFT", "CZECH_CZECH_REPUBLIC"): "cs",
    ("MICROSOFT", "DANISH_DENMARK"): "da",
    ("MICROSOFT", "GERMAN_GERMANY"): "de",
    ("MICROSOFT", "GERMAN_SWITZERLAND"): "de",
    ("MICROSOFT", "GERMAN_AUSTRIA"): "de",
    ("MICROSOFT", "GERMAN_LUXEMBOURG"): "de",
    ("MICROSOFT", "GERMAN_LIECHTENSTEI"): "de",
    ("MICROSOFT", "GREEK_GREECE"): "el",
    ("MICROSOFT", "ENGLISH_UNITED_STATES"): "en",
    ("MICROSOFT", "ENGLISH_UNITED_KINGDOM"): "en",
    ("MICROSOFT", "ENGLISH_AUSTRALIA"): "en",
    ("MICROSOFT", "ENGLISH_CANADA"): "en",
    ("MICROSOFT", "ENGLISH_NEW_ZEALAND"): "en",
    ("MICROSOFT", "ENGLISH_IRELAND"): "en",
    ("MICROSOFT", "ENGLISH_SOUTH_AFRICA"): "en",
    ("MICROSOFT", "ENGLISH_JAMAICA"): "en",
    ("MICROSOFT", "ENGLISH_CARIBBEAN"): "en",
    ("MICROSOFT", "ENGLISH_BELIZE"): "en",
    ("MICROSOFT", "ENGLISH_TRINIDAD"): "en",
    ("MICROSOFT", "ENGLISH_ZIMBABWE"): "en",
    ("MICROSOFT", "ENGLISH_PHILIPPINES"): "en",
    ("MICROSOFT", "SPANISH_SPAIN_TRADITIONAL_SORT"): "es",
    ("MICROSOFT", "SPANISH_MEXICO"): "es",
    ("MICROSOFT", "SPANISH_SPAIN_MODERN_SORT"): "es",
    ("MICROSOFT", "SPANISH_GUATEMALA"): "es",
    ("MICROSOFT", "SPANISH_COSTA_RICA"): "es",
    ("MICROSOFT", "SPANISH_PANAMA"): "es",
    ("MICROSOFT", "SPANISH_DOMINICAN_REPUBLIC"): "es",
    ("MICROSOFT", "SPANISH_VENEZUELA"): "es",
    ("MICROSOFT", "SPANISH_COLOMBIA"): "es",
    ("MICROSOFT", "SPANISH_PERU"): "es",
    ("MICROSOFT", "SPANISH_ARGENTINA"): "es",
    ("MICROSOFT", "SPANISH_ECUADOR"): "es",
    ("MICROSOFT", "SPANISH_CHILE"): "es",
    ("MICROSOFT", "SPANISH_URUGUAY"): "es",
    ("MICROSOFT", "SPANISH_PARAGUAY"): "es",
    ("MICROSOFT", "SPANISH_BOLIVIA"): "es",
    ("MICROSOFT", "SPANISH_EL_SALVADOR"): "es",
    ("MICROSOFT", "SPANISH_HONDURAS"): "es",
    ("MICROSOFT", "SPANISH_NICARAGUA"): "es",
    ("MICROSOFT", "SPANISH_PUERTO_RICO"): "es",
    ("MICROSOFT", "FINNISH_FINLAND"): "fi",
    ("MICROSOFT", "FRENCH_FRANCE"): "fr",
    ("MICROSOFT", "FRENCH_BELGIUM"): "fr",
    ("MICROSOFT", "FRENCH_CANADA"): "fr",
    ("MICROSOFT", "FRENCH_SWITZERLAND"): "fr",
    ("MICROSOFT", "FRENCH_LUXEMBOURG"): "fr",
    ("MICROSOFT", "FRENCH_MONACO"): "fr",
    ("MICROSOFT", "HEBREW_ISRAEL"): "he",
    ("MICROSOFT", "HUNGARIAN_HUNGARY"): "hu",
    ("MICROSOFT", "ICELANDIC_ICELAND"): "is",
    ("MICROSOFT", "ITALIAN_ITALY"): "it",
    ("MICROSOFT", "ITALIAN_SWITZERLAND"): "it",
    ("MICROSOFT", "JAPANESE_JAPAN"): "ja",
    ("MICROSOFT", "KOREAN_EXTENDED_WANSUNG_KOREA"): "ko",
    ("MICROSOFT", "KOREAN_JOHAB_KOREA"): "ko",
    ("MICROSOFT", "DUTCH_NETHERLANDS"): "nl",
    ("MICROSOFT", "DUTCH_BELGIUM"): "nl",
    ("MICROSOFT", "NORWEGIAN_NORWAY_BOKMAL"): "no",
    ("MICROSOFT", "NORWEGIAN_NORWAY_NYNORSK"): "nn",
    ("MICROSOFT", "POLISH_POLAND"): "pl",
    ("MICROSOFT", "PORTUGUESE_BRAZIL"): "pt",
    ("MICROSOFT", "PORTUGUESE_PORTUGAL"): "pt",
    ("MICROSOFT", "RHAETO_ROMANIC_SWITZERLAND"): "rm",
    ("MICROSOFT", "ROMANIAN_ROMANIA"): "ro",
    ("MICROSOFT", "MOLDAVIAN_MOLDAVIA"): "mo",
    ("MICROSOFT", "RUSSIAN_RUSSIA"): "ru",
    ("MICROSOFT", "RUSSIAN_MOLDAVIA"): "ru",
    ("MICROSOFT", "CROATIAN_CROATIA"): "hr",
    ("MICROSOFT", "SERBIAN_SERBIA_LATIN"): "sr",
    ("MICROSOFT", "SERBIAN_SERBIA_CYRILLIC"): "sr",
    ("MICROSOFT", "SLOVAK_SLOVAKIA"): "sk",
    ("MICROSOFT", "ALBANIAN_ALBANIA"): "sq",
    ("MICROSOFT", "SWEDISH_SWEDEN"): "sv",
    ("MICROSOFT", "SWEDISH_FINLAND"): "sv",
    ("MICROSOFT", "THAI_THAILAND"): "th",
    ("MICROSOFT", "TURKISH_TURKEY"): "tr",
    ("MICROSOFT", "URDU_PAKISTAN"): "ur",
    ("MICROSOFT", "INDONESIAN_INDONESIA"): "id",
    ("MICROSOFT", "UKRAINIAN_UKRAINE"): "uk",
    ("MICROSOFT", "BELARUSIAN_BELARUS"): "be",
    ("MICROSOFT", "SLOVENIAN_SLOVENIA"): "sl",
    ("MICROSOFT", "ESTONIAN_ESTONIA"): "et",
    ("MICROSOFT", "LATVIAN_LATVIA"): "lv",
    ("MICROSOFT", "LITHUANIAN_LITHUANIA"): "lt",
    ("MICROSOFT", "CLASSIC_LITHUANIAN_LITHUANIA"): "lt",
    ("MICROSOFT", "MAORI_NEW_ZEALAND"): "mi",
    ("MICROSOFT", "FARSI_IRAN"): "fa",
    ("MICROSOFT", "VIETNAMESE_VIET_NAM"): "vi",
    ("MICROSOFT", "ARMENIAN_ARMENIA"): "hy",
    ("MICROSOFT", "AZERI_AZERBAIJAN_LATIN"): "az",
    ("MICROSOFT", "AZERI_AZERBAIJAN_CYRILLIC"): "az",
    ("MICROSOFT", "BASQUE_BASQUE"): "eu",
    ("MICROSOFT", "SORBIAN_GERMANY"): "wen",
    ("MICROSOFT", "MACEDONIAN_MACEDONIA"): "mk",
    ("MICROSOFT", "SUTU_SOUTH_AFRICA"): "st",
    ("MICROSOFT", "TSONGA_SOUTH_AFRICA"): "ts",
    ("MICROSOFT", "TSWANA_SOUTH_AFRICA"): "tn",
    ("MICROSOFT", "VENDA_SOUTH_AFRICA"): "ven",
    ("MICROSOFT", "XHOSA_SOUTH_AFRICA"): "xh",
    ("MICROSOFT", "ZULU_SOUTH_AFRICA"): "zu",
    ("MICROSOFT", "AFRIKAANS_SOUTH_AFRICA"): "af",
    ("MICROSOFT", "GEORGIAN_GEORGIA"): "ka",
    ("MICROSOFT", "FAEROESE_FAEROE_ISLANDS"): "fo",
    ("MICROSOFT", "HINDI_INDIA"): "hi",
    ("MICROSOFT", "MALTESE_MALTA"): "mt",
    ("MICROSOFT", "SAAMI_LAPONIA"): "se",
    ("MICROSOFT", "SCOTTISH_GAELIC_UNITED_KINGDOM"): "gd",
    ("MICROSOFT", "IRISH_GAELIC_IRELAND"): "ga",
    ("MICROSOFT", "MALAY_MALAYSIA"): "ms",
    ("MICROSOFT", "MALAY_BRUNEI_DARUSSALAM"): "ms",
    ("MICROSOFT", "KAZAK_KAZAKSTAN"): "kk",
    ("MICROSOFT", "SWAHILI_KENYA"): "sw",
    ("MICROSOFT", "UZBEK_UZBEKISTAN_LATIN"): "uz",
    ("MICROSOFT", "UZBEK_UZBEKISTAN_CYRILLIC"): "uz",
    ("MICROSOFT", "TATAR_TATARSTAN"): "tt",
    ("MICROSOFT", "BENGALI_INDIA"): "bn",
    ("MICROSOFT", "PUNJABI_INDIA"): "pa",
    ("MICROSOFT", "GUJARATI_INDIA"): "gu",
    ("MICROSOFT", "ORIYA_INDIA"): "or",
    ("MICROSOFT", "TAMIL_INDIA"): "ta",
    ("MICROSOFT", "TELUGU_INDIA"): "te",
    ("MICROSOFT", "KANNADA_INDIA"): "kn",
    ("MICROSOFT", "MALAYALAM_INDIA"): "ml",
    ("MICROSOFT", "ASSAMESE_INDIA"): "as",
    ("MICROSOFT", "MARATHI_INDIA"): "mr",
    ("MICROSOFT", "SANSKRIT_INDIA"): "sa",
    ("MICROSOFT", "KONKANI_INDIA"): "kok",
    ("MICROSOFT", "ARABIC_GENERAL"): "ar",
    ("MICROSOFT", "CHINESE_GENERAL"): "zh",
    ("MICROSOFT", "ENGLISH_GENERAL"): "en",
    ("MICROSOFT", "FRENCH_WEST_INDIES"): "fr",
    ("MICROSOFT", "FRENCH_REUNION"): "fr",
    ("MICROSOFT", "FRENCH_CONGO"): "fr",
    ("MICROSOFT", "FRENCH_SENEGAL"): "fr",
    ("MICROSOFT", "FRENCH_CAMEROON"): "fr",
    ("MICROSOFT", "FRENCH_COTE_D_IVOIRE"): "fr",
    ("MICROSOFT", "FRENCH_MALI"): "fr",
    ("MICROSOFT", "BOSNIAN_BOSNIA_HERZEGOVINA"): "bs",
    ("MICROSOFT", "URDU_INDIA"): "ur",
    ("MICROSOFT", "TAJIK_TAJIKISTAN"): "tg",
    ("MICROSOFT", "YIDDISH_GERMANY"): "yi",
    ("MICROSOFT", "KIRGHIZ_KIRGHIZSTAN"): "ky",
    ("MICROSOFT", "TURKMEN_TURKMENISTAN"): "tk",
    ("MICROSOFT", "MONGOLIAN_MONGOLIA"): "mn",
    ("MICROSOFT", "TIBETAN_BHUTAN"): "bo",
    ("MICROSOFT", "TIBETAN_CHINA"): "bo",
    ("MICROSOFT", "DZONGHKA_BHUTAN"): "dz",
    ("MICROSOFT", "WELSH_WALES"): "cy",
    ("MICROSOFT", "KHMER_CAMBODIA"): "km",
    ("MICROSOFT", "LAO_LAOS"): "lo",
    ("MICROSOFT", "BURMESE_MYANMAR"): "my",
    ("MICROSOFT", "GALICIAN_SPAIN"): "gl",
    ("MICROSOFT", "MANIPURI_INDIA"): "mni",
    ("MICROSOFT", "SINDHI_INDIA"): "sd",
    ("MICROSOFT", "KASHMIRI_PAKISTAN"): "ks",
    ("MICROSOFT", "KASHMIRI_INDIA"): "ks",
    ("MICROSOFT", "NEPALI_NEPAL"): "ne",
    ("MICROSOFT", "NEPALI_INDIA"): "ne",
    ("MICROSOFT", "FRISIAN_NETHERLANDS"): "fy",
    ("MICROSOFT", "ENGLISH_HONG_KONG"): "en",
    ("MICROSOFT", "ENGLISH_INDIA"): "en",
    ("MICROSOFT", "ENGLISH_MALAYSIA"): "en",
    ("MICROSOFT", "ENGLISH_SINGAPORE"): "en",
    ("MICROSOFT", "SYRIAC_SYRIA"): "syr",
    ("MICROSOFT", "SINHALESE_SRI_LANKA"): "si",
    ("MICROSOFT", "CHEROKEE_UNITED_STATES"): "chr",
    ("MICROSOFT", "INUKTITUT_CANADA"): "iu",
    ("MICROSOFT", "AMHARIC_ETHIOPIA"): "am",
    ("MICROSOFT", "PASHTO_AFGHANISTAN"): "ps",
    ("MICROSOFT", "FILIPINO_PHILIPPINES"): "phi",
    ("MICROSOFT", "DHIVEHI_MALDIVES"): "div",
    ("MICROSOFT", "OROMO_ETHIOPIA"): "om",
    ("MICROSOFT", "TIGRIGNA_ETHIOPIA"): "ti",
    ("MICROSOFT", "TIGRIGNA_ERYTHREA"): "ti",
    ("MICROSOFT", "SPANISH_UNITED_STATES"): "es",
    ("MICROSOFT", "SPANISH_LATIN_AMERICA"): "es",
    ("MICROSOFT", "FRENCH_NORTH_AFRICA"): "fr",
    ("MICROSOFT", "FRENCH_MOROCCO"): "fr",
    ("MICROSOFT", "FRENCH_HAITI"): "fr",
    ("MICROSOFT", "BENGALI_BANGLADESH"): "bn",
    ("MICROSOFT", "PUNJABI_ARABIC_PAKISTAN"): "ar",
    ("MICROSOFT", "MONGOLIAN_MONGOLIA_MONGOLIAN"): "mn",
    ("MICROSOFT", "HAUSA_NIGERIA"): "ha",
    ("MICROSOFT", "YORUBA_NIGERIA"): "yo",
    ("MICROSOFT", "IGBO_NIGERIA"): "ibo",
    ("MICROSOFT", "KANURI_NIGERIA"): "kau",
    ("MICROSOFT", "GUARANI_PARAGUAY"): "gn",
    ("MICROSOFT", "HAWAIIAN_UNITED_STATES"): "haw",
    ("MICROSOFT", "LATIN"): "la",
    ("MICROSOFT", "SOMALI_SOMALIA"): "so",
    ("MICROSOFT", "PAPIAMENTU_NETHERLANDS_ANTILLES"): "pap",
}
_notice_foundries = [
    ("Adobe", "adobe"),
    ("Bigelow", "b&h"),
    ("Bitstream", "bitstream"),
    ("Gnat", "culmus"),
    ("Iorsh", "culmus"),
    ("HanYang System", "hanyang"),
    ("Font21", "hwan"),
    ("IBM", "ibm"),
    ("International Typeface Corporation", "itc"),
    ("Linotype", "linotype"),
    ("LINOTYPE-HELL", "linotype"),
    ("Microsoft", "microsoft"),
    ("Monotype", "monotype"),
    ("Omega", "omega"),
    ("Tiro Typeworks", "tiro"),
    ("URW", "urw"),
    ("XFree86", "xfree86"),
    ("Xorg", "xorg"),
]


class Slant(IntEnum):
    Roman = 0
    Italic = 100
    Oblique = 110


class Weight(IntEnum):
    Thin = 0
    Extralight = Ultralight = 40
    Light = 50
    Demilight = Semilight = 55
    Book = 75
    Regular = Normal = 80
    Medium = 100
    Demibold = Semibold = 180
    Bold = 200
    Extrabold = Ultrabold = 205
    Black = Heavy = 210
    Extrablack = Ultrablack = 215

    @classmethod
    def from_opentype(cls, ot_weight):
        fc_weights = [0, 40, 50, 55, 75, 80, 100, 180, 200, 205, 210, 215]
        ot_weights = [
            100, 200, 300, 350, 380, 400, 500, 600, 700, 800, 900, 1000]
        weight = int(np.interp(ot_weight, ot_weights, fc_weights) + .5)
        try:
            return Weight(weight)
        except ValueError:
            return weight


class Width(IntEnum):
    Ultracondensed = 50
    Extracondensed = 63
    Condensed = 75
    Semicondensed = 87
    Normal = 100
    Semiexpanded = 113
    Expanded = 125
    Extraexpanded = 150
    Ultraexpanded = 200


class Decorative(IntEnum):
    pass


Weight.consts = [
    ("thin", Weight.Thin),
    ("extralight", Weight.Extralight),
    ("ultralight", Weight.Ultralight),
    ("demilight", Weight.Demilight),
    ("semilight", Weight.Semilight),
    ("light", Weight.Light),
    ("book", Weight.Book),
    ("regular", Weight.Regular),
    ("normal", Weight.Normal),
    ("medium", Weight.Medium),
    ("demibold", Weight.Demibold),
    ("demi", Weight.Demibold),
    ("semibold", Weight.Semibold),
    ("extrabold", Weight.Extrabold),
    ("superbold", Weight.Extrabold),
    ("ultrabold", Weight.Ultrabold),
    ("bold", Weight.Bold),
    ("ultrablack", Weight.Ultrablack),
    ("superblack", Weight.Extrablack),
    ("extrablack", Weight.Extrablack),
    (r"\bultra", Weight.Ultrabold),
    ("black", Weight.Black),
    ("heavy", Weight.Heavy),
]
Width.consts = [
    ("ultracondensed", Width.Ultracondensed),
    ("extracondensed", Width.Extracondensed),
    ("semicondensed", Width.Semicondensed),
    ("condensed", Width.Condensed),
    ("normal", Width.Normal),
    ("semiexpanded", Width.Semiexpanded),
    ("extraexpanded", Width.Extraexpanded),
    ("ultraexpanded", Width.Ultraexpanded),
    ("expanded", Width.Expanded),
    ("extended", Width.Expanded),
]
Slant.consts = [
    ("italic", Slant.Italic),
    ("kursiv", Slant.Italic),
    ("oblique", Slant.Oblique),
]
Decorative.consts = [
    ("shadow", True),
    ("caps", True),
    ("antiqua", True),
    ("romansc", True),
    ("embosed", True),
    ("dunhill", True),
]


_platform_order = [
    "MICROSOFT",
    "APPLE_UNICODE",
    "MACINTOSH",
    "ISO",
]
_name_order = [
    # fc uses PREFERRED_{,SUB}FAMILY which is a deprecated synonym of
    # TYPOGRAPHIC_{,SUB}FAMILY.
    "WWS_FAMILY",
    "TYPOGRAPHIC_FAMILY",
    "FONT_FAMILY",
    "MAC_FULL_NAME",
    "FULL_NAME",
    "WWS_SUBFAMILY",
    "TYPOGRAPHIC_SUBFAMILY",
    "FONT_SUBFAMILY",
    "TRADEMARK",
    "MANUFACTURER",
]


def query_face(face):
    pattern = {}
    pattern["outline"] = bool(face.face_flags & _ft2.FaceFlag.SCALABLE)
    pattern["color"] = bool(face.face_flags & _ft2.FaceFlag.COLOR)
    pattern["scalable"] = pattern["outline"] or pattern["color"]
    variable = False  # TODO: Multiple masters not supported.
    pattern["family"] = []
    pattern["fullname"] = []
    pattern["style"] = []
    try:
        os2_t = face.get_sfnt_table("OS/2")
        head_t = face.get_sfnt_table("head")
        raw_name_table = face.get_sfnt_name_table()
    except RuntimeError:  # Not an SFNT font.
        os2_t = head_t = raw_name_table = None
    else:
        if (os2_t and os2_t["version"] >= 0x0001 and os2_t["version"] != 0xffff
                and os2_t["achVendID"]):
            pattern["foundry"] = os2_t["achVendID"]
        name_table = {}
        for (platform, encoding, language, name), value \
                in raw_name_table.items():
            if isinstance(value, bytes):
                warnings.warn(
                    "Skipping undecoded value {} {} {} {}: {}"
                    .format(platform, encoding, language, name, value))
                continue  # Don't try to guess Shift-JIS, unlike fc.
            name_table.setdefault((platform, name), {})[
                # APPLE_UNICODE specifies no language.
                encoding, _language_codes.get((platform, language), "")] = \
                value
        name_to_entry = {
            "WWS_FAMILY": "family",
            "TYPOGRAPHIC_FAMILY": "family",
            "FONT_FAMILY": "family",
            "MAC_FULL_NAME": "fullname",
            "FULL_NAME": "fullname",
            "WWS_SUBFAMILY": "style",
            "TYPOGRAPHIC_SUBFAMILY": "style",
            "FONT_SUBFAMILY": "style",
        }
        for platform in _platform_order:
            for name in _name_order:
                # TODO: Instances skipped.
                values = name_table.get((platform, name))
                if values is None:
                    continue
                if name in name_to_entry:
                    # fc drops duplicate values even if the language is
                    # different, which seems wrong.
                    for (_, language), value in values.items():
                        pattern[name_to_entry[name]].append((language, value))
                elif name in ["TRADEMARK", "MANUFACTURER"]:
                    for _, value in values.items():
                        pattern.setdefault("foundry", value)
        # Deduplicate family/fullname/style.
        for entry in name_to_entry.values():
            pattern[entry] = list(dict.fromkeys(pattern[entry]))  # Py3.6+.
    # family_name can *actually* be None...
    if not pattern["family"] and face.family_name and face.family_name.strip():
        # fc stores the lang in STYLELANG, seems like a bug?
        pattern["family"] = [("en", face.family_name.strip())]
    # TODO: Variables check skipped.
    if not pattern["style"] and face.style_name.strip():
        pattern["style"] = [("en", face.style_name.strip())]
    if not pattern["family"]:
        pattern["family"] = [("", face.path.rsplit("/", 1)[-1].rsplit(".")[0])]
    try:
        pattern["postscriptname"] = (
            face.get_postscript_name()
            or next(family for language, family in pattern["family"]
                    if language == "en")[:255]
               .translate({ord(c): "-" for c in "\x04()/<>[]{}\t\f\r\n "}))
    except StopIteration:
        pass
    pattern["file"] = face.path
    pattern["index"] = face.face_index
    pattern["fontversion"] = head_t["Font_Revision"] if head_t else 0
    # TODO: Check for multiple "exclusive" languages.
    if os2_t and os2_t["version"] != 0xffff:
        pattern["weight"] = Weight.from_opentype(os2_t["usWeightClass"])
        try:
            # TODO: Multiply by MM width multiplier (after conversion).
            pattern["width"] = {
                1: Width.Ultracondensed,
                2: Width.Extracondensed,
                3: Width.Condensed,
                4: Width.Semicondensed,
                5: Width.Normal,
                6: Width.Semiexpanded,
                7: Width.Expanded,
                8: Width.Extraexpanded,
                9: Width.Ultraexpanded,
            }[round(os2_t["usWidthClass"])]
        except KeyError:
            pass
    # TODO: Font capabilities.
    # TODO: Optical sizes.
    try:
        ps_font_info = face.get_ps_font_info()
    except RuntimeError:
        pass
    else:
        try:
            pattern.setdefault(
                "weight",
                next(weight for regex, weight in Weight.consts
                     if re.fullmatch(
                         regex, ps_font_info["weight"] or "", re.I)))
        except StopIteration:
            pass
        try:
            pattern.setdefault(
                "foundry",
                next(foundry for notice, foundry in _notice_foundries
                     if notice in (ps_font_info["notice"] or "")))
        except StopIteration:
            pass
    # TODO: BDF properties.
    for _, style in pattern["style"]:
        for prop, enum in [("weight", Weight), ("width", Width),
                           ("slant", Slant), ("decorative", Decorative)]:
            try:
                pattern.setdefault(
                    prop, next(value for regex, value in enum.consts
                               if re.search(regex, style, re.I)))
            except StopIteration:
                pass
    pattern.setdefault(
        "slant",
        Slant.Italic if face.style_flags & _ft2.StyleFlag.ITALIC
        else Slant.Roman)
    pattern.setdefault(
        "weight",
        Weight.Medium if face.style_flags & _ft2.StyleFlag.BOLD
        else Weight.Bold)
    pattern.setdefault("width", Width.Normal)
    pattern.setdefault("foundry", "unknown")
    # TODO: Unicode coverage.
    # TODO: Spacing.
    if not face.face_flags & _ft2.FaceFlag.SCALABLE:
        pattern["antialias"] = False
        # TODO: BDF properties.
        pattern["pixel_size"] = [size["y_ppem"]
                                 for size in face.available_sizes]
    pattern["fontformat"] = face.get_font_format()
    return pattern
