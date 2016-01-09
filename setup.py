# -*- coding: utf-8 -*-
#!/usr/bin/env python

import codecs
import glob
import os
import sys

from setuptools import setup, find_packages

PACKAGE = 'cesiumpy'
README = 'README.rst'
REQUIREMENTS = 'requirements.txt'

VERSION = '0.1.1.dev'

def read(fname):
  # file must be read as utf-8 in py3 to avoid to be bytes
  return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

def write_version_py(filename=None):
    cnt = """\
version = '%s'
"""
    a = open(filename, 'w')
    try:
        a.write(cnt % VERSION)
    finally:
        a.close()

version_file = os.path.join(os.path.dirname(__file__), PACKAGE, 'version.py')
write_version_py(filename=version_file)

install_requires = list(read(REQUIREMENTS).splitlines())
if sys.version_info < (3, 4, 0):
    install_requires.append('enum34')

# include cesiumlib
data_files = []
def get_dirs(path):
    contents = glob.glob(os.path.join(path, '*'))
    current_files = []
    for c in contents:
        if os.path.isdir(c):
            get_dirs(c)
        else:
            current_files.append(c)
    data_files.append((path, current_files))
get_dirs(os.path.join(PACKAGE, 'cesiumlib'))


setup(name=PACKAGE,
      version=VERSION,
      description='python wrapper for cesium.js',
      long_description=read(README),
      author='sinhrks',
      author_email='sinhrks@gmail.com',
      url='http://cesiumpy.readthedocs.org/en/stable',
      license = 'Apache 2.0',
      packages=find_packages(),
      data_files=data_files,
      install_requires=install_requires
      )


