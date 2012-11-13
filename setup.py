#!/usr/bin/env python
#This file is part party_type module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from setuptools import setup
import re
import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = []
next_minor_version = minor_version + 1
if minor_version % 2:
    next_minor_version += 1
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|workflow|webdav)(\W|$)', dep):
        requires.append('trytond_%s >= %s.%s, < %s.%s' %
                (dep, major_version, minor_version, major_version,
                    next_minor_version))
requires.append('trytond >= %s.%s, < %s.%s' %
        (major_version, minor_version, major_version, next_minor_version))

setup(name='trytonzz_party_type',
    version=info.get('version', '0.0.1'),
    description='Tryton module to add Type Party',
    author='Virtual Things',
    author_email='info@virtual-things.biz',
    url='http://www.virtual-things.biz',
    download_url="http://downloads.tryton.org/" + \
            info.get('version', '0.0.1').rsplit('.', 1)[0] + '/',
    package_dir={'trytonzz.modules.party_type': '.'},
    packages=[
        'trytonzz.modules.party_type',
        'trytonzz.modules.party_type.tests',
    ],
    package_data={
        'trytonzz.modules.party_type': info.get('xml', []) \
            + ['tryton.cfg', 'locale/*.po'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
    ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytonzz.modules]
    party_type = trytonzz.modules.party_type
    """,
    test_suite='tests',
    test_loader='trytonzz.test_loader:Loader',
)
