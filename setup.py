# -*- coding: utf-8 -*-

import distutils.core
import logutils
import os
from os.path import join, dirname, abspath
import re

def missing_files():
    result = []
    if os.name == 'nt':

        def found_file(fn):
            if os.path.exists(fn):
                return True
            for d in os.environ['PATH'].split(os.pathsep):
                p = os.path.join(d, fn)
                if os.path.exists(p):
                    return True
            return False

        FILES = ('cat.exe', 'echo.exe', 'tee.exe', 'false.exe', 'true.exe',
                 'sleep.exe', 'touch.exe')
        print('APPVEYOR: %s' % os.environ.get('APPVEYOR'))
        if os.environ.get('APPVEYOR', 'False') != 'True':
            FILES = ('libiconv2.dll', 'libintl3.dll') + FILES

        missing = []
        for fn in FILES:
            if not found_file(fn):
                result.append(fn)
    return result


def description():
    f = open(join(dirname(__file__), 'README.rst'))
    readme = f.read()
    f.close()
    regexp = r'logutils\s*[\d.]*\s*\n=======+\s*\n(.*)Requirements '
    reqts, = re.findall(regexp, readme, re.DOTALL)
    regexp = r'Availability & Documentation\s*\n-----+\s*\n(.*)'
    avail, = re.findall(regexp, readme, re.DOTALL)
    return reqts + avail

class TestCommand(distutils.core.Command):
    user_options = []

    def run(self):
        missing = missing_files()

        if missing:
            missing = ', '.join(missing)
            raise ValueError('Can\'t find one or more files needed for '
                             'tests: %s' % missing)

        import sys
        import unittest

        sys.path.append(join(dirname(__file__), 'tests'))
        import logutil_tests
        loader = unittest.TestLoader()
        runner = unittest.TextTestRunner()
        test_results = runner.run(loader.loadTestsFromModule(logutil_tests))
        if not test_results.wasSuccessful():
            sys.exit(1)

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
    license='Copyright (C) 2010-2017 by Vinay Sajip. All Rights Reserved. See LICENSE.txt for license.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Topic :: Software Development',
    ],
    packages=['logutils'],
    cmdclass={
        'test': TestCommand,
    },

)
