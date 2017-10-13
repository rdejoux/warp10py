# -*- coding: utf-8 -*-
"""
:Authors:
  - Romain de Joux

:Copyright:
  - Romain de Joux 2017

:License:
  - Apache License Version 2.0
"""

import time
import datetime
from io import StringIO
from itertools import chain

import requests

from .config import default as default_config
from .gtshelper import Warp10GTSCache, get_ident


class Warp10UpdateError(Exception):
    status2txt = {200: 'Successful request. Body will contain a JSON hash of response data',
                  400: 'Error: details in response body',
                  401: 'Authentication error: response body will contain an explanation',
                  403: 'Forbidden: app disabled or over message quota'}

    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body


class Warp10Client:
    def __init__(self, config=default_config):
        self.config = config

    def update(self, gts_lines):
        post_buff = StringIO()
        post_buff.writelines(gts_lines)
        post_buff.seek(0)

        r = requests.post(self.config.update_url,
                          data=post_buff.getvalue(),
                          headers={'X-Warp10-Token': self.config.write_token})
        if r.status_code != 200:
            raise Warp10UpdateError(r.status_code, r.text)

    def warpscript_exec(self, warpscript):
        pass

    def meta(self, lines):
        post_buff = StringIO()
        post_buff.writelines(lines)
        post_buff.seek(0)

        r = requests.post(self.config.meta_url,
                          data=post_buff.getvalue(),
                          headers={'X-Warp10-Token': self.config.write_token})
        if r.status_code != 200:
            raise Warp10UpdateError(r.status_code, r.text)

    def fetch(self, selector,
              start=None, stop=None,
              now=None, timespan=None,
              format='text', dedup=False,
              result_parser=None):
        pass

    def delete(self, selector,
               start=None, stop=None,
               now=None, timespan=None):
        pass


class Warp10BufferedUpdate(object):
    def __init__(self, client, buffer_size=(128 * 1024)):
        self.client = client
        self.buffer_size = buffer_size
        self.gts = {}

    def __len__(self):
        return sum(len(gts) for gts in self.gts.values())

    def add_value(self, clsname, labels, value, ts, lat=None, lon=None, elev=None):
        ident = get_ident(clsname, labels)
        gts = self.gts.setdefault(ident, Warp10GTSCache(ident=ident))
        gts.add_value(value, ts, lat=lat, lon=lon, elev=elev)
        if len(self) > self.buffer_size:
            self.flush()


    def update_attributes(self, clsname, labels, attributes):
        ident = get_ident(clsname, labels)
        if ident not in self.gts:
            return

        self.gts[ident].update_attributes(attributes)

    def flush(self):
        t0 = time.time()
        self.client.update(chain(*[gts.iter_gts_lines() for gts in self.gts.values()]))
        self.client.meta([gts.meta_line() for gts in self.gts.values() if gts.attributes])
        self.clean()
        print('[{0:%H:%M:%S}] Flush data. | Duration: {1:0.1f}'.format(datetime.datetime.now(),
                                                                       time.time() - t0))

    def clean(self, remove_gts=False):
        for gts in self.gts.values():
            gts.clean()
        if remove_gts:
            self.gts = {}
