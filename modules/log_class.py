#!/usr/bin/env python3
"""
This class provides to work with all logs.
Classes: Logs: 'upload_temp_file_log',
               'check_number_in_range',
               'choose_item',
               'confirm_deletion',
               'create_log',
               'delete_all_logs',
               'search_in_logs',
               'search_logs_by_item',
               'show_all_logs',
"""

import pickle
import os
from datetime import datetime
from modules.absolyte_path_module import AbsolytePath
from modules.users import Users


class Logs:
    """This class provides to work with all logs."""
    def __init__(self, data_file=AbsolytePath('logs_base')):

        self.data_file = data_file.get_absolyte_path()
        self.log_constructor = []
        self.log_list = {
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
            '[Наряд бригады]': 'edit report',
            'Создать отчет по буровым инструментам': 'create drill report'
            }

        self.search_list = list(self.log_list.keys())
        self.search_list.extend(Users().get_all_users_list())

    def _load_data(self):
        """Load file from pickle"""
        with open(self.data_file, 'rb') as logs_file:
            logs_base = pickle.load(logs_file)
        return logs_base

    def _dump_data(self, logs_base):
        """Dumb data to pickle."""
        with open(self.data_file, 'wb') as logs_file:
            pickle.dump(logs_base, logs_file)

    def create_log(self, user_login, user_action):
        """Create detailed log for action"""
        if user_action in self.log_list:
            self.log_constructor.append(user_login)
            self.log_constructor.append(self.log_list[user_action])
            self.upload_temp_file_log()
            current_time = str(datetime.now().replace(microsecond=0))
            logs_base = self._load_data()
            logs_base[current_time] = self.log_constructor
            self._dump_data(logs_base)
            self.log_constructor = self.log_constructor[:]

    def upload_temp_file_log(self):
        """Read detailed user log from temp file"""
        file_path = AbsolytePath('log.tmp').get_absolyte_path()
        if os.path.exists(file_path):
            with open(file_path, 'r') as temp_file:
                detail_log = temp_file.readlines()
                self.log_constructor.extend(detail_log)
            os.remove(file_path)

    def show_all_logs(self):
        """show_all_logs"""
        logs_base = self._load_data()
        for log in sorted(logs_base):
            print(log, ' '.join(logs_base[log]))

    def search_in_logs(self):
        """Search in logs."""
        print("Choose item to search:")
        self.search_logs_by_item(self.choose_item())

    def choose_item(self):
        """Chose item to search"""
        item = None
        for index, option in enumerate(self.search_list, 1):
            print("[{}] - {}".format(index, option))
        choose = input("\nInput action to search:  ")
        if self.check_number_in_range(choose, len(self.search_list)):
            item = self.search_list[int(choose)-1]
        return item

    def search_logs_by_item(self, search_item):
        """Search particular information from logs."""
        print(search_item)
        search_list = {}
        logs_base = self._load_data()
        for log in logs_base:
            if search_item in logs_base[log]:
                search_list[log] = logs_base[log]
        for log in sorted(search_list):
            print(log, ' '.join(search_list[log]))
        if not search_list:
            print("No such item in logs.")

    @classmethod
    def check_number_in_range(cls, user_input, list_range):
        """Check is input a number in current range."""
        check_number = None
        if user_input.isdigit():
            check_number = int(user_input) in range(list_range+1)
            if not check_number:
                print("\nYou must input number IN CURRENT RANGE.\n")
        else:
            print("\nYou must input NUMBER.\n")
        return check_number

    def delete_all_logs(self):
        """delete logs for all users"""
        if self.confirm_deletion('all logs'):
            logs_base = {}
            self._dump_data(logs_base)

    @classmethod
    def confirm_deletion(cls, logs):
        """Action conformation"""
        confirm = input(
            "Are you shure you want delete '{}'? Y/n: ".format(logs))
        if confirm.lower() == 'y':
            confirm = True
            print("\033[91m '{}' - deleted. \033[0m".format(logs))
        else:
            confirm = False
            print("\nYou skip deletion.\n")
        return confirm
