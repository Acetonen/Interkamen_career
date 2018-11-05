#!/usr/bin/env python3
"""Make absolyte path to working with database on different platforms."""

import sys
import os


def make_absolyte_path(relative_path):
    """Make absolyte path of database file."""
    script_name = sys.argv[0]
    script_path = os.path.dirname(script_name)
    absolute_path = os.path.abspath(script_path)
    os_path = os.path.join(absolute_path, *relative_path)
    return os_path


USERS_PATH = make_absolyte_path(['data', 'users_base'])
