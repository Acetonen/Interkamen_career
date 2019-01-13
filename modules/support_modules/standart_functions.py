#!/usr/bin/env python3.7
"""Frequently using functions in modules classes."""

from __future__ import annotations

import sys
import os
import pickle
import time
import re
import calendar as cl
from pathlib import Path, PurePath
from typing import Set, Dict, List
import bcrypt
from matplotlib import rcParams as window_parametrs
from modules.support_modules.custom_exceptions import MainMenu


PROGRAM_PATH = Path(sys.argv[0]).resolve().parent


class BasicFunctions:
    """Frequently using functions in modules classes."""

    @classmethod
    def stupid_timer(cls, count: int, title: str):
        """Stupid timer."""
        cls.clear_screen()
        print(title)
        time.sleep(3)
        for sec in range(count):
            cls.clear_screen()
            print(count - sec)
            time.sleep(1)
        cls.clear_screen()
        print("GO!")
        time.sleep(1)

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
    def input_date(cls) -> Dict[str, int]:
        """Input date."""
        check_date = False
        while not check_date:
            rep_date = input("[ENTER] - выйти."
                             "\nВведите год и месяц формате 2018-01: ")
            if not rep_date:
                raise MainMenu
            if '-' not in rep_date:
                print("Неверный формат.")
                continue
            check_date = cls.check_date_format(rep_date)
        rep_date = list(map(int, rep_date.split('-')))
        rep_dict = {'year': rep_date[0], 'month': rep_date[1]}
        return rep_dict

    @classmethod
    def check_date_in_dataframe(cls, dataframe,
                                rep_date: Dict[str, int]) -> bool:
        """
        Check if report allready exist in DataFrame
        rep_date can contain keys: year, month, day or shift (optionaly)
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
                avail_days = sorted(set(avail_days))
                print(
                    "Имеющиеся отчеты:\n\t",
                    cls.colorise_avaliable_date(
                        rep_date['year'],
                        rep_date['month'],
                        avail_days
                    )
                )
            check = check_items.any()
        elif (len(rep_date) == 1 or
              (len(rep_date) == 2 and not rep_date['month'])):
            check_items = dataframe['year'] == rep_date['year']
            check = (check_items).any()
            avail_months = dataframe[check_items].month
            print("Имеющиеся отчеты: {}".format(sorted(set(avail_months))))

        return check

    @classmethod
    def check_correct_email(cls) -> str:
        """Change e-mail adress."""
        match = True
        new_email = None
        while match:
            new_email = input("[ENTER] - cansel."
                              "\nenter new email: ")
            if not new_email:
                break
            match = re.match(
                r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                new_email
            )
            cls.clear_screen()
            if not match:
                print('\033[91mbad Syntax in\033[0m ' + new_email)
            else:
                break
        return new_email

    @classmethod
    def confirm_deletion_decorator(cls, func):
        """Decorator to confirm item deletion."""
        def wrapper(*args, **kwargs) -> bool:
            condition, item_name = func(*args, **kwargs)
            if condition:
                deleted = cls.confirm_deletion(item_name)
            else:
                deleted = False
            return deleted
        return wrapper

    @staticmethod
    def check_date_format(rep_date: str) -> bool:
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
    def colorise_avaliable_date(year: int,
                                month: int,
                                av_days: Set[float]) -> str:
        """Colorise avaliable date."""
        cal = cl.TextCalendar()
        month_prnt = cal.formatmonth(year, month).__repr__()
        month_prnt = month_prnt.replace(str(year), '')
        month_prnt = month_prnt.replace("'", '')
        for day in av_days:
            st_day = str(int(day))
            if len(st_day) == 1:
                st_day = ' ' + st_day
            month_prnt = month_prnt.replace(st_day,
                                            f'\033[91m{st_day}\033[0m', 1)
        month_prnt = month_prnt.replace('\\n', '\n\t')
        return month_prnt

    @staticmethod
    def float_input(msg: str = None, inp: str = None):
        """Input float with comma, not point."""
        if not inp:
            inp = input(msg)
            if not inp:
                return 0
        try:
            make_float = float(inp)
        except ValueError:
            inp = inp.replace(',', '.')
            make_float = float(inp)
            print("\033[91mЗапятая заменена на точку.\033[0m")
        return make_float

    @staticmethod
    def make_name_short(name: str):
        """Make short name for workers or users
        Ковалев Антон Викторович -> Ковалев А.В."""
        name = name.split(' ')
        sh_name = name[0] + ' ' + name[1][0] + '.' + name[2][0] + '.'
        return sh_name

    @staticmethod
    def get_root_path() -> PurePath:
        """
        Make absolyte path to root program directory.
        """
        return PROGRAM_PATH

    @staticmethod
    def check_login_password(users_base, login, password):
        """Check user login and password."""
        sucsesse_login = False
        password = password.encode('utf-8')
        if (login in users_base and
                bcrypt.checkpw(password, users_base[login].password)):
            sucsesse_login = True
        else:
            print("Неправильные имя пользователя или пароль.")
        return sucsesse_login

    @staticmethod
    def check_number_in_range(user_input, list_range: List):
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
        """Deletion confirmation."""
        confirm = input(
            "Вы уверены что хотите удалить '{}'? Y/N: ".format(item))
        if confirm.lower() == 'y':
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
    def load_data(data_path: PurePath):
        """Load data from pickle"""
        if data_path.exists():
            with open(data_path, 'rb') as base_file:
                base = pickle.load(base_file)
        else:
            base = {}
        return base

    @staticmethod
    def dump_data(data_path: PurePath, base_to_dump):
        """Dumb data to pickle."""
        with open(data_path, 'wb') as base_file:
            pickle.dump(base_to_dump, base_file)

    @staticmethod
    def count_unzero_items(items_list):
        """Count nonzero items in list."""
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
