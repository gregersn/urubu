# Copyright 2017 Greger Stolt Nilsen
#
# watcher.py is a module for watching a folder, invoking commands on change.
#
# watcher.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# watcher.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with watcher.py.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def watch(folder, callback, arguments):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt():
        observer.stop()
    observer.join()


def main():
    watch('.', None, None)


if __name__ == '__main__':
    main()
