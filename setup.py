#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Muuse',
      version='0.0.2',
      description='Yet another audio player',
      author='Joel Griffith',
      packages=find_packages(),
      package_data={'muuse': ['images/*.png']}
)
