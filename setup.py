# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.2'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='pathaliases',
    version=__version__,
    description='A python package for handling path aliases.',
    long_description=long_description,
    url='https://github.com/adamkewley/pathaliases',
    download_url='https://github.com/adamkewley/pathaliases/tarball/' + __version__,
    license='Apache 2.0',
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3.4',
      'License :: OSI Approved :: Apache Software License',
    ],
    keywords='path aliasing',
    py_modules=['pathaliases'],
    include_package_data=True,
    author='Adam Kewley',
    author_email='contact@adamkewley.com',
    install_requires=install_requires,
    dependency_links=dependency_links,
    python_requires='>=3',
)
