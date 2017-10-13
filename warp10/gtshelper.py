# -*- coding: utf-8 -*-

from urllib.parse import quote


def get_tlle(ts=None, lat=None, lon=None, elev=None):
    res = '{0:d}/'.format(ts) if ts else '/'
    res += '{0:f}:{1:f}/'.format(lat, lon) if lat is not None and lon is not None else '/'
    if elev:
        res += '{0:f}'.format(elev)
    return res


def get_labels(labels):
    return '{{{0}}}'.format(','.join(['{0}={1}'.format(k, quote(str(v)))
                                      for k, v in labels.items()]))


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


class Warp10GTSCache(object):
    def __init__(self, ident=None, clsname=None, labels=None, attributes=None):
        if clsname and labels:
            ident = get_ident(clsname, labels)
        if not attributes:
            attributes = {}
        self.ident = ident
        self.attributes = attributes

        self.values = []

    def __len__(self):
        return len(self.values)

    def clean(self):
        self.values = []
        self.attributes = {}

    def add_value(self, value, ts, lat=None, lon=None, elev=None):
        if self.values and self.values[-1][1][0] == ts:
            return  # doublon
        if isinstance(value, str):
            value = "'{0}'".format(quote(value))
        self.values.append((value, (ts, lat, lon, elev)))

    def update_attributes(self, attributes):
        self.attributes.update(attributes)

    def meta_line(self):
        if not self.attributes:
            return ''

        return '{0}{1}\n'.format(self.ident, get_labels(self.attributes))

    def iter_gts_lines(self, uniq_class_def=True):
        if not self.values:
            raise StopIteration

        ident = self.ident
        for value, (ts, lat, lon, elev) in self.values:
            yield get_gts_line(value,
                               ts=ts, lat=lat, lon=lon, elev=elev,
                               ident=ident)

            if uniq_class_def:
                ident = None

        raise StopIteration

