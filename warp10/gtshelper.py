# -*- coding: utf-8 -*-

from urllib import quote


def get_tlle(ts=None, lat=None, lon=None, elev=None):
    res = '{0:d}/'.format(ts) if ts else '/'
    res += '{0:f}:{1:f}/'.format(lat, lon) if lat is not None and lon is not None else '/'
    if elev:
        res += '{0:f}'.format(elev)
    return res


def get_ident(clsname, labels):
    return '{0}{{{1}}}'.format(clsname,
                               ','.join(['{0}={1}'.format(*items)
                                         for items in labels.items()]))


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
    def __init__(self, ident=None, clsname=None, labels=None):
        if clsname and labels:
            ident = get_ident(clsname, labels)
        self.ident = ident
        self.values = []

    def __len__(self):
        return len(self.values) * len(self.clsnames)

    def clean(self):
        self.values = []

    def add_value(self, value, ts, lat=None, lon=None, elev=None):
        if self.values and self.values[-1][1][0] == ts:
            return  # doublon
        if isinstance(value, str):
            value = "'{0}'".format(quote(value))
        self.values.append((value, (ts, lat, lon, elev)))

    def iter_gts_lines(self, uniq_class_def):
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
