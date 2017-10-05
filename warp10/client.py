# -*- coding: utf-8 -*-
"""
:Authors:
  - Romain de Joux

:Copyright:
  - Romain de Joux 2017

:License:
  - Apache License Version 2.0
"""

from .config import default as default_config


class Warp10Client:
    def __init__(self, config=default_config):
        self.config = config

    def update(self, gts_lines):
        pass

    def warpscript_exec(self, warpscript):
        pass

    def meta(self, lines):
        pass

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
