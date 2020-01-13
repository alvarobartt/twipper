#!/usr/bin/env python

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='twipper',
    version='0.1.6',
    packages=find_packages(),
    url='https://github.com/alvarob96/twipper',
    download_url='https://github.com/alvarob96/twipper/archive/0.1.6.tar.gz',
    license='GNU General Public License v3 (GPLv3)',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='twipper - is a Twitter API wrapper for both free and premium plans developed on Python',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.22.0',
        'requests_oauthlib>=1.2.0',
        'oauth2>=1.9.0.post1',
        'setuptools>=41.2.0'
    ],
    data_files=[],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords='twitter, twitter-wrapper, twitter-api',
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://github.com/alvarob96/twipper/issues',
        'Source': 'https://github.com/alvarob96/twipper',
        'Documentation': 'https://twipper.readthedocs.io/'
    },
)
