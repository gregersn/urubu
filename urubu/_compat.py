# -*- coding: utf-8 -*-
"""
    jinja2._compat
    ~~~~~~~~~~~~~~

    Some py2/py3 compatibility support based on a stripped down
    version of six so we don't have to depend on a specific version
    of it.

    :copyright: Copyright 2013 by the Jinja team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import sys

PY2 = sys.version_info[0] == 2
PYPY = hasattr(sys, 'pypy_translation_info')


def _identity(x):
    return x


if not PY2:
    unichr = chr
    range_type = range
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    def iterkeys(d):
        return iter(d.keys())

    def itervalues(d):
        return iter(d.values())

    def iteritems(d):
        return iter(d.items())

    ifilter = filter
    imap = map
    izip = zip
    intern = sys.intern

    import socketserver
    import http.server as httpserver

else:
    unichr = unichr
    text_type = unicode  # noqa
    range_type = xrange  # noqa
    string_types = (str, unicode)  # noqa
    integer_types = (int, long)  # noqa

    def iterkeys(d):
        return d.iterkeys()

    def itervalues(d):
        return d.itervalues()

    def iteritems(d):
        return d.iteritems()

    from itertools import imap, izip, ifilter  # noqa
    intern = intern

    import SocketServer as socketserver  # noqa
    import SimpleHTTPServer as httpserver  # noqa