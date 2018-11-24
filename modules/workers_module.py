#!/usr/bin/env python3
"""
This module containe classes that provide accesse to information about workers.

class: Worker: 'get_working_place',
               'change_name',
class AllWorkers: 'add_new_worker',
                  'add_worker_to_structure',
                  'add_working_place',
                  'delete_worker_from_structure',
                  'edit_worker',
                  'print_company_structure',
                  'upd_company_structure'
                  'give_workers_from_division',
                  'print_workers_from_division'
                  'print_telefon_numbers'
                  'print_archive_workers'
                  'return_from_archive'
                  'give_workers_from_shift'
                  'add_salary_to_workers'
"""

import os
from pprint import pprint
from datetime import date
from modules.absolyte_path_module import AbsolytePath
from modules.standart_functions import BasicFunctions


class Worker():
    """Particular worker"""
    def __init__(self, name, working_place):
        self.name = name
        self.working_place = working_place
        # working_place = {'division': division,
        #                  'subdivision': subdivision,
        #                  'profession': profession,
        #                  'shift': shift}
        self.telefone_number = ''
        self.employing_lay_off_dates = {'employing': '',
                                        'lay_off': ''}
        self.salary = {}
        self.penalties = {}
        self.contributions = {}

    def get_working_place(self):
        """Get dictionary working_place"""
        return self.working_place

    def change_name(self, new_name):
        """Change user name"""
        self.name = new_name

    def __str__(self):
        output = ("ФИО: {}\n".format(self.name)
                  + """Подразделение: {division}
Служба: {subdivision}
Профессия/должность: {profession}
Смена: {shift}\n""".format(**self.working_place)
                  + "тел.: {}\n".format(self.telefone_number))
        return output


