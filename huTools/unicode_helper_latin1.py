#!/usr/bin/env python
# encoding: latin-1

"""
Copyright (c) 2016 HUDORA GmbH. BSD Licensed.
"""

import re


CTRLPOINTS = re.compile(u'[\x00-\x1F]|[\x7F-\x9F]')
REPLACRS = {
    " ": "\xA0",
    "": "µ¤¶º®©|¦¨",
    "'": "´`",
    "(": "«<[{",
    ")": "»>]}",
    "+": "±",
    "-": "~_¯¬",
    ".": "·¸°",
    "/": "\\",
    "1": "¹",
    "1/2": "½",
    "1/4": "¼",
    "2": "²",
    "3": "³",
    "3/4": "¾",
    "?": "¿",
    "a": "ª",
    "f": "",
    "i": "¡",
    '"': '',
}
# this could be an one liner
REVERSEREPLACRS = {}
for result, inputs in REPLACRS.iteritems():
    for c in inputs:
        REVERSEREPLACRS[c] = result
REPLACE_RE = re.compile('[%s]' % ''.join([re.escape(x) for x in REVERSEREPLACRS.keys()]))


def deNoiseLatin1(data):
    """Replace typical latin1 problem chars."""
    data = data.encode('latin-1', 'ignore')

    def noiserepl(matchobj):
        return REVERSEREPLACRS.get(matchobj.group(0), '_')
    data = REPLACE_RE.sub(noiserepl, data)
    data = CTRLPOINTS.sub('', data)  # removes Control Characters
    return data.decode('latin-1')
