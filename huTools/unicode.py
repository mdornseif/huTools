#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2007, 2015, 2016 HUDORA GmbH. BSD Licensed.
"""

import doctest
import re
import string
import sys
import unicodedata

from types import StringType

import huTools.unicode_helper_latin1


def deUTF8(data):
    """This is meant to help with utf-8 data appearing where unicode should apperar."""
    # In particular my DB is returning the wrong thing.
    if isinstance(data, StringType):
        return data.decode('utf-8')
    return data


# native, HTML, default Unicode (Code page 850), Unicode combined Character, Windows-1250
_recodings = {'ae': ['ä', u'ä', '&auml;', '\u00E4', u'\u00E4', '\u0308a', '\xc3\xa4'],
              'oe': ['ö', u'ö', '&ouml;', '\u00F6', u'\u00F6', '\u0308o', '\xc3\xb6', u'á'],
              'ue': ['ü', u'ü', '&uuml;', '\u00FC', u'\u00FC', '\u0308u', '\xc3\xbc'],
              'Ae': ['Ä', u'Ä', '&Auml;', '\u00C4', u'\u00C4', '\u0308A', '\xc3\x84'],
              'Oe': ['Ö', u'Ö', '&Ouml;', '\u00D6', u'\u00D6', '\u0308O', '\xc3\x96', u'Ó'],
              'Ue': ['Ü', u'Ü', '&Uuml;', '\u00DC', u'\u00DC', '\u0308U', '\xc3\x9c'],
              'ss': ['ß', u'ß', '&szlig;', '\u00DF', u'\u00DF', '\xc3\x9f', u'ß'],
              'e': ['é', u'é', '\xc3\xa9', u'ê', u'è'],
              'i': [u'í', u'í'],
              'E': [u'É', u'È'],
              "'": [u'´', '´', u'`', '`'],
              }


def deUmlaut(data):
    """Converts a text to ASCII acting smart about Umlauts.

    >>> deUmlaut('1 Über Hügel saß René äöüÄÖÜß')
    '1 Ueber Huegel sass Rene aeoeueAeOeUess'
    """

    for to_char, from_chars in _recodings.items():
        for from_char in from_chars:
            try:
                data = data.replace(from_char, to_char)
            except UnicodeDecodeError:
                data = data

    data = unicodedata.normalize('NFKD', data)

    try:
        return data.encode('ascii', 'replace')
    except UnicodeEncodeError as msg:
        raise ValueError('%s: %r' % (msg, data))
    except UnicodeDecodeError as msg:
        raise ValueError('%s: %r' % (msg, data))

# see http://instagram-engineering.tumblr.com/post/118304328152
# to learn more about the mess
try:
    HIGHPOINTS = re.compile(u'[\U00010000-\U0010ffff]')
    EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
except re.error:
    # UCS-2 build
    HIGHPOINTS = re.compile('[\uD800-\uDBFF][\uDC00-\uDFFF]')
    EMOJI = re.compile(
        u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
DASHES = ""
# Crap from Windows-1250: ‚„…‰Š‹ŚŤŽŹ‘’“”•–—™›ˇ¦©«®·»śťžźĄąĽľ
# Crap fom Unicode: …
# !¡‼❕
# ¿⁇❓ ❔؟‽
# ‘’“”
# ‹ › « »
# -‐‑–‒—― see https://www.cs.tut.fi/~jkorpela/dashes.html
# _﹏
# ~〜
# ′″‴〃
# 'ʻˮ՚Ꞌꞌ
# /\⁄¦|
# &＆⅋﹠
# ·•◦‣⦿⦾⁃◘
# ※⁕⁜*⁎∗
# en space   em space   SYMBOL FOR SPACE ␠ BLANK  see https://www.cs.tut.fi/~jkorpela/chars/spaces.html


def deNoise(data):
    u"""Removes all stuff which should not appear in normal Western Text.

    >>> deNoise(u'Susie`s Giga\\Super-Markt®¿')
    u"Susie's Giga/Super-Markt?"
    >>> deNoise(u"ümlaut eins:\x01")
    u'\\xfcmlaut eins:'
    >>> deNoise(u'«😎» `Umlaute kann doctest nicht so gut´ {®} ¿👩‍👩‍👧‍👦? „👨‍❤️‍💋‍👨“ ›🎅🏻🎅🏼🎅🏽🎅🏾🎅🏿‹')
    u"() 'Umlaute kann doctest nicht so gut' () ??  "
    """
    data = unicodedata.normalize('NFC', data)
    data = huTools.unicode_helper_latin1.deNoiseLatin1(data)
    # data = unicodedata.normalize('NFKC', data) # decruft a little but keep umlauts
    return data

# from http://stackoverflow.com/questions/561486
ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SHORTALPHABET = string.digits + string.ascii_uppercase
SHORTALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(SHORTALPHABET))
SHORTBASE = len(SHORTALPHABET)
SIGN_CHARACTER = '$'


def num_encode(n):
    """Convert an integer to an base62 encoded string."""
    if n < 0:
        return SIGN_CHARACTER + num_encode(-n)
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0:
            break
    return u''.join(reversed(s))


def num_decode(s):
    """Convert the result of num_encode() back to an integer."""
    if s[0] == SIGN_CHARACTER:
        return -num_decode(s[1:])
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n


def num_encode_uppercase(n):
    """Convert an integer to an base36 encoded string."""
    if n < 0:
        return SIGN_CHARACTER + num_encode_uppercase(-n)
    s = []
    while True:
        n, r = divmod(n, SHORTBASE)
        s.append(SHORTALPHABET[r])
        if n == 0:
            break
    return u''.join(reversed(s))

if __name__ == '__main__':
    # print deNoise(u"`Iñtërnâtiônàlizætiøn!'")
    # print deNoise(u'«😎» `Iñtërnâtiônàlizætiøn´ {®} ¿👩‍👩‍👧‍👦? „👨‍❤️‍💋‍👨“ ›🎅🏻🎅🏼🎅🏽🎅🏾🎅🏿‹')
    failure_count, test_count = doctest.testmod()
    sys.exit(failure_count)
