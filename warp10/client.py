# -*- coding: utf-8 -*-
"""
:Authors:
  - Romain de Joux

:Copyright:
  - Romain de Joux 2017

:License:
  - Apache License Version 2.0
"""

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)


import time
import datetime
from io import StringIO
from collections import OrderedDict

import requests

from .config import default as default_config
from .gtshelper import get_gts_line, get_meta_line


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
            print(r.status_code, r.text)
            raise Warp10UpdateError(r.status_code, r.text)

    def warpscript_exec(self, warpscript):
        pass

    def meta(self, lines):
        post_buff = StringIO()
        post_buff.writelines(lines)
        post_buff.seek(0)

        r = requests.post(self.config.meta_url,
                          data=post_buff.getvalue(),
                          headers={'X-Warp10-Token': self.config.write_token,
                                   # Needed to auth with OVH Metrics
                                   'X-CITYZENDATA-TOKEN': self.config.write_token})
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
    def __init__(self, client, buffer_size=(64 * 1024)):
        self.client = client
        self.buffer_size = buffer_size
        self.gts = []
        self.attribs = OrderedDict()

    def __len__(self):
        return len(self.gts)

    def add_value(self, clsname, labels, value, ts, lat=None, lon=None, elev=None):
        self.gts.append(get_gts_line(value, ts,
                                     lat=None, lon=None, elev=None,
                                     clsname=clsname, labels=labels))
        if len(self) > self.buffer_size:
            self.flush()

    def update_attributes(self, clsname, labels, attributes):
        self.attribs[get_meta_line(attributes,
                                   clsname=clsname, labels=labels)] = None

    def flush(self):
        t0 = time.time()
        self.client.update(self.gts)
        self.client.meta(self.attribs.keys())
        self.clean()
        print('[{0:%H:%M:%S}] Flush data. | Duration: {1:0.1f}'.format(datetime.datetime.now(),
                                                                       time.time() - t0))

    def clean(self):
        self.gts = []
        self.attribs = OrderedDict()
