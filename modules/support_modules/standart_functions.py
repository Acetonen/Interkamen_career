#!/usr/bin/env python3
"""Frequently using functions in modules classes."""

import sys
import os
import pickle
from modules.support_modules.absolyte_path_module import AbsolytePath


class BasicFunctions:
    """Frequently using functions in modules classes."""

    @classmethod
    def choise_from_list(cls, variants_list, none_option=False):
        """Chose variant from list."""
        sort_list = sorted(variants_list)
        for index, item in enumerate(sort_list, 1):
            print("\t[{}] - {}".format(index, item))
        while True:
            choise = input()
            if choise == '' and none_option:
                chosen_item = None
                break
            elif cls.check_number_in_range(choise, sort_list):
                chosen_item = sort_list[int(choise)-1]
                break
        return chosen_item

    @classmethod
    def check_number_in_range(cls, user_input, list_range):
        """Check is input a number in current range."""
        check_number = None
        if user_input.isdigit():
            check_number = int(user_input) in range(len(list_range)+1)
            if not check_number:
                print("\nВы должны ввести цифру в заданном диапазоне.\n")
        else:
            print("\nВы должны ввести ЦИФРУ.\n")
        return check_number

    @classmethod
    def confirm_deletion(cls, item):
        """Action conformation"""
        confirm = input(
            "Вы уверены что хотите удалить '{}'? Д/н: ".format(item))
        if confirm.lower() == 'д':
            confirm = True
            print("\033[91m'{}' - удален. \033[0m".format(item))
        else:
            confirm = False
            print("\nВы отменили удаление.\n")
        return confirm

    @classmethod
    def clear_screen(cls):
        """Clear shell screen"""
        if sys.platform[:3] == 'win':
            os.system('cls')
        else:
            os.system('clear')

    @classmethod
    def load_data(cls, data_path):
        """Load file from pickle"""
        if os.path.exists(data_path):
            with open(data_path, 'rb') as base_file:
                base = pickle.load(base_file)
        else:
            base = {}
        return base

    @classmethod
    def dump_data(cls, data_path, base_to_dump):
        """Dumb data to pickle."""
        with open(data_path, 'wb') as base_file:
            pickle.dump(base_to_dump, base_file)

    @classmethod
    def save_log_to_temp_file(cls, log):
        "Get detailed log for user actions."
        file_path = AbsolytePath('log.tmp').get_absolyte_path()
        with open(file_path, 'a', encoding='utf-8') as temp_file:
            temp_file.write(log)

    @classmethod
    def count_unzero_items(cls, items_list):
        """Count workers that haven't zero hours."""
        counter = 0
        for item in items_list:
            if items_list[item] != 0:
                counter += 1
        return counter
