""" Python Character Mapping Codec hebrew generated from 'codecs/HEBREW.TXT' with gencodec.py.

"""#"
# Manually changed in HEBREW.TXT:
#   0x81 0x05F2+0x05B7 HEBREW LIGATURE YOD YOD PATAH
#        -> 0xFB1F  HEBREW LIGATURE YOD YOD PATAH
#   0xC0 0xF86A+0x05DC+0x05B9 Hebrew ligature lamed holam
#        -> removed
#   0xDE 0x05B8+0xF87F HEBREW POINT QAMATS, alternate form "qamats qatan"
#        -> 0x05C7 HEBREW POINT QAMATS QATAN

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, errors, encoding_table)

    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, decoding_table)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_table)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, decoding_table)[0]

class StreamWriter(Codec, codecs.StreamWriter):
    pass

class StreamReader(Codec, codecs.StreamReader):
    pass

### encodings module API

def getregentry():
    return codecs.CodecInfo(
        name='hebrew',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


### Decoding Table

decoding_table = (
    '\x00'      #  0x00 -> CONTROL CHARACTER
    '\x01'      #  0x01 -> CONTROL CHARACTER
    '\x02'      #  0x02 -> CONTROL CHARACTER
    '\x03'      #  0x03 -> CONTROL CHARACTER
    '\x04'      #  0x04 -> CONTROL CHARACTER
    '\x05'      #  0x05 -> CONTROL CHARACTER
    '\x06'      #  0x06 -> CONTROL CHARACTER
    '\x07'      #  0x07 -> CONTROL CHARACTER
    '\x08'      #  0x08 -> CONTROL CHARACTER
    '\t'        #  0x09 -> CONTROL CHARACTER
    '\n'        #  0x0A -> CONTROL CHARACTER
    '\x0b'      #  0x0B -> CONTROL CHARACTER
    '\x0c'      #  0x0C -> CONTROL CHARACTER
    '\r'        #  0x0D -> CONTROL CHARACTER
    '\x0e'      #  0x0E -> CONTROL CHARACTER
    '\x0f'      #  0x0F -> CONTROL CHARACTER
    '\x10'      #  0x10 -> CONTROL CHARACTER
    '\x11'      #  0x11 -> CONTROL CHARACTER
    '\x12'      #  0x12 -> CONTROL CHARACTER
    '\x13'      #  0x13 -> CONTROL CHARACTER
    '\x14'      #  0x14 -> CONTROL CHARACTER
    '\x15'      #  0x15 -> CONTROL CHARACTER
    '\x16'      #  0x16 -> CONTROL CHARACTER
    '\x17'      #  0x17 -> CONTROL CHARACTER
    '\x18'      #  0x18 -> CONTROL CHARACTER
    '\x19'      #  0x19 -> CONTROL CHARACTER
    '\x1a'      #  0x1A -> CONTROL CHARACTER
    '\x1b'      #  0x1B -> CONTROL CHARACTER
    '\x1c'      #  0x1C -> CONTROL CHARACTER
    '\x1d'      #  0x1D -> CONTROL CHARACTER
    '\x1e'      #  0x1E -> CONTROL CHARACTER
    '\x1f'      #  0x1F -> CONTROL CHARACTER
    ' '         #  0x20 -> SPACE, left-right
    '!'         #  0x21 -> EXCLAMATION MARK, left-right
    '"'         #  0x22 -> QUOTATION MARK, left-right
    '#'         #  0x23 -> NUMBER SIGN, left-right
    '$'         #  0x24 -> DOLLAR SIGN, left-right
    '%'         #  0x25 -> PERCENT SIGN, left-right
    '&'         #  0x26 -> AMPERSAND
    "'"         #  0x27 -> APOSTROPHE, left-right
    '('         #  0x28 -> LEFT PARENTHESIS, left-right
    ')'         #  0x29 -> RIGHT PARENTHESIS, left-right
    '*'         #  0x2A -> ASTERISK, left-right
    '+'         #  0x2B -> PLUS SIGN, left-right
    ','         #  0x2C -> COMMA, left-right
    '-'         #  0x2D -> HYPHEN-MINUS, left-right
    '.'         #  0x2E -> FULL STOP, left-right
    '/'         #  0x2F -> SOLIDUS, left-right
    '0'         #  0x30 -> DIGIT ZERO
    '1'         #  0x31 -> DIGIT ONE
    '2'         #  0x32 -> DIGIT TWO
    '3'         #  0x33 -> DIGIT THREE
    '4'         #  0x34 -> DIGIT FOUR
    '5'         #  0x35 -> DIGIT FIVE
    '6'         #  0x36 -> DIGIT SIX
    '7'         #  0x37 -> DIGIT SEVEN
    '8'         #  0x38 -> DIGIT EIGHT
    '9'         #  0x39 -> DIGIT NINE
    ':'         #  0x3A -> COLON, left-right
    ';'         #  0x3B -> SEMICOLON, left-right
    '<'         #  0x3C -> LESS-THAN SIGN, left-right
    '='         #  0x3D -> EQUALS SIGN, left-right
    '>'         #  0x3E -> GREATER-THAN SIGN, left-right
    '?'         #  0x3F -> QUESTION MARK, left-right
    '@'         #  0x40 -> COMMERCIAL AT
    'A'         #  0x41 -> LATIN CAPITAL LETTER A
    'B'         #  0x42 -> LATIN CAPITAL LETTER B
    'C'         #  0x43 -> LATIN CAPITAL LETTER C
    'D'         #  0x44 -> LATIN CAPITAL LETTER D
    'E'         #  0x45 -> LATIN CAPITAL LETTER E
    'F'         #  0x46 -> LATIN CAPITAL LETTER F
    'G'         #  0x47 -> LATIN CAPITAL LETTER G
    'H'         #  0x48 -> LATIN CAPITAL LETTER H
    'I'         #  0x49 -> LATIN CAPITAL LETTER I
    'J'         #  0x4A -> LATIN CAPITAL LETTER J
    'K'         #  0x4B -> LATIN CAPITAL LETTER K
    'L'         #  0x4C -> LATIN CAPITAL LETTER L
    'M'         #  0x4D -> LATIN CAPITAL LETTER M
    'N'         #  0x4E -> LATIN CAPITAL LETTER N
    'O'         #  0x4F -> LATIN CAPITAL LETTER O
    'P'         #  0x50 -> LATIN CAPITAL LETTER P
    'Q'         #  0x51 -> LATIN CAPITAL LETTER Q
    'R'         #  0x52 -> LATIN CAPITAL LETTER R
    'S'         #  0x53 -> LATIN CAPITAL LETTER S
    'T'         #  0x54 -> LATIN CAPITAL LETTER T
    'U'         #  0x55 -> LATIN CAPITAL LETTER U
    'V'         #  0x56 -> LATIN CAPITAL LETTER V
    'W'         #  0x57 -> LATIN CAPITAL LETTER W
    'X'         #  0x58 -> LATIN CAPITAL LETTER X
    'Y'         #  0x59 -> LATIN CAPITAL LETTER Y
    'Z'         #  0x5A -> LATIN CAPITAL LETTER Z
    '['         #  0x5B -> LEFT SQUARE BRACKET, left-right
    '\\'        #  0x5C -> REVERSE SOLIDUS
    ']'         #  0x5D -> RIGHT SQUARE BRACKET, left-right
    '^'         #  0x5E -> CIRCUMFLEX ACCENT
    '_'         #  0x5F -> LOW LINE
    '`'         #  0x60 -> GRAVE ACCENT
    'a'         #  0x61 -> LATIN SMALL LETTER A
    'b'         #  0x62 -> LATIN SMALL LETTER B
    'c'         #  0x63 -> LATIN SMALL LETTER C
    'd'         #  0x64 -> LATIN SMALL LETTER D
    'e'         #  0x65 -> LATIN SMALL LETTER E
    'f'         #  0x66 -> LATIN SMALL LETTER F
    'g'         #  0x67 -> LATIN SMALL LETTER G
    'h'         #  0x68 -> LATIN SMALL LETTER H
    'i'         #  0x69 -> LATIN SMALL LETTER I
    'j'         #  0x6A -> LATIN SMALL LETTER J
    'k'         #  0x6B -> LATIN SMALL LETTER K
    'l'         #  0x6C -> LATIN SMALL LETTER L
    'm'         #  0x6D -> LATIN SMALL LETTER M
    'n'         #  0x6E -> LATIN SMALL LETTER N
    'o'         #  0x6F -> LATIN SMALL LETTER O
    'p'         #  0x70 -> LATIN SMALL LETTER P
    'q'         #  0x71 -> LATIN SMALL LETTER Q
    'r'         #  0x72 -> LATIN SMALL LETTER R
    's'         #  0x73 -> LATIN SMALL LETTER S
    't'         #  0x74 -> LATIN SMALL LETTER T
    'u'         #  0x75 -> LATIN SMALL LETTER U
    'v'         #  0x76 -> LATIN SMALL LETTER V
    'w'         #  0x77 -> LATIN SMALL LETTER W
    'x'         #  0x78 -> LATIN SMALL LETTER X
    'y'         #  0x79 -> LATIN SMALL LETTER Y
    'z'         #  0x7A -> LATIN SMALL LETTER Z
    '{'         #  0x7B -> LEFT CURLY BRACKET, left-right
    '|'         #  0x7C -> VERTICAL LINE, left-right
    '}'         #  0x7D -> RIGHT CURLY BRACKET, left-right
    '~'         #  0x7E -> TILDE
    '\x7f'      #  0x7F -> CONTROL CHARACTER
    '\xc4'      #  0x80 -> LATIN CAPITAL LETTER A WITH DIAERESIS
    '\ufb1f'    #  0x81 -> HEBREW LIGATURE YIDDISH YOD YOD PATAH
    '\xc7'      #  0x82 -> LATIN CAPITAL LETTER C WITH CEDILLA
    '\xc9'      #  0x83 -> LATIN CAPITAL LETTER E WITH ACUTE
    '\xd1'      #  0x84 -> LATIN CAPITAL LETTER N WITH TILDE
    '\xd6'      #  0x85 -> LATIN CAPITAL LETTER O WITH DIAERESIS
    '\xdc'      #  0x86 -> LATIN CAPITAL LETTER U WITH DIAERESIS
    '\xe1'      #  0x87 -> LATIN SMALL LETTER A WITH ACUTE
    '\xe0'      #  0x88 -> LATIN SMALL LETTER A WITH GRAVE
    '\xe2'      #  0x89 -> LATIN SMALL LETTER A WITH CIRCUMFLEX
    '\xe4'      #  0x8A -> LATIN SMALL LETTER A WITH DIAERESIS
    '\xe3'      #  0x8B -> LATIN SMALL LETTER A WITH TILDE
    '\xe5'      #  0x8C -> LATIN SMALL LETTER A WITH RING ABOVE
    '\xe7'      #  0x8D -> LATIN SMALL LETTER C WITH CEDILLA
    '\xe9'      #  0x8E -> LATIN SMALL LETTER E WITH ACUTE
    '\xe8'      #  0x8F -> LATIN SMALL LETTER E WITH GRAVE
    '\xea'      #  0x90 -> LATIN SMALL LETTER E WITH CIRCUMFLEX
    '\xeb'      #  0x91 -> LATIN SMALL LETTER E WITH DIAERESIS
    '\xed'      #  0x92 -> LATIN SMALL LETTER I WITH ACUTE
    '\xec'      #  0x93 -> LATIN SMALL LETTER I WITH GRAVE
    '\xee'      #  0x94 -> LATIN SMALL LETTER I WITH CIRCUMFLEX
    '\xef'      #  0x95 -> LATIN SMALL LETTER I WITH DIAERESIS
    '\xf1'      #  0x96 -> LATIN SMALL LETTER N WITH TILDE
    '\xf3'      #  0x97 -> LATIN SMALL LETTER O WITH ACUTE
    '\xf2'      #  0x98 -> LATIN SMALL LETTER O WITH GRAVE
    '\xf4'      #  0x99 -> LATIN SMALL LETTER O WITH CIRCUMFLEX
    '\xf6'      #  0x9A -> LATIN SMALL LETTER O WITH DIAERESIS
    '\xf5'      #  0x9B -> LATIN SMALL LETTER O WITH TILDE
    '\xfa'      #  0x9C -> LATIN SMALL LETTER U WITH ACUTE
    '\xf9'      #  0x9D -> LATIN SMALL LETTER U WITH GRAVE
    '\xfb'      #  0x9E -> LATIN SMALL LETTER U WITH CIRCUMFLEX
    '\xfc'      #  0x9F -> LATIN SMALL LETTER U WITH DIAERESIS
    ' '         #  0xA0 -> SPACE, right-left
    '!'         #  0xA1 -> EXCLAMATION MARK, right-left
    '"'         #  0xA2 -> QUOTATION MARK, right-left
    '#'         #  0xA3 -> NUMBER SIGN, right-left
    '$'         #  0xA4 -> DOLLAR SIGN, right-left
    '%'         #  0xA5 -> PERCENT SIGN, right-left
    '\u20aa'    #  0xA6 -> NEW SHEQEL SIGN
    "'"         #  0xA7 -> APOSTROPHE, right-left
    ')'         #  0xA8 -> RIGHT PARENTHESIS, right-left # close parenthesis
    '('         #  0xA9 -> LEFT PARENTHESIS, right-left # open parenthesis
    '*'         #  0xAA -> ASTERISK, right-left
    '+'         #  0xAB -> PLUS SIGN, right-left
    ','         #  0xAC -> COMMA, right-left
    '-'         #  0xAD -> HYPHEN-MINUS, right-left
    '.'         #  0xAE -> FULL STOP, right-left
    '/'         #  0xAF -> SOLIDUS, right-left
    '0'         #  0xB0 -> DIGIT ZERO, right-left (need override)
    '1'         #  0xB1 -> DIGIT ONE, right-left (need override)
    '2'         #  0xB2 -> DIGIT TWO, right-left (need override)
    '3'         #  0xB3 -> DIGIT THREE, right-left (need override)
    '4'         #  0xB4 -> DIGIT FOUR, right-left (need override)
    '5'         #  0xB5 -> DIGIT FIVE, right-left (need override)
    '6'         #  0xB6 -> DIGIT SIX, right-left (need override)
    '7'         #  0xB7 -> DIGIT SEVEN, right-left (need override)
    '8'         #  0xB8 -> DIGIT EIGHT, right-left (need override)
    '9'         #  0xB9 -> DIGIT NINE, right-left (need override)
    ':'         #  0xBA -> COLON, right-left
    ';'         #  0xBB -> SEMICOLON, right-left
    '<'         #  0xBC -> LESS-THAN SIGN, right-left
    '='         #  0xBD -> EQUALS SIGN, right-left
    '>'         #  0xBE -> GREATER-THAN SIGN, right-left
    '?'         #  0xBF -> QUESTION MARK, right-left
    '\ufffe'
    '\u201e'    #  0xC1 -> DOUBLE LOW-9 QUOTATION MARK, right-left
    '\uf89b'    #  0xC2 -> Hebrew canoral 1
    '\uf89c'    #  0xC3 -> Hebrew canoral 2
    '\uf89d'    #  0xC4 -> Hebrew canoral 3
    '\uf89e'    #  0xC5 -> Hebrew canoral 4
    '\u05bc'    #  0xC6 -> HEBREW POINT DAGESH OR MAPIQ
    '\ufb4b'    #  0xC7 -> HEBREW LETTER VAV WITH HOLAM
    '\ufb35'    #  0xC8 -> HEBREW LETTER VAV WITH DAGESH
    '\u2026'    #  0xC9 -> HORIZONTAL ELLIPSIS, right-left
    '\xa0'      #  0xCA -> NO-BREAK SPACE, right-left
    '\u05b8'    #  0xCB -> HEBREW POINT QAMATS
    '\u05b7'    #  0xCC -> HEBREW POINT PATAH
    '\u05b5'    #  0xCD -> HEBREW POINT TSERE
    '\u05b6'    #  0xCE -> HEBREW POINT SEGOL
    '\u05b4'    #  0xCF -> HEBREW POINT HIRIQ
    '\u2013'    #  0xD0 -> EN DASH, right-left
    '\u2014'    #  0xD1 -> EM DASH, right-left
    '\u201c'    #  0xD2 -> LEFT DOUBLE QUOTATION MARK, right-left
    '\u201d'    #  0xD3 -> RIGHT DOUBLE QUOTATION MARK, right-left
    '\u2018'    #  0xD4 -> LEFT SINGLE QUOTATION MARK, right-left
    '\u2019'    #  0xD5 -> RIGHT SINGLE QUOTATION MARK, right-left
    '\ufb2a'    #  0xD6 -> HEBREW LETTER SHIN WITH SHIN DOT
    '\ufb2b'    #  0xD7 -> HEBREW LETTER SHIN WITH SIN DOT
    '\u05bf'    #  0xD8 -> HEBREW POINT RAFE
    '\u05b0'    #  0xD9 -> HEBREW POINT SHEVA
    '\u05b2'    #  0xDA -> HEBREW POINT HATAF PATAH
    '\u05b1'    #  0xDB -> HEBREW POINT HATAF SEGOL
    '\u05bb'    #  0xDC -> HEBREW POINT QUBUTS
    '\u05b9'    #  0xDD -> HEBREW POINT HOLAM
    '\u05c7'    #  0xDE -> HEBREW POINT QAMATS, alternate form "qamats qatan"
    '\u05b3'    #  0xDF -> HEBREW POINT HATAF QAMATS
    '\u05d0'    #  0xE0 -> HEBREW LETTER ALEF
    '\u05d1'    #  0xE1 -> HEBREW LETTER BET
    '\u05d2'    #  0xE2 -> HEBREW LETTER GIMEL
    '\u05d3'    #  0xE3 -> HEBREW LETTER DALET
    '\u05d4'    #  0xE4 -> HEBREW LETTER HE
    '\u05d5'    #  0xE5 -> HEBREW LETTER VAV
    '\u05d6'    #  0xE6 -> HEBREW LETTER ZAYIN
    '\u05d7'    #  0xE7 -> HEBREW LETTER HET
    '\u05d8'    #  0xE8 -> HEBREW LETTER TET
    '\u05d9'    #  0xE9 -> HEBREW LETTER YOD
    '\u05da'    #  0xEA -> HEBREW LETTER FINAL KAF
    '\u05db'    #  0xEB -> HEBREW LETTER KAF
    '\u05dc'    #  0xEC -> HEBREW LETTER LAMED
    '\u05dd'    #  0xED -> HEBREW LETTER FINAL MEM
    '\u05de'    #  0xEE -> HEBREW LETTER MEM
    '\u05df'    #  0xEF -> HEBREW LETTER FINAL NUN
    '\u05e0'    #  0xF0 -> HEBREW LETTER NUN
    '\u05e1'    #  0xF1 -> HEBREW LETTER SAMEKH
    '\u05e2'    #  0xF2 -> HEBREW LETTER AYIN
    '\u05e3'    #  0xF3 -> HEBREW LETTER FINAL PE
    '\u05e4'    #  0xF4 -> HEBREW LETTER PE
    '\u05e5'    #  0xF5 -> HEBREW LETTER FINAL TSADI
    '\u05e6'    #  0xF6 -> HEBREW LETTER TSADI
    '\u05e7'    #  0xF7 -> HEBREW LETTER QOF
    '\u05e8'    #  0xF8 -> HEBREW LETTER RESH
    '\u05e9'    #  0xF9 -> HEBREW LETTER SHIN
    '\u05ea'    #  0xFA -> HEBREW LETTER TAV
    '}'         #  0xFB -> RIGHT CURLY BRACKET, right-left
    ']'         #  0xFC -> RIGHT SQUARE BRACKET, right-left
    '{'         #  0xFD -> LEFT CURLY BRACKET, right-left
    '['         #  0xFE -> LEFT SQUARE BRACKET, right-left
    '|'         #  0xFF -> VERTICAL LINE, right-left
)

### Encoding table
encoding_table = codecs.charmap_build(decoding_table)

