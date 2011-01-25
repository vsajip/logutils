# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import distutils.core
import logutils
from os.path import join, dirname, abspath
import re


def description():
    f = open(join(dirname(__file__), 'README.txt'))
    readme = f.read()
    f.close()
    regexp = r'^logutils\s*[\d.]*\s*\n=======+\s*\n(.*)Requirements '
    reqts, = re.findall(regexp, readme, re.DOTALL)
    regexp = r'Availability & Documentation\s*\n-----+\s*\n(.*)'
    avail, = re.findall(regexp, readme, re.DOTALL)
    return reqts + avail

class TestCommand(distutils.core.Command):
    user_options = []

    def run(self):
        import sys
        import unittest
        
        sys.path.append(join(dirname(__file__), 'tests'))
        import logutil_tests
        loader = unittest.TestLoader()
        runner = unittest.TextTestRunner()
        runner.run(loader.loadTestsFromModule(logutil_tests))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

distutils.core.setup(
    name='logutils',
    version=logutils.__version__,
    author='Vinay Sajip',
    author_email='vinay_sajip@red-dove.com',
    url='http://code.google.com/p/logutils/',
    description='Logging utilities',
    long_description = description(),
    license='New BSD',
    classifiers=[
        'Development Status :: 5 - Production',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Topic :: Software Development',
    ],
    packages=['logutils'],
    cmdclass={
        'test': TestCommand,
    },
    
)
