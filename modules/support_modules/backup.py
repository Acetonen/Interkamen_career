#!/usr/bin/env python3
"""Create backup of data files once a month."""

import shutil
import os
from datetime import date, datetime
from modules.support_modules.absolyte_path_module import AbsPath
from modules.support_modules.emailed import EmailSender
from modules.support_modules.standart_functions import BasicFunctions


DATA_PATH = AbsPath().get_path('data')
LOG_FILE_PATH = AbsPath().get_path('backup', 'backup_log')
EMPTY_LIST = []


def make_backup(backup_log_list=EMPTY_LIST):
    """Make backup file."""
    current_date = str(date.today())
    backup_path = os.path.join('backup', current_date)
    shutil.make_archive(backup_path, 'zip', DATA_PATH)
    backup_log_list.append(current_date)
    BasicFunctions.dump_data(LOG_FILE_PATH, backup_log_list)
    print("\033[5m\033[1mBackup done.\033[0m")
    unsucsesse = EmailSender().try_email(
        recivers='resivers list',
        subject='Data backup',
        message='Data backup for ' + current_date,
        add_file=AbsPath().get_path(backup_path) + '.zip',
    )
    if unsucsesse:
        print(unsucsesse)
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
