#!usr/bin/env python3
"""
This module work with User class and access.

Classes: Users: 'change_password',
                'change_user_access',
                'change_user_name',
                'check_number_in_range',
                'check_only_admin',
                'choise_from_list',
                'confirm_deletion',
                'create_new_user',
                'delete_user',
                'edit_user',
                'get_all_users_list',
                'print_user',
                'save_log_to_temp_file',
                'show_all_users',
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
        self.access_list = ['admin', 'boss', 'master', 'mechanic']
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
        print("Choose access by number:")
        access = self.choise_from_list(self.access_list)
        users_base = shelve.open(self.data_file)
        users_base[login] = {'login': login,
                             'name': name,
                             'accesse': access,
                             'password': password}
        log = f"\033[92m user '{login}' created. \033[0m"
        print(log)
        self.save_log_to_temp_file(log)
        users_base.close()

    @classmethod
    def choise_from_list(cls, variants_list):
        """Chose variant from list or dict."""
        sort_list = sorted(variants_list)
        for index, item in enumerate(sort_list, 1):
            print("\t[{}] - {}".format(index, item))
        while True:
            choise = input()
            if cls.check_number_in_range(choise, len(sort_list)):
                chosen_item = sort_list[int(choise)-1]
                return chosen_item

    def edit_user(self):
        """Change user parametrs."""

        users_base = shelve.open(self.data_file)
        print("Input number of user to edit:")
        choosen_user = self.choise_from_list(users_base)
        if choosen_user:
            self.save_log_to_temp_file(choosen_user)

        while choosen_user:
            temp_user = users_base[choosen_user]
            print()
            self.print_user(users_base[choosen_user])
            edit_menu_dict = {'change user access': self.change_user_access,
                              'change user name': self.change_user_name,
                              'change user password': self.change_password,
                              'delete user': self.delete_user,
                              '[exit edition]': 'break'}
            print("Choose action:")
            choosen_action = self.choise_from_list(edit_menu_dict)

            print()
            if choosen_action in ['[exit edition]', '']:
                break
            are_user_deleted = edit_menu_dict[choosen_action](temp_user)
            if are_user_deleted:
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
        print("Choose new accesse:")
        new_accesse = self.choise_from_list(self.access_list)
        user['accesse'] = new_accesse
        self.save_log_to_temp_file(' change access')

    def change_user_name(self, user):
        """Change user name"""
        new_name = input("Input new user name: ")
        user['name'] = new_name
        self.save_log_to_temp_file(f' change name -> {new_name}')

    def change_password(self, user):
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
                self.save_log_to_temp_file('change password')
            else:
                print("Введенные пароли не совпадают.")
        else:
            print("Неправильный пароль.")

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

    def show_all_users(self):
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
