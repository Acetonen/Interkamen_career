#!usr/bin/env python3
"""
This module work with User class and access.

Classes: User: get_name(self)
               get_access(self)
               bump_log(self)
               clean_log(self)
               print_log(self, action)
               change_password(self)

Functions: edit_user(): change_user_access()
                        change_user_name()
                        change_user_password()
                        delete_user()
           try_to_enter_program()
           create_new_user()
           choose_access()
           check_is_it_number_in_range(user_input, list_range)
           confirm_deletion(action)
           show_all_users()
           choose_user_from_base()
           check_only_admin()

Constants: DETAIL_LOG
"""


import getpass
import shelve
from datetime import datetime
from modules import access_options
from modules.absolyte_path_module import USERS_PATH


DETAIL_LOG = []


class User():
    """User warking with program."""
    def __init__(self, name, access, login, password):
        self.name = name
        self.access = access
        self.login = login
        self.password = password
        self.log = {}

    def get_name(self):
        """Return user name"""
        return self.name

    def get_access(self):
        """Return user access"""
        return self.access

    def bump_log(self, action):
        """Bump log information to user log"""
        current_time = datetime.now().replace(microsecond=0)
        self.log[current_time] = self.login + ' ' + action

    def clean_log(self):
        """Clean log information"""
        confirm = input("Are you shure to clean log? Y/n: ")
        if confirm.lower() == 'y':
            self.log = {}
            print("\033[91m log - deleted. \033[0m")
        else:
            print("\nYou skip deletion.\n")

    def print_log(self):
        """Print user log file"""
        for time in sorted(self.log):
            print(time, self.log[time])

    def change_password(self):
        """Changing password"""
        old_password = input("Введите старый пароль: ")
        if old_password == self.password:
            new_password = getpass.getpass("Введите новый пароль: ")
            repeat_password = getpass.getpass("Повторите новый пароль: ")
            if new_password == repeat_password:
                self.password = new_password
                print("Новый пароль сохранен.")
            else:
                print("Введенные пароли не совпадают.")
        else:
            print("Неправильный пароль.")

    def __str__(self):
        return (
            "User - {}\nlogin:   {}\npassword: {}\naccess level: {}\n".format(
                self.name, self.login, self.password, self.access))


def edit_user():
    """Change user parametrs."""

    def change_user_access():
        """Change_user_access"""
        new_accesse = choose_access()
        temp_user.access = new_accesse
        DETAIL_LOG.append(' change access')

    def change_user_name():
        """Change user name"""
        new_name = input("Input new user name: ")
        temp_user.name = new_name
        DETAIL_LOG.append(' change name')

    def change_user_password():
        """Change user password"""
        new_password = input("Input new user password: ")
        temp_user.password = new_password
        DETAIL_LOG.append(' change password')

    def delete_user():
        """Delete user from database"""
        if check_only_admin():
            print("If 'admin' user alone you can't delete him.")
        elif confirm_deletion(choosen_user):
            users_base.pop(choosen_user, None)
            users_base.close()
        nonlocal temp_user
        temp_user = None

    choosen_user = choose_user_from_base()
    if choosen_user:
        DETAIL_LOG.append(choosen_user)
    users_base = shelve.open(USERS_PATH)
    while choosen_user:
        temp_user = users_base[choosen_user]
        print()
        print(users_base[choosen_user])
        action_name_list = {'a': 'change user access',
                            'n': 'change user name',
                            'p': 'change user password',
                            'd': 'delete user',
                            'x': 'exit edition'}
        action_list = {'a': change_user_access,
                       'n': change_user_name,
                       'p': change_user_password,
                       'd': delete_user,
                       'x': 'break'}
        for action in sorted(action_list):
            print("[{}] {}".format(action, action_name_list[action]))

        choosen_action = input("Choose action: ")
        print()
        if choosen_action in ['x', '']:
            break
        action_list[choosen_action]()
        if not temp_user:
            break
        users_base[choosen_user] = temp_user
    users_base.close()


def choose_user_from_base():
    """Chose user from user base"""
    users_base = shelve.open(USERS_PATH)
    for index, login in enumerate(sorted(users_base), 1):
        print("[{}] {}".format(index, login))
    choose = input("Input number of user to edit: ")
    if check_is_it_number_in_range(choose, len(users_base)):
        user = sorted(users_base)[int(choose)-1]
    else:
        user = None
    users_base.close()
    return user


def show_all_users():
    """Showing all users in base"""
    with shelve.open(USERS_PATH) as users_base:
        for login in users_base:
            print(users_base[login])


def create_new_user():
    """Create new user and save him in databese"""
    users_base = shelve.open(USERS_PATH)
    user_name = input("Input username: ")
    while True:
        user_login = input("Input login: ")
        if user_login in users_base:
            print("Login alredy exist, try enother.")
        else:
            break
    user_password = input("Input password: ")
    user_access = choose_access()
    users_base[user_login] = User(user_name, user_access,
                                  user_login, user_password)
    output = "\033[92m User '{}' created. \033[0m".format(user_name)
    print(output)
    DETAIL_LOG.append(output)
    users_base.close()


def choose_access():
    """Choosing access from access list"""
    access_list = access_options.ACCESS_LIST
    for index, name in enumerate(access_list[1:], 1):
        print("[{}] {}".format(index, name))
    while True:
        choose = input("Choose access by number: ")
        if check_is_it_number_in_range(choose, len(access_list)-1):
            chosen_access = access_list[int(choose)]
            break
    return chosen_access


def try_to_enter_program():
    """
    Take user login/password input and return current user privilege
    """
    user_in = None
    login = input("Введите имя пользователя: ")
    users_base = shelve.open(USERS_PATH)
    if login in users_base:
        while True:
            password = getpass.getpass("Введите пароль: ")
            if users_base[login].password == password:
                user_in = users_base[login]
                break
            else:
                print("Неправильный пароль, попробуйте еще раз.")
    else:
        print("Такого пользователя не существует.")
    users_base.close()
    return user_in


def check_is_it_number_in_range(user_input, list_range):
    """Check is input a number in current range."""
    check_number = None
    if user_input.isdigit():
        check_number = int(user_input) in range(list_range+1)
        if not check_number:
            print("\nYou must input number IN CURRENT RANGE.\n")
    else:
        print("\nYou must input NUMBER.\n")
    return check_number


def confirm_deletion(action):
    """Action conformation"""
    confirm = input(
        "Are you shure to delete '{}'? Y/n: ".format(action))
    if confirm.lower() == 'y':
        confirm = True
        output = "\033[91m '{}' - deleted. \033[0m".format(action)
        print(output)
        DETAIL_LOG.append(output)
    else:
        confirm = False
        print("\nYou skip deletion.\n")
    return confirm


def check_only_admin():
    """Check if admin user only one in base"""
    check = False
    admin_counter = 0
    with shelve.open(USERS_PATH) as users_base:
        for login in users_base:
            if users_base[login].access == 'admin':
                admin_counter += 1
    if admin_counter == 1:
        check = True
    return check
