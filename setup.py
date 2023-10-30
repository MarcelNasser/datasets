#!/usr/bin/env python

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(name='pipelines',
      version='1.0',
      description='Research datasets',
      author='Marcel Nasser',
      author_email='marcel.nasser@live.fr',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['pipelines'],
      install_requires=requirements
      )
