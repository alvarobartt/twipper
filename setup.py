#!/usr/bin/env python

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='twipper',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/alvarob96/twipper',
    download_url='https://github.com/alvarob96/twipper/archive/0.0.2.tar.gz',
    license='GNU General Public License v3 (GPLv3)',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='twipper - is a Python package that works as a Twitter API Wrapper',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=['requests==2.22.0',
                      'requests_oauthlib==1.2.0',
                      'oauth2==1.9.0.post1',
                      'setuptools==40.6.3'],
    data_files=[],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
    ],
    keywords='twitter, wrapper, api'
)
