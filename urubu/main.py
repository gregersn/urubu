# Copyright 2014 Jan Decaluwe
#
# This file is part of Urubu.
#
# Urubu is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Urubu is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Urubu.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import argparse

import os

from urubu import __version__
from urubu import project

from urubu._compat import socketserver  # , httpserver
from urubu.httphandler import AliasingHTTPRequestHandler

from urubu import watcher


class UrubuServer(socketserver.TCPServer):
    def __init__(self, base_path, server_address, handler):
        self.base_path = base_path
        super(self.__class__, self).__init__(server_address, handler)


def serve(baseurl, host='localhost', port=8000):
    """HTTP server straight from the docs."""
    # allow running this from the top level
    servedir = '.'
    if os.path.isdir('_build'):
        servedir = '_build'

    # local use, address reuse should be OK
    UrubuServer.allow_reuse_address = True
    handler = AliasingHTTPRequestHandler
    httpd = UrubuServer(servedir, (host, port), handler)
    httpd.baseurl = baseurl

    print("Serving {} at port {}".format(host, port))
    if httpd.baseurl:
        print("Using baseurl {}".format(httpd.baseurl))

    httpd.serve_forever()


def watch(baseurl, host='localhost', port=8000):
    print('start watch thread')
    observer = watcher.watch('.', project.build, None)
    try:
        serve(baseurl, host=host, port=port)
    except KeyboardInterrupt:
        print('Done serving')
        observer.stop()
        observer.join()


def main():
    parser = argparse.ArgumentParser(prog='python -m urubu')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('command', choices=['build',
                                            'serve', 'serveany',
                                            'watch'])
    args = parser.parse_args()
    if args.command == 'build':
        project.build()
    elif args.command == 'serve':
        proj = project.load()
        serve(proj.site['baseurl'])
    elif args.command == 'watch':
        proj = project.load()
        watch(proj.site['baseurl'])
    elif args.command == 'serveany':
        proj = project.load()
        serve(proj.site['baseurl'], host='')
