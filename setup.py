# coding: utf-8
try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
long_description = 'Get current coin (btc/eth/xrp) ticker from exchanges (bitflyer/btcbox/zaif/bitbank/quoinex)'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name  = 'arbitrage',
    version = '0.1.5',
    description = 'Get current coin (btc/eth/xrp) ticker from exchanges (bitflyer/btcbox/zaif/bitbank/quoinex)',
    long_description = long_description,
    license = 'MIT',
    author = '10mohi6',
    author_email = '10.mohi.6.y@gmail.com',
    url = 'https://github.com/10mohi6/arbitrage-python',
    keywords = 'arbitrage',
    py_modules=['arbitrage'],
    install_requires = ['grequests'],
    classifiers = [
      'Development Status :: 4 - Beta',
      'Programming Language :: Python :: 3.6',
      'Intended Audience :: Financial and Insurance Industry',
      'Intended Audience :: Developers',
      'Intended Audience :: Information Technology',
      'Operating System :: OS Independent',
      'Topic :: Software Development :: Build Tools',
      'Topic :: Office/Business :: Financial :: Investment',
      'License :: OSI Approved :: MIT License'
    ]
)