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
import logging
from logging.handlers import BufferingHandler

class TestHandler(BufferingHandler):
    def __init__(self, matcher):
        # BufferingHandler takes a "capacity" argument
        # so as to know when to flush. As we're overriding
        # shouldFlush anyway, we can set a capacity of zero.
        # You can call flush() manually to clear out the
        # buffer.
        BufferingHandler.__init__(self, 0)
        self.formatted = []
        self.matcher = matcher

    def shouldFlush(self):
        return False

    def emit(self, record):
        self.formatted.append(self.format(record))
        self.buffer.append(record.__dict__)

    def flush(self):
        BufferingHandler.flush(self)
        self.formatted = []

    def matches(self, **kwargs):
        """
        Look for a saved dict whose keys/values match the supplied arguments.
        """
        result = False
        for d in self.buffer:
            if self.matcher.matches(d, **kwargs):
                result = True
                break
        #if not result:
        #    print('*** matcher failed completely on %d records' % len(self.buffer))
        return result

    def matchall(self, kwarglist):
        """
        Accept a list of keyword argument values and ensure that the handler's
        buffer of stored records matches the list one-for-one.
        """
        if self.count != len(kwarglist):
            result = False
        else:
            result = True
            for d, kwargs in zip(self.buffer, kwarglist):
                if not self.matcher.matches(d, **kwargs):
                    result = False
                    break
        return result

    @property
    def count(self):
        return len(self.buffer)

class Matcher(object):

    _partial_matches = ('msg', 'message')

    def matches(self, d, **kwargs):
        """
        Try to match a single dict with the supplied arguments.

        Keys whose values are strings and which are in self._partial_matches
        will be checked for partial (i.e. substring) matches. You can extend
        this scheme to (for example) do regular expression matching, etc.
        """
        result = True
        for k in kwargs:
            v = kwargs[k]
            dv = d.get(k)
            if not self.match_value(k, dv, v):
                #print('*** matcher failed: %s, %r, %r' % (k, dv, v))
                result = False
                break
        return result

    def match_value(self, k, dv, v):
        """
        Try to match a single stored value (dv) with a supplied value (v).
        """
        if type(v) != type(dv):
            result = False
        elif type(dv) is not str or k not in self._partial_matches:
            result = (v == dv)
        else:
            result = dv.find(v) >= 0
        #if not result:
        #    print('*** matcher failed on %s: %r vs. %r' % (k, dv, v))
        return result

