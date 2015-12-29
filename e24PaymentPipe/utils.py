# -*- coding: utf-8 -*-
import itertools

""" This module contains
    various utility methods
    that were extracted from the main
    Gateway class
"""

FILTER_CHARS = ['~', '`', '!', '#', '$', '%', '^', '|', '\\', ':', "'", '"', '/']


def xor(cryptext=None):
    """
    :param cryptext: The crypted text to decipher
    :return: the plain text
    """
    key = "Those who profess to favour freedom and yet depreciate agitation are men who want rain without thunder "
    key += "and lightning"
    key = itertools.cycle(bytearray(key, 'utf-8'))
    return bytearray([a ^ b for a, b in zip(cryptext, key)])


def sanitize(s):
    """
    Filter out characters not allowed in the tracking id or the UDF values
    """
    return s.translate(None, ''.join(FILTER_CHARS))
