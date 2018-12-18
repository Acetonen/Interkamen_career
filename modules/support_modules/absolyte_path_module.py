#!/usr/bin/env python3
"""
Make absolyte path to working with database on different platforms.

Classes: AbsPath: '_make_absolyte_path',
                  'get_path'

"""

import sys
import os


class AbsPath:
    """Make absolyte path to working with database on different platforms."""

    @classmethod
    def _make_absolyte_path(cls, up_root=False):
        """
        Make absolyte path to root program directory,
        or upper directory if up_root option is True.
        Return path string.
        """
        script_name = sys.argv[0]  # Find screept name.
        script_path = os.path.dirname(script_name)  # Find screept path.
        absolute_path = os.path.abspath(script_path)  # Find abs path.
        if up_root:
            absolute_path = os.path.split(absolute_path)[0]  # Make up_root.
        return absolute_path

    @classmethod
    def get_path(cls, *paths, up_root=False):
        """Get absolyte path to data file"""
        absolute_path = cls._make_absolyte_path(up_root)
        file_path = os.path.join(absolute_path, *paths)
        return file_path
