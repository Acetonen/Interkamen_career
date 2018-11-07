#!usr/bin/env python3
"""
This class provides to work with all logs.
Classes: Logs: 'add_read_temp_file_log',
               'check_number_in_range',
               'choose_item',
               'confirm_deletion',
               'create_log',
               'delete_all_logs',
               'search_in_logs',
               'search_logs_by_item',
               'show_all_logs'
"""

import shelve
import os
from datetime import datetime
from modules.absolyte_path_module import AbsolytePath
from modules.users import Users


class Logs:
    """This class provides to work with all logs."""
    def __init__(self, data_file=AbsolytePath('logs_base')):

        self.data_file = data_file.get_absolyte_path()
        self.log_constructor = []
        self.access_list = ['', 'admin', 'master', 'mechanics']
        self.log_list = {'enter': '\033[94m enter program \033[0m',
                         'в': '\033[93m exit program \033[0m',
                         'c': 'create new user',
                         'e': 'edit user',
                         's': 'show all users',
                         'п': 'change password',
                         'l': 'search in logs',
                         'a': 'show all users logs',
                         'w': 'delete logs from all useers',
                         'м': 'Показать меню программы'}

        self.search_list = [value for key, value in self.log_list.items()]
        self.search_list.extend(Users().get_all_users_list())

    def create_log(self, user_login, user_action):
        """Create detailed log for action"""
        current_time = str(datetime.now().replace(microsecond=0))
        self.log_constructor.append(user_login)  # User login
        self.log_constructor.append(self.log_list[user_action])  # User action
        self.add_read_temp_file_log()
        with shelve.open(self.data_file) as logs_base:
            logs_base[current_time] = self.log_constructor
        self.log_constructor = self.log_constructor[:]

    def add_read_temp_file_log(self):
        """Read detailed user log from temp file"""
        file_path = AbsolytePath('log.tmp').get_absolyte_path()
        if os.path.exists(file_path):
            with open(file_path, 'r') as temp_file:
                detail_log = temp_file.readlines()
                self.log_constructor.extend(detail_log)
            os.remove(file_path)

    def show_all_logs(self):
        """show_all_logs"""
        with shelve.open(self.data_file) as logs_base:
            for log in sorted(logs_base):
                print(log, ' '.join(logs_base[log]))

    def search_in_logs(self):
        """Search in logs."""
        print("Choose item to search:")
        self.search_logs_by_item(self.choose_item())

    def choose_item(self):
        """Chose item for search"""
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
        users_base = shelve.open(self.data_file)
        for log in users_base:
            if search_item in users_base[log]:
                search_list[log] = users_base[log]
        users_base.close()
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
            with shelve.open(self.data_file) as logs_base:
                logs_base.clear()

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