#!usr/bin/env python3
"""
This module containe classes that provide accesse to information about workers.
"""

import shelve
from collections import OrderedDict
from modules.absolyte_path_module import AbsolytePath


class Worker:
    """Particular worker"""
    def __init__(self, name, working_place, shift):
        self.name = name
        self.working_place = working_place
        self.working_shift = shift
        self.telefone_number = ''
        self.salary = {}
        self.penalties = {}
        self.contributions = {}

    def get_working_place(self):
        """Get dictionary working_place"""
        return self.working_place

    def __str__(self):
        output = (
            "{} ".format(self.name)
            + "[{division}->{subdivision}->{profession}]; ".format(
                **self.working_place)
            + "{}".format(self.working_shift)
            )
        return output


class AllWorkers:
    """Infofmation about all workers and tools to manipulate"""
    def __init__(self):

        self.workers_base = AbsolytePath(
            'workers_base').get_absolyte_path()
        self.company_structure = AbsolytePath(
            'company_structure').get_absolyte_path()

        self.interkamen = {
            'Карьер': {
                'Инженерная служба': {'Смена 1': [],
                                      'Смена 2': []},
                'Добычная бригада': {'Смена 1': [],
                                     'Смена 2': []},
                'Механическая служба': {'Смена 1': [],
                                        'Смена 2': []},
                'Другие работники': {'Смена 1': [],
                                     'Смена 2': [],
                                     'Регуляный': []}
                }
            }
        self.subdivision_list = ['',
                                 'Инженерная служба',
                                 'Добычная бригада',
                                 'Механическая служба',
                                 'Другие работники']
        self.shift_list = ['', 'Смена 1', 'Смена 2', 'Регуляный']

    def add_new_worker(self):
        """Create new worker."""
        name = input("Введите ФИО: ")
        profession = input("Введите название профессии: ")
        print("Выберете подразделение:")
        division = self.choise_from_list(self.interkamen)
        print("Выберете отдел:")
        subdivision = self.choise_from_list(self.interkamen[division])
        print("Выберете смену:")
        shift = self.choise_from_list(self.interkamen[division][subdivision])
        working_place = {'division': division,
                         'subdivision': subdivision,
                         'profession': profession}
        new_worker = Worker(name, working_place, shift)
        with shelve.open(self.workers_base) as workers_base:
            workers_base[name] = new_worker
        with shelve.open(self.company_structure) as company_structure:
            self.interkamen[division][subdivision][shift].append(name)
            company_structure['division'] = self.interkamen[division]
        log = f"\033[92m добавлен сотрудник '{name}' . \033[0m"
        print(log)
        self.save_log_to_temp_file(log)

    def edit_worker(self):
        """Edit worker information"""
        workers_base = shelve.open(self.workers_base)
        print("Выберете работника для редактирования:")
        worker = self.choise_from_list(workers_base)
        if worker:
            self.save_log_to_temp_file(worker)

        while worker:
            temp_worker = workers_base[worker]
            print()
            print(workers_base[worker])
            edit_menu_dict = OrderedDict
            edit_menu_dict = {
                'редактировать ФИО': self.change_worker_name,
                'перевести в другую смену': self.change_worker_shift,
                'редактировать место работы': self.change_worker_place,
                'удалить работника': self.delete_worker,
                '<-- [Работники]': 'break'
                }
            print("Выберете пункт дляредактирования:")
            action_name = self.choise_from_list(edit_menu_dict)
            action = edit_menu_dict[action_name]
            if action == 'break':
                break
            are_worker_deleted = action(worker)
            if are_worker_deleted:
                break
            workers_base[worker] = temp_worker
        workers_base.close()
# TODO: add action functions


    @classmethod
    def choise_from_list(cls, variants_list):
        """Chose variant from list."""
        sort_list = sorted(variants_list)
        for index, item in enumerate(sort_list, 1):
            print("\t[{}] - {}".format(index, item))
        while True:
            choise = input()
            if cls.check_number_in_range(choise, len(sort_list)):
                chosen_item = sort_list[int(choise)-1]
                return chosen_item

    @classmethod
    def check_number_in_range(cls, user_input, list_range):
        """Check is input a number in current range."""
        check_number = None
        if user_input.isdigit():
            check_number = int(user_input) in range(list_range+1)
            if not check_number:
                print("\nВы должны выбрать цифру из списка.\n")
        else:
            print("\nВы должны ввести цифру.\n")
        return check_number

    @classmethod
    def save_log_to_temp_file(cls, log):
        "Get detailed log for user actions."
        file_path = AbsolytePath('log.tmp').get_absolyte_path()
        with open(file_path, 'a') as temp_file:
            temp_file.write(log)

    def print_all_workers(self):
        """Print all users from base"""
        with shelve.open(self.workers_base) as workers_base:
            for index, warker in enumerate(sorted(workers_base), 1):
                print(f"[{index}]", workers_base[warker])
