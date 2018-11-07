#!usr/bin/env python3
"""
This module work with User class and access.

Classes: User: 'change_user_access',
               'change_user_name',
               'change_user_password',
               'check_number_in_range',
               'check_only_admin',
               'choose_access',
               'choose_user_from_base',
               'confirm_deletion',
               'create_new_user',
               'delete_user',
               'edit_user',
               'get_all_users_list',
               'save_log_to_temp_file',
               'print_all_users',
               'print_user',
               'sync_user',
               'try_to_enter_program'
"""


import getpass
import shelve
from modules.absolyte_path_module import AbsolytePath


class Users:
    """Users warking with program."""
    def __init__(self, data_file=AbsolytePath('users_base')):

        self.data_file = data_file.get_absolyte_path()
        self.access_list = ['', 'admin', 'master', 'mechanics']
        with shelve.open(self.data_file) as users_base:
            self.all_users_list = [user for user in users_base]

    def create_new_user(self):
        """Create new user and save him in databese"""
        name = input("Input username: ")
        users_base = shelve.open(self.data_file)
        while True:
            login = input("Input login: ")
            if login in users_base:
                print("Login alredy exist, try enother.")
            else:
                break
        password = input("Input password: ")
        access = self.choose_access()
        users_base = shelve.open(self.data_file)
        users_base[login] = {'login': login,
                             'name': name,
                             'accesse': access,
                             'password': password}
        log = f"\033[92m user '{login}' created. \033[0m"
        print(log)
        self.save_log_to_temp_file(log)
        users_base.close()

    def choose_access(self):
        """Choosing access from access list"""
        for index, name in enumerate(self.access_list[1:], 1):
            print("[{}] {}".format(index, name))
        while True:
            choose = input("Choose access by number: ")
            if self.check_number_in_range(choose, len(self.access_list)-1):
                chosen_access = self.access_list[int(choose)]
                break
        return chosen_access

    def edit_user(self):
        """Change user parametrs."""

        choosen_user = self.choose_user_from_base()
        if choosen_user:
            self.save_log_to_temp_file(choosen_user)
        users_base = shelve.open(self.data_file)
        while choosen_user:
            temp_user = users_base[choosen_user]
            print()
            self.print_user(users_base[choosen_user])
            user_name_list = {'a': 'change user access',
                              'n': 'change user name',
                              'p': 'change user password',
                              'd': 'delete user',
                              'x': 'exit edition'}
            user_list = {'a': self.change_user_access,
                         'n': self.change_user_name,
                         'p': self.change_user_password,
                         'd': self.delete_user,
                         'x': 'break'}
            for user in sorted(user_list):
                print("[{}] {}".format(user, user_name_list[user]))

            choosen_action = input("Choose action: ")
            print()
            if choosen_action not in user_list:
                print("\nNo such option.\n")
                continue
            if choosen_action in ['x', '']:
                break
            user_deleted = user_list[choosen_action](temp_user)
            if user_deleted:
                break
            users_base[choosen_user] = temp_user
        users_base.close()

    def delete_user(self, user):
        """Delete user from database"""
        user_deleted = False
        if user['accesse'] == 'admin' and self.check_only_admin():
            print("If 'admin' user alone you can't delete him.")
        elif self.confirm_deletion(user['login']):
            with shelve.open(self.data_file) as users_base:
                users_base.pop(user['login'], None)
            user_deleted = True
        return user_deleted

    def check_only_admin(self):
        """Check if admin user only one in base"""
        check = False
        admin_counter = 0
        with shelve.open(self.data_file) as users_base:
            for login in users_base:
                if users_base[login]['accesse'] == 'admin':
                    admin_counter += 1
        if admin_counter == 1:
            check = True
        return check

    def confirm_deletion(self, user_login):
        """Action conformation"""
        confirm = input(
            "Are you shure you want delete '{}'? Y/n: ".format(user_login))
        if confirm.lower() == 'y':
            confirm = True
            log = "\033[91m user '{}' - deleted. \033[0m".format(user_login)
            print(log)
            self.save_log_to_temp_file(log)
        else:
            confirm = False
            print("\nYou skip deletion.\n")
        return confirm

    def change_user_access(self, user):
        """Change_user_access"""
        new_accesse = self.choose_access()
        user['accesse'] = new_accesse
        self.save_log_to_temp_file(' change access')

    def change_user_name(self, user):
        """Change user name"""
        new_name = input("Input new user name: ")
        user['name'] = new_name
        self.save_log_to_temp_file(f' change name -> {new_name}')

    def change_user_password(self, user):
        """Changing password"""
        old_password = input("Введите старый пароль: ")
        if old_password == user['password']:
            new_password = getpass.getpass("Введите новый пароль: ")
            repeat_password = getpass.getpass("Повторите новый пароль: ")
            if new_password == repeat_password:
                user['password'] = new_password
                with shelve.open(self.data_file) as base:
                    base[user['login']] = user
                print("Новый пароль сохранен.")
                self.save_log_to_temp_file(' change password')
            else:
                print("Введенные пароли не совпадают.")
        else:
            print("Неправильный пароль.")

    def choose_user_from_base(self):
        """Return user login if user in base, return None if not."""
        users_base = shelve.open(self.data_file)
        for index, login in enumerate(sorted(users_base), 1):
            print("[{}] {}".format(index, login))
        choose = input("Input number of user to edit: ")
        if self.check_number_in_range(choose, len(users_base)):
            user = sorted(users_base)[int(choose)-1]
        else:
            user = None
        users_base.close()
        return user

    def try_to_enter_program(self):
        """
        Take user login/password input and return current user privilege
        """
        user_in = None
        login = input("Введите имя пользователя: ")
        users_base = shelve.open(self.data_file)
        if login in users_base:
            while True:
                password = getpass.getpass("Введите пароль: ")
                if users_base[login]['password'] == password:
                    user_in = users_base[login]
                    break
                else:
                    print("Неправильный пароль, попробуйте еще раз.")
        else:
            print("Такого пользователя не существует.")
        users_base.close()
        return user_in

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

    def sync_user(self, user_login):
        """Sync current user with base"""
        with shelve.open(self.data_file) as users_base:
            return users_base[user_login]

    def print_all_users(self):
        """Print all users from base"""
        with shelve.open(self.data_file) as users_base:
            for login in users_base:
                self.print_user(users_base[login])

    @classmethod
    def print_user(cls, user):
        """Print one user"""
        print("name:{name}\nlogin:{login}\n\
password:{password}\naccesse:{accesse}\n".format(**user))

    @classmethod
    def save_log_to_temp_file(cls, log):
        "Get detailed log for user actions."
        file_path = AbsolytePath('log.tmp').get_absolyte_path()
        with open(file_path, 'a') as temp_file:
            temp_file.write(log)

    def get_all_users_list(self):
        """List of all users logins"""
        return self.all_users_list

    def __str__(self):
        output = ['']
        users_base = shelve.open(self.data_file)
        for login in users_base:
            for parametr in users_base[login]:
                output.append(parametr + ':' + users_base[login][parametr])
            output.append('\n')
        users_base.close()
        return ' '.join(output)
