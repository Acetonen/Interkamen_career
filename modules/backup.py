#!usr/bin/env python3
"""Create backup of data files once a month."""

import shutil
import os
from datetime import date, datetime
from modules.absolyte_path_module import AbsolytePath


def make_backup():
    """Make backup file."""
    current_date = str(date.today())
    data_path = AbsolytePath('').get_absolyte_path()
    shutil.make_archive(current_date, 'zip', data_path)
    log_file_name = AbsolytePath('backup_log.txt').get_absolyte_path()
    with open(log_file_name, 'a') as backup_log:
        backup_log.write(current_date)
    backup_log.close()


def check_last_backup_date():
    """Check last backup date"""
    log_file_name = AbsolytePath('backup_log.txt').get_absolyte_path()
    backup_log = None
    if os.path.exists(log_file_name):
        with open(log_file_name, 'r') as backup_log:
            last_backup_date = backup_log.readlines()[-1]
        last_data = datetime.strptime(last_backup_date[:-1], '%Y-%m-%d')
        delta = datetime.now() - last_data
        if delta.days > 30:
            backup_log = "\033[5m\033[1mBackup done.\033[0m"
            print(backup_log)
            make_backup()
    else:
        backup_log = "\033[5m\033[1mBackup done.\033[0m"
        print(backup_log)
        make_backup()
    return backup_log
