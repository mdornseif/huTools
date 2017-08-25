#!/usr/bin/env python
# encoding: utf-8
"""
dictools.py - tools for dictionaries

Created by Christian Klein on 2017-08-25.
Copyright (c) 2017 HUDORA. All rights reserved.
"""

def filter_dict(obj, whitelist):
    """Filters a dict to only contain keys from a whitelist"""
    return dict((key, value) for key, value in obj.iteritems() if key in whitelist)
