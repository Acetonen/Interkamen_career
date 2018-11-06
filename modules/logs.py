#!usr/bin/env python3
"""
This module provide working with program logs

Functions: search_in_logs(): choose_item()
                             search_logs_by_item(search_item)
           show_all_logs()
           create_log(current_user, user_choise)
"""

import shelve
from modules.absolyte_path_module import USERS_PATH
from modules import access_options, users


def search_in_logs():
    """Search in logs."""

    def choose_item():
        """Chose item for search"""
        search_list = [value for key, value in access_options.LOG_LIST.items()]
        for index, option in enumerate(search_list, 1):
            print("[{}] - {}".format(index, option))
        choose = input("\nInput action to search:  ")
        if users.check_is_it_number_in_range(choose, len(search_list)):
            item = search_list[int(choose)-1]
        return item

    def search_logs_by_item(search_item):
        """Search particular information from logs."""
        print(search_item)
        search_list = {}
        users_base = shelve.open(USERS_PATH)
        for user in users_base:
            for log in users_base[user].log:
                if search_item in users_base[user].log[log]:
                    search_list[log] = users_base[user].log[log]
        users_base.close()
        for log in sorted(search_list):
            print(log, search_list[log])

    search_logs_by_item(choose_item())


def show_all_logs():
    """show_all_logs"""
    log_list = {}
    with shelve.open(USERS_PATH) as users_base:
        for user in users_base:
            for log in users_base[user].log:
                log_list.update(users_base[user].log)
    for log in sorted(log_list):
        print(log, log_list[log])


def create_log(current_user, user_choise):
    """Create detailed log for action"""
    log = (
        access_options.LOG_LIST[user_choise] + ' ' + ''.join(users.DETAIL_LOG))
    current_user.bump_log(log)
    del users.DETAIL_LOG[:]


def delete_all_logs():
    """delete logs for all users"""
    if users.confirm_deletion('all logs'):
        users_base = shelve.open(USERS_PATH)
        for user in users_base:
            temp_user = users_base[user]
            temp_user.clean_log()
            users_base[user] = temp_user
        users_base.close()
