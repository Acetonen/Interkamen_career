#!/usr/bin/env python3
"""Create backup of data files once a month."""

import shutil
import os
from datetime import date, datetime
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.support_modules.emailed import EmailSender
from modules.support_modules.standart_functions import BasicFunctions


DATA_PATH = AbsolytePath('').get_absolyte_path()
LOG_FILE_PATH = DATA_PATH[:-5] + 'backup/backup_log'


def make_backup(backup_log_list=[]):
    """Make backup file."""
    current_date = str(date.today())
    backup_path = 'backup/' + current_date
    shutil.make_archive(backup_path, 'zip', DATA_PATH)
    backup_log_list.append(current_date)
    BasicFunctions.dump_data(LOG_FILE_PATH, backup_log_list)
    print("\033[5m\033[1mBackup done.\033[0m")
    EmailSender().try_email(
        subject='Data backup',
        message='Data backup for ' + current_date,
        add_file=''.join([DATA_PATH[:-5], backup_path, '.zip'])
    )
    log_maden = True
    return log_maden


def check_last_backup_date():
    """Check last backup date"""
    log_maden = False
    if os.path.exists(LOG_FILE_PATH):
        backup_log_list = BasicFunctions.load_data(LOG_FILE_PATH)
        last_backup_date = backup_log_list[-1]
        last_data = datetime.strptime(last_backup_date.rstrip(), '%Y-%m-%d')
        delta = datetime.now() - last_data
        if delta.days > 30:
            log_maden = make_backup(backup_log_list)
    else:
        log_maden = make_backup()
    return log_maden
