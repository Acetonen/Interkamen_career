#!/usr/bin/env python3
"""Frequently using functions in modules classes."""

import sys
import os
import pickle
from matplotlib import rcParams as window_parametrs
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

    @staticmethod
    def check_number_in_range(user_input, list_range):
        """Check is input a number in current range."""
        check_number = None
        if user_input.isdigit():
            check_number = int(user_input) in range(len(list_range)+1)
            if not check_number:
                print("\nВы должны ввести цифру в заданном диапазоне.\n")
        else:
            print("\nВы должны ввести ЦИФРУ.\n")
        return check_number

    @staticmethod
    def confirm_deletion(item):
        """Deletion confirmation"""
        confirm = input(
            "Вы уверены что хотите удалить '{}'? Д/н: ".format(item))
        if confirm.lower() == 'д':
            confirm = True
            print("\033[91m'{}' - удален. \033[0m".format(item))
        else:
            confirm = False
            print("\nВы отменили удаление.\n")
        return confirm

    @staticmethod
    def clear_screen():
        """Clear shell screen"""
        if sys.platform[:3] == 'win':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def load_data(data_path):
        """Load data from pickle"""
        if os.path.exists(data_path):
            with open(data_path, 'rb') as base_file:
                base = pickle.load(base_file)
        else:
            base = {}
        return base

    @staticmethod
    def dump_data(data_path, base_to_dump):
        """Dumb data to pickle."""
        with open(data_path, 'wb') as base_file:
            pickle.dump(base_to_dump, base_file)

    @staticmethod
    def save_log_to_temp_file(log):
        "Get detailed log for user actions."
        file_path = AbsolytePath('log.tmp').get_absolyte_path()
        with open(file_path, 'a', encoding='utf-8') as temp_file:
            temp_file.write(log)

    @staticmethod
    def count_unzero_items(items_list):
        """Count nonzero items."""
        counter = 0
        for item in items_list:
            if items_list[item] != 0:
                counter += 1
        return counter

    @staticmethod
    def make_windows_plot_param():
        """Make windows plot parametrs."""
        window_parametrs['figure.figsize'] = [22.0, 8.0]
        window_parametrs['figure.dpi'] = 100
        window_parametrs['savefig.dpi'] = 200
        window_parametrs['font.size'] = 12
        window_parametrs['legend.fontsize'] = 'large'
        window_parametrs['figure.titlesize'] = 'large'

    @classmethod
    def input_date(cls):
        """Input date."""
        check_date = False
        while not check_date:
            rep_date = input("Введите год и месяц формате 2018-01: ")
            if not rep_date or '-' not in rep_date:
                print("Неверный формат.")
                continue
            check_date = cls.check_date_format(rep_date)
        rep_date = list(map(int, rep_date.split('-')))
        rep_dict = {'year': rep_date[0], 'month': rep_date[1]}
        return rep_dict

    @staticmethod
    def check_date_format(rep_date):
        """Check if date format correct"""
        date_numbers = rep_date.split('-')
        correct = (rep_date[4] == '-' and
                   len(date_numbers) == 2 and
                   len(date_numbers[1]) == 2 and
                   date_numbers[0].isdigit() and
                   date_numbers[1].isdigit() and
                   int(date_numbers[1]) < 13 and
                   int(date_numbers[1]) > 0)
        return correct

    @staticmethod
    def check_date_in_dataframe(dataframe, rep_date):
        """
        Check if report allready exist.
        rep_date is a dictionary, that contain keys: year, month, day or shift.
        """
        if dataframe.empty:
            check = False
        elif len(rep_date) >= 3:
            tmp_check = []
            for key in rep_date:
                tmp_check.append((dataframe[key] == rep_date[key]))
            check = tmp_check[0]
            while tmp_check:
                check = check & tmp_check[0]
                tmp_check = tmp_check[1:]
            check = check.any()
        elif len(rep_date) == 2 and rep_date['month']:
            check_items = ((dataframe['year'] == rep_date['year']) &
                           (dataframe['month'] == rep_date['month']))
            if 'day' in dataframe[check_items]:
                avail_days = dataframe[check_items].day
                print("Имеющиеся отчеты: {}".format(sorted(set(avail_days))))
            check = check_items.any()
        elif (len(rep_date) == 1 or
              (len(rep_date) == 2 and not rep_date['month'])):
            check_items = dataframe['year'] == rep_date['year']
            check = (check_items).any()
            avail_months = dataframe[check_items].month
            print("Имеющиеся отчеты: {}".format(sorted(set(avail_months))))
        return check

    @staticmethod
    def float_input(msg=None, inp=None):
        """Input float with comma, not point."""
        if not inp:
            inp = input(msg)
        try:
            make_float = float(inp)
        except ValueError:
            inp = inp.replace(',', '.')
            make_float = float(inp)
            print("\033[91mЗапятая заменена на точку.\033[0m")
        return make_float

    @staticmethod
    def make_name_short(name):
        """Make short name."""
        name = name.split(' ')
        sh_name = name[0] + ' ' + name[1][0] + '.' + name[2][0] + '.'
        return sh_name
