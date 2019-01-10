#!/usr/bin/env python3
"""Create backup of data files once a month."""


import shutil
from pathlib import Path
from datetime import date, datetime
from modules.support_modules.emailed import EmailSender
from modules.administration.logger_cfg import Logs
from modules.support_modules.standart_functions import BasicFunctions as BasF


LOGGER = Logs().give_logger(__name__)

DATA_PATH = BasF.get_root_path() / 'data'
LOG_FILE_PATH = BasF.get_root_path() / 'backup' / 'backup_log'
EMPTY_LIST = []


def make_backup(user, backup_log_list=EMPTY_LIST, event=None):
    """Make backup file."""
    current_date = str(date.today())
    backup_path = Path('backup') / current_date
    shutil.make_archive(backup_path, 'zip', DATA_PATH)
    backup_log_list.append(current_date)
    BasF.dump_data(LOG_FILE_PATH, backup_log_list)
    LOGGER.warning(f"User '{user['login']}' Make backup.")
    unsucsesse = EmailSender().try_email(
        recivers='resivers list',
        subject='Data backup',
        message='Data backup for ' + current_date,
        add_file=(
            BasF.get_root_path().joinpath(backup_path).with_suffix('.zip')),
    )
    if event:
        event.wait()
    print("\033[5m\033[1mBackup done.\033[0m")
    if unsucsesse:
        print(unsucsesse)


def check_last_backup_date(user, event=None):
    """Check last backup date"""
    if LOG_FILE_PATH.exists():
        backup_log_list = BasF.load_data(LOG_FILE_PATH)
        last_backup_date = backup_log_list[-1]
        last_data = datetime.strptime(last_backup_date.rstrip(), '%Y-%m-%d')
        delta = datetime.now() - last_data
        if delta.days > 30:
            make_backup(user, backup_log_list, event=event)
    else:
        make_backup(user, event=event)
