#
# Copyright (C) 2012-2017 Vinay Sajip. See LICENSE.txt for details.
#
import logging
import logutils.colorize
import sys
import tempfile
import unittest

if sys.version_info[0] < 3:
    u = lambda o: unicode(o, 'unicode_escape')
else:
    u = lambda o: o

class ColorizeTest(unittest.TestCase):

    def test_colorize(self):
        logger = logging.getLogger()
        handler = logutils.colorize.ColorizingStreamHandler()
        logger.addHandler(handler)
        try:
            logger.warning(u('Some unicode string with some \u015b\u0107\u017a\xf3\u0142 chars'))
        finally:
            logger.removeHandler(handler)

    def test_colorize_to_file_with_unicode(self):
        if sys.version_info >= (3, 0):
            raise unittest.SkipTest('tests 2.x specific issue')
        logger = logging.getLogger()
        with tempfile.TemporaryFile() as logfile_handle:
            handler = logutils.colorize.ColorizingStreamHandler(logfile_handle)
            logger.addHandler(handler)
            try:
                logger.warning(u('Some unicode string'))
                logfile_handle.seek(0)
                self.assertTrue('Some unicode string' in logfile_handle.read())
            finally:
                logger.removeHandler(handler)
                handler.close()
