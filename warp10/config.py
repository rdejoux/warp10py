# -*- coding: utf-8 -*-
"""
:Authors:
  - Romain de Joux

:Copyright:
  - Romain de Joux 2017

:License:
  - Apache License Version 2.0
"""

import os


class Warp10Config:
    def __init__(self):
        self.read_token = ''
        self.write_token = ''

        self.warp10_server = ''

        self.update_url = ''
        self.streamupdate_url = ''
        self.exec_url = ''
        self.fetch_url = ''
        self.delete_url = ''
        self.meta_url = ''

        # by default try to get config from ENV
        self.from_environ()

    def from_config(self, config_fname):
        pass

    def from_dict(self, config):
        self.write_token = config.get('WARP10_WRITE_TOKEN', '')
        self.read_token = config.get('WARP10_READ_TOKEN', '')
        self.warp10_server = config.get('WARP10_SERVER', '')
        if self.warp10_server:
            # set default url
            self.update_url = '{0}/api/v0/update'.format(self.warp10_server)
            self.streamupdate_url = '{0}/api/v0/streamupdate'.format(self.warp10_server)
            self.exec_url = '{0}/api/v0/exec'.format(self.warp10_server)
            self.fetch_url = '{0}/api/v0/fetch'.format(self.warp10_server)
            self.delete_url = '{0}/api/v0/delete'.format(self.warp10_server)
            self.meta_url = '{0}/api/v0/meta'.format(self.warp10_server)

        self.update_url = config.get('WARP10_UPDATE_URL', self.update_url)
        self.streamupdate_url = config.get('WARP10_STREAMUPDATE_URL',
                                           self.streamupdate_url)
        self.exec_url = config.get('WARP10_EXEC_URL', self.exec_url)
        self.fetch_url = config.get('WARP10_FETCH_URL', self.fetch_url)
        self.delete_url = config.get('WARP10_DELETE_URL', self.delete_url)
        self.meta_url = config.get('WARP10_META_URL', self.meta_url)

    def from_environ(self):
        config = {k: v for k, v in os.environ.items() if k[:6] == 'WARP10'}
        self.from_config(config)

    @property
    def write_access(self):
        return self.write_token != ''

    @property
    def read_access(self):
        return self.read_token != ''


# Initialise a default configuration instance
default = Warp10Config()
