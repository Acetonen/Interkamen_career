#!/usr/bin/env python3
"""
This class provides to work with all logs.
Classes: Logs: 'upload_temp_file_log',
               'choose_item',
               'delete_all_logs',
               'search_in_logs',
               '_search_logs_by_item',
               'show_all_logs',
"""

import os
from datetime import datetime

from modules.administration.users import Users

from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.support_modules.emailed import EmailSender


class Logs(BasicFunctions):
    """This class provides to work with all logs."""

    data_path = AbsolytePath('logs_base').get_absolyte_path()
    log_list = {
        'enter program': '\033[94m enter program \033[0m',
        'exit program': '\033[93m exit program \033[0m',
        'create new user': 'create new user',
        'edit user': 'edit user',
        'search in logs': 'search in logs',
        'delete all logs': 'delete all logs',
        'change self password': 'change self password',
        'add worker': 'add worker',
        'edit worker': 'edit worker',
        'upd company structure': 'upd company structure',
        'Новый работник': 'new worker',
        'Редактировать работника': 'edit worker',
        "Backup done.": '\033[1mbackup done.\033[0m',
        'Вернуть работника из архива': 'restore worker from archive',
        'Редактировать табель': 'edit report',
        'Создать табель добычной бригады': 'create new report',
        'Наряд бригады': 'edit report',
        'Создать отчет по буровым инструментам': 'create drill report',
        'Бригадиры, окладники, бурильщики': 'edit',
        'Создать отчет по ремонтам': 'create mechanics report'
        }
    notification_list = [
        'create drill report',
        '-->',
        'create new user',
        'create new report'
    ]

    def __init__(self):
        self.log_base = super().load_data(self.data_path)
        self.search_list = list(self.log_list.keys())
        self.search_list.extend(Users().get_all_users_list())

    @classmethod
    def upload_temp_file_log(cls, log_constructor):
        """Read detailed user log from temp file"""
        file_path = AbsolytePath('log.tmp').get_absolyte_path()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as temp_file:
                detail_log = temp_file.readlines()
                log_constructor.extend(detail_log)
            os.remove(file_path)

    def _send_mail_notification(self, log_constructor, subject, message):
        """Send notification email if action in notification list."""
        for event in self.notification_list:
            if event in ' '.join(log_constructor):
                EmailSender().try_email(subject=subject, message=message)

    def _search_logs_by_item(self, search_item):
        """Search particular information from logs."""
        print(search_item)
        search_list = {}
        for log in self.log_base:
            if search_item in self.log_base[log]:
                search_list[log] = self.log_base[log]
        for log in sorted(search_list):
            print(log, ' '.join(search_list[log]))
        if not search_list:
            print("No such item in logs.")

    def create_log(self, user_login, user_action):
        """Create detailed log for action"""
        if user_action in self.log_list:
            log_constructor = []
            log_constructor.append(user_login)
            log_constructor.append(self.log_list[user_action])
            self.upload_temp_file_log(log_constructor)
            current_time = str(datetime.now().replace(microsecond=0))
            self.log_base[current_time] = log_constructor
            super().dump_data(self.data_path, self.log_base)
            self._send_mail_notification(
                log_constructor,
                'InterKamen program notification.',
                ' '.join(log_constructor))

    def show_all_logs(self):
        """show_all_logs"""
        for log in sorted(self.log_base):
            print(log, ' '.join(self.log_base[log]))

    def search_in_logs(self):
        """Search in logs."""
        print("Choose item to search:")
        self._search_logs_by_item(self.choose_item())

    def choose_item(self):
        """Chose item to search"""
        item = None
        for index, option in enumerate(self.search_list, 1):
            print("[{}] - {}".format(index, option))
        choose = input("\nInput action to search:  ")
        if super().check_number_in_range(choose, self.search_list):
            item = self.search_list[int(choose)-1]
        return item

    def delete_all_logs(self):
        """delete logs for all users"""
        if super().confirm_deletion('all logs'):
            logs_base = {}
            super().dump_data(self.data_path, logs_base)
