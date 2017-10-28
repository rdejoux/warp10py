# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

try:
    from urllib.parse import quote
except ImportError:
    from urllib2 import quote


def get_tlle(ts=None, lat=None, lon=None, elev=None):
    res = '{0:d}/'.format(ts) if ts else '/'
    res += '{0:f}:{1:f}/'.format(lat, lon) if lat is not None and lon is not None else '/'
    if elev:
        res += '{0:f}'.format(elev)
    return res


def get_labels(labels):
    keys = list(labels)  # get keys
    keys.sort()
    return '{{{0}}}'.format(','.join(['{0}={1}'.format(k, quote(str(labels[k])))
                                      for k in keys]))


def get_ident(clsname, labels):
    return '{0}{1}'.format(clsname,
                           get_labels(labels))


def get_gts_line(value, ts=None, lat=None, lon=None, elev=None,
                 ident=None, clsname=None, labels=None):
    if clsname and labels:
        ident = get_ident(clsname, labels)

    tlle = get_tlle(ts=ts, lat=lat, lon=lon, elev=elev)

    gts_format = '{tlle} {cls} {value}\n'
    if not ident:
        gts_format = '={tlle} {value}\n'
    if isinstance(value, str):
        value = "'{0}'".format(quote(value))

    return gts_format.format(tlle=tlle,
                             cls=ident,
                             value=value)


def get_meta_line(attributes,
                  ident=None,
                  clsname=None, labels=None):
    if not attributes:
        return ''

    if clsname and labels:
        ident = get_ident(clsname, labels)

    return '{0}{1}\n'.format(ident, get_labels(attributes))


