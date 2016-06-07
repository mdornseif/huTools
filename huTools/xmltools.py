#!/usr/bin/env python
# encoding: utf-8
"""
xmltools.py

Created by Christian Klein on 2010-02-26.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import datetime
import xml.etree.ElementTree as ET


def encode_text(data):
    """
    Encode for usage in XML Tree

    >>> encode_text(None)
    u''
    >>> encode_text('Alex')
    u'Alex'
    >>> encode_text(u'Alex')
    u'Alex'
    >>> encode_text(12)
    u'12'
    >>> encode_text(callable(encode_text))
    u'True'
    >>> encode_text(callable)
    u''
    """

    if callable(data):
        try:
            return encode_text(data())
        except TypeError:
            return u''

    if isinstance(data, str):
        return data.decode('utf-8', 'replace')
    elif isinstance(data, datetime.datetime):
        if not(data.hour or data.minute):
            fmt = '%Y-%m-%d'
        else:
            fmt = '%Y-%m-%d %H:%M'
        return data.strftime(fmt)
    elif data is None:
        return u''
    else:
        return unicode(data)


def add_fields(root, source, fieldnames):
    """
    Appends a number of fields from a source object to a XML Tree (root).
    If the source object does not contain an attribute, an empty element is appended.
    Otherwise, encode_text is called.

    >>> root = ET.Element("address")
    >>> class Address(object):
    ...     def __init__(self, **kwargs):
    ...         for key, value in kwargs.items():
    ...             setattr(self, key, value)
    >>> a = Address(name1=u'HUDORA', strasse=u'Jägerwald 13', t='one')
    >>> add_fields(root, a, ['name1', 'name2', 'strasse', 'plz', 'ort'])
    >>> ET.tostring(root)
    '<address><name1>HUDORA</name1><name2 /><strasse>J&#228;gerwald 13</strasse></address>'
    """
    for fieldname in fieldnames:
        elem = ET.SubElement(root, fieldname)
        if hasattr(source, fieldname):
            elem.text = encode_text(getattr(source, fieldname, ''))
    return root


if __name__ == "__main__":
    import doctest
    doctest.testmod()
