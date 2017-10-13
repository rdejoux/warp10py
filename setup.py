###############################################################################
#
#
###############################################################################

from __future__ import absolute_import

import os
import sys
import platform
from setuptools import setup
from setuptools.command.test import test as test_command

# read version string
with open('warp10/__init__.py') as f:
    exec(f.read())  # defines __version__

# read package long description
with open('README.md') as f:
    docstr = f.read()


setup(
    name='warp10py',
    version=__version__,
    description='Warp10.io [http://www.warp10.io] client library (update, exec, fetch, ...) and with GTS and WarpScript helpers',
    long_description=docstr,
    license='Apache 2 license',
    author='Romain de Joux',
    url='https://github.com/rdejoux/warp10py',
    platforms='Any',
    install_requires=[
        'requests'
    ],
    extras_require={
#        'websocket': ['authobahn'],
    },
    packages=[
        'warp10',
    ],
    zip_safe=True,

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["License :: OSI Approved :: Apache Software License",
                 "Development Status :: 2 - Pre-Alpha",
                 "Environment :: No Input/Output (Daemon)",
                 "Framework :: Twisted",
                 "Intended Audience :: Developers",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: Implementation :: CPython",
                 "Programming Language :: Python :: Implementation :: PyPy",
                 "Topic :: Database :: Front-Ends",
                 "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords='warp10 timeseries database client'
)
