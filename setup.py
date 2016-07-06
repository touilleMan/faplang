#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
	"pyparsing==2.1.5",
]

test_requirements = [
    "pytest",
]

setup(
    name='faplang',
    version='0.1.0',
    description="Functional programming language for learning purpose",
    long_description=readme,
    author="Emmanuel Leblond",
    author_email='emmanuel.leblond@gmail.com',
    url='https://github.com/touilleMan/faplang',
    packages=[
        'faplang',
    ],
    package_dir={'faplang':
                 'faplang'},
    include_package_data=True,
    install_requires=requirements,
    license="WTFPLv2",
    zip_safe=False,
    keywords='faplang',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points = {
        'console_scripts': [
        	'fapi=faplang.scripts:fapi_main',
        	'fapc=faplang.scripts:fapc_main',
        ]
    },
    test_suite='tests',
    tests_require=test_requirements
)