class AllWorkers(BasicFunctions):
    """Infofmation about all workers and tools to manipulate"""
    def __init__(self):
        self.workers_base = AbsolytePath(
            'workers_base').get_absolyte_path()
        self.workers_archive = AbsolytePath(
            'workers_archive').get_absolyte_path()
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
                },
            'Офис': {
                'Инженерная служба': {'Регуляный': []},
                'Бухгалтерия': {'Регуляный': []},
                'Директора': {'Регуляный': []},
                'Отдел кадров': {'Регуляный': []},
                'Руководители служб и снабжение': {'Регулярный': []}
                },
            'КОЦ': {
                'Инженерная служба': {'Регуляный': []},
                'Рабочая бригада': {'Смена 1': [],
                                    'Смена 2': [],
                                    'Смена 3': [],
                                    'Смена 4': []},
                'Механическая служба': {'Регуляный': []},
                'Другие работники': {'Регуляный': []}
                }
            }
        # Create company structure base if it not exist.
        if not os.path.exists(self.company_structure):
            self.upd_company_structure()

    def upd_company_structure(self):
        """Add new division in base"""
        company_structure = super().load_data(self.company_structure)
        for division in self.interkamen:
            if division not in company_structure:
                company_structure[division] = self.interkamen[division]
                print(f"{division} added.")
        super().dump_data(self.company_structure, company_structure)

    def print_company_structure(self):
        """Print company structure"""
        company_structure = super().load_data(self.company_structure)
        for division in company_structure:
            print(division + ':')
            pprint(company_structure[division])

    def add_new_worker(self):
        """Create new worker."""
        name = input("Введите ФИО: ")
        working_place = self.add_working_place(None)
        new_worker = Worker(name, working_place)
        workers_base = super().load_data(self.workers_base)
        workers_base[name] = new_worker
        super().dump_data(self.workers_base, workers_base)
        self.add_worker_to_structure(name, working_place)
        log = f"\033[92m Добавлен сотрудник '{name}'. \033[0m"
        print(log)
        super().save_log_to_temp_file(f"\033[92m '{name}' \033[0m")

    def add_working_place(self, profession):
        """Change worker working place"""
        if not profession:
            profession = input("Введите название профессии: ")
        print("Выберете подразделение:")
        division = super().choise_from_list(self.interkamen)
        print("Выберете отдел:")
        subdivision = super().choise_from_list(self.interkamen[division])
        print("Выберете смену:")
        shift = super().choise_from_list(
            self.interkamen[division][subdivision])
        working_place = {'division': division,
                         'subdivision': subdivision,
                         'profession': profession,
                         'shift': shift}
        return working_place

    def add_worker_to_structure(self, name, working_place):
        """Change company structure"""
        division = working_place['division']
        subdivision = working_place['subdivision']
        shift = working_place['shift']
        company_structure = super().load_data(self.company_structure)
        company_structure[division][subdivision][shift].append(name)
        super().dump_data(self.company_structure, company_structure)

    def delete_worker_from_structure(self, worker):
        """Delete worker name from company structure."""
        print(worker)
        division = worker.working_place['division']
        subdivision = worker.working_place['subdivision']
        shift = worker.working_place['shift']
        company_structure = super().load_data(self.company_structure)
        company_structure[division][subdivision][shift].remove(worker.name)
        super().dump_data(self.company_structure, company_structure)

    def edit_worker(self):
        """
        Edit worker information.
        """

        def change_worker_name(temp_worker):
            """Change worker name."""
            self.delete_worker_from_structure(temp_worker)
            workers_base.pop(temp_worker.name, None)
            new_name = input("Введите новые ФИО:")
            temp_worker.name = new_name
            self.add_worker_to_structure(new_name, temp_worker.working_place)
            return temp_worker

        def change_worker_shift(temp_worker):
            """Change worker shift."""
            self.delete_worker_from_structure(temp_worker)
            division = temp_worker.working_place['division']
            subdivision = temp_worker.working_place['subdivision']
            print("Выберете смену:")
            new_shift = super(AllWorkers, self).choise_from_list(
                self.interkamen[division][subdivision])
            temp_worker.working_place['shift'] = new_shift
            self.add_worker_to_structure(
                temp_worker.name, temp_worker.working_place)
            log = f"{temp_worker.name} - переведен в '{new_shift}'."
            print(log)
            super(AllWorkers, self).save_log_to_temp_file(
                f" - shifted in '{new_shift}'.")
            return temp_worker

        def change_working_place(temp_worker):
            """Change worker shift."""
            self.delete_worker_from_structure(temp_worker)
            profession = temp_worker.working_place['profession']
            new_working_place = self.add_working_place(profession)
            temp_worker.working_place = new_working_place
            self.add_worker_to_structure(
                temp_worker.name, temp_worker.working_place)
            log = f"{temp_worker.name} - перемещен'."
            print(log)
            super(AllWorkers, self).save_log_to_temp_file(f" - shifted.")
            return temp_worker

        def change_phone_number(temp_worker):
            """Change worker phone number"""
            number = input("Введите новый номер (без восьмерки): ")
            new_number = ('+7(' + number[:3] + ')' + number[3:6]
                          + '-' + number[6:8] + '-' + number[8:])
            print(new_number)
            temp_worker.telefone_number = new_number
            return temp_worker

        def lay_off_worker(temp_worker):
            """Lay off worker and put him in archive"""
            temp_worker.employing_lay_off_dates['lay_off'] = str(date.today())
            workers_archive = super(
                AllWorkers, self).load_data(self.workers_archive)
            workers_archive[temp_worker.name] = temp_worker
            super(AllWorkers, self).dump_data(
                self.workers_archive, workers_archive)
            print(f"\033[91m{temp_worker.name} - уволен. \033[0m")
            super(AllWorkers, self).save_log_to_temp_file(
                "\033[91m - layed off\033[0m")
            temp_worker = delete_worker(temp_worker)
            return temp_worker

        def delete_worker(temp_worker):
            """Delete worker."""
            self.delete_worker_from_structure(temp_worker)
            workers_base.pop(temp_worker.name, None)
            log = f"\033[91m{temp_worker.name} - удален. \033[0m"
            print(log)
            super(AllWorkers, self).save_log_to_temp_file(
                "\033[91m - worker deleted. \033[0m")
            temp_worker = None
            return temp_worker

        def show_salary(temp_worker):
            """Show worker salary"""
            salary_count = 0
            for salary_date in sorted(temp_worker.salary):
                print(salary_date, '-', temp_worker.salary[salary_date], 'р.')
                salary_count += temp_worker.salary[salary_date]
            if temp_worker.salary:
                unzero = super(AllWorkers, self).count_unzero_items(
                    temp_worker.salary)
                average_sallary = round(salary_count / unzero)
                print("\033[93mСредняя з/п:\033[0m ", average_sallary, 'p.')

        workers_base = super().load_data(self.workers_base)
        print("Выберете работника для редактирования:")
        division_workers = self.give_workers_from_division()
        worker = super(AllWorkers, self).choise_from_list(
            division_workers, none_option=True)
        if worker:
            super().save_log_to_temp_file(worker)
        super().clear_screen()
        while worker:
            temp_worker = workers_base[worker]
            print(temp_worker)
            edit_menu_dict = {
                'редактировать ФИО': change_worker_name,
                'перевести в другую смену': change_worker_shift,
                'редактировать место работы': change_working_place,
                'изменить номер телефона': change_phone_number,
                'показать зарплату': show_salary,
                'уДАлить работника': delete_worker,
                'уВОлить работника': lay_off_worker,
                '[закончить редактирование]': 'break'
                }
            print("Выберете пункт для редактирования:")
            action_name = super().choise_from_list(edit_menu_dict)

            print()
            if action_name in ['[закончить редактирование]', '']:
                break
            temp_worker = edit_menu_dict[action_name](temp_worker)
            if not temp_worker:
                break
            worker = temp_worker.name
            workers_base[worker] = temp_worker
            super().dump_data(self.workers_base, workers_base)
            super().clear_screen()

    def print_archive_workers(self):
        """Print layed off workers"""
        workers_archive = super().load_data(self.workers_archive)
        for worker in workers_archive:
            print(
                worker,
                workers_archive[worker].employing_lay_off_dates['lay_off']
                )

    def add_salary_to_workers(self, salary_dict,
                              salary_date, unofficial_workers):
        """Add monthly salary to workers"""
        workers_base = super().load_data(self.workers_base)
        for worker in salary_dict:
            if worker not in unofficial_workers:
                temp_worker = workers_base[worker]
                temp_worker.salary[salary_date] = salary_dict[worker]
                workers_base[worker] = temp_worker
        super().dump_data(self.workers_base, workers_base)

    def return_from_archive(self):
        """Return worker from archive"""
        print("Выберете работника для возвращения:")
        workers_archive = super().load_data(self.workers_archive)
        choose = super().choise_from_list(workers_archive, none_option=True)
        if choose:
            worker = workers_archive[choose]
            workers_archive.pop(choose, None)
            super().dump_data(self.workers_archive, workers_archive)
            workers_base = super().load_data(self.workers_base)
            workers_base[worker.name] = worker
            super().dump_data(self.workers_base, workers_base)
            self.add_worker_to_structure(worker.name, worker.working_place)
            print(f"\033[92mCотрудник '{worker.name}' возвращен\033[0m")
            super().save_log_to_temp_file(
                f"\033[92m'{worker.name}' returned.\033[0m")

    def give_workers_from_shift(self, shift, division='Карьер',
                                subdivision='Добычная бригада'):
        """Give worker list from shift"""
        company_structure = super().load_data(self.company_structure)
        worker_list = company_structure[division][subdivision][shift]
        return worker_list

    def give_workers_from_division(self):
        """Print all users from base"""
        company_structure = super().load_data(self.company_structure)
        print("Выберете подразделение:")
        division = super().choise_from_list(company_structure)
        worker_list = [
            worker for subdivision in company_structure[division]
            for shift in company_structure[division][subdivision]
            for worker in company_structure[division][subdivision][shift]
            ]
        return worker_list

    def give_mining_workers(self):
        """Give all mining workers from both shifts."""
        company_structure = super().load_data(self.company_structure)
        mining_workers_list = (
            company_structure['Карьер']['Добычная бригада']['Смена 1']
            + company_structure['Карьер']['Добычная бригада']['Смена 2']
            )
        return mining_workers_list

    def print_workers_from_division(self):
        """Output workers from division"""
        workers_list = self.give_workers_from_division()
        workers_base = super().load_data(self.workers_base)
        for worker in sorted(workers_list):
            print(workers_base[worker])

    def print_telefon_numbers(self):
        """Print telefone numbers of workers from division."""
        workers_list = self.give_workers_from_division()
        workers_base = super().load_data(self.workers_base)
        for worker in sorted(workers_list):
            name = workers_base[worker].name
            profession = workers_base[worker].working_place['profession']
            telefone = workers_base[worker].telefone_number
            print("{:<32}- {:<24}тел.: {}".format(
                name, profession, telefone))
