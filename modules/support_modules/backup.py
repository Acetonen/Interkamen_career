#!/usr/bin/env python3
"""Create backup of data files once a month."""

import shutil
import os
from datetime import date, datetime
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.support_modules.emailed import EmailSender


def make_backup():
    """Make backup file."""
    current_date = str(date.today())
    backup_path = 'backup/' + current_date
    data_path = AbsolytePath('').get_absolyte_path()
    shutil.make_archive(backup_path, 'zip', data_path)
    log_file_name = 'backup/backup_log.txt'
    with open(log_file_name, 'a', encoding='utf-8') as backup_log:
        backup_log.write(current_date)
    backup_log.close()
    EmailSender().try_email(
        ''.join([data_path[:-5], backup_path, '.zip']),
        'Data backup',
        'Data backup for ' + current_date)


def check_last_backup_date():
    """Check last backup date"""
    log_file_name = 'backup/backup_log.txt'
    log_maden = False
    if os.path.exists(log_file_name):
        with open(log_file_name, 'r') as backup_log:
            last_backup_date = backup_log.readlines()[-1]
        last_data = datetime.strptime(last_backup_date[:-1], '%Y-%m-%d')
        delta = datetime.now() - last_data
        if delta.days > 30:
            print("\033[5m\033[1mBackup done.\033[0m")
            make_backup()
            log_maden = True
    else:
        print("\033[5m\033[1mBackup done.\033[0m")
        make_backup()
        log_maden = True
    return log_maden
