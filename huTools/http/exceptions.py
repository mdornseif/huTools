#!/usr/bin/env python
# encoding: utf-8
"""
exceptions.py

Created by Christian Klein on 2011-05-16.
Copyright (c) 2011 HUDORA GmbH. All rights reserved.
"""


class BaseHTTPException(RuntimeError):
    """Base for all our exceptions"""
    pass

class WrongStatusCode(BaseHTTPException):
    """Thrown if the Server returns a unexpected status code."""
    pass


class Timeout(BaseHTTPException):
    """Thrown on request timeout"""
    pass
