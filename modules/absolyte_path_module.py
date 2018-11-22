#!/usr/bin/env python3
"""
Make absolyte path to working with database on different platforms.

Classes: AbsolytePath: 'make_absolyte_path',
                       'get_absolyte_path'

"""

import sys
import os


class AbsolytePath:
    """Make absolyte path to working with database on different platforms."""
    def __init__(self, file_name):
        self.absolute_path = self.make_absolyte_path(['data', file_name])

    @classmethod
    def make_absolyte_path(cls, relative_path):
        """Make absolyte path of database file."""
        script_name = sys.argv[0]
        script_path = os.path.dirname(script_name)
        absolute_path = os.path.abspath(script_path)
        os_path = os.path.join(absolute_path, *relative_path)
        return os_path

    def get_absolyte_path(self):
        """Get absolyte path to data file"""
        return self.absolute_path
