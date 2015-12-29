#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='e24PaymentPipe',
    version='1.2.0',
    description="This package provides a Python implementation for ACI's e24PaymentPipe Merchant Gateway",
    long_description=readme + '\n\n' + history,
    author='Burhan Khalid',
    author_email='burhan.khalid@gmail.com',
    url='https://github.com/burhan/e24PaymentPipe',
    packages=[
        'e24PaymentPipe',
    ],
    package_dir={'e24PaymentPipe': 'e24PaymentPipe'},
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license="BSD",
    zip_safe=False,
    keywords='e24PaymentPipe',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
)
