#!/usr/bin/env python3
"""
This module containe classes that provide accesse to information about workers.

"""

import os
from pprint import pprint
from datetime import date

from modules.support_modules.absolyte_path_module import AbsPath
from modules.support_modules.standart_functions import BasicFunctions as BasF


class Worker():
    """Particular worker"""

    telefone_number = ''
    employing_lay_off_dates = {'employing': '',
                               'lay_off': ''}
    salary = {}
    penalties = {}
    contributions = {}

    def __init__(self, name, working_place):
        self.name = name
        self.working_place = working_place
        # working_place = {'division': division,
        #                  'subdivision': subdivision,
        #                  'profession': profession,
        #                  'shift': shift}

    def __repr__(self):
        output = ("ФИО: {}\n".format(self.name)
                  + """Подразделение: {division}
Служба: {subdivision}
Профессия/должность: {profession}
Смена: {shift}\n""".format(**self.working_place)
                  + "тел.: {}\n".format(self.telefone_number)
                  + "дата устройства на работу: {}\n".format(
                      self.employing_lay_off_dates['employing']
                  ))
        return output


class AllWorkers(BasF):
    """Infofmation about all workers and tools to manipulate."""

    workers_base_path = AbsPath.get_path('data', 'workers_base')
    workers_archive_path = AbsPath.get_path('data', 'workers_archive')
    comp_structure_path = AbsPath.get_path('data', 'company_structure')

    interkamen = {
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

    def __init__(self):
        self.workers_base = BasF.load_data(self.workers_base_path)
        self.workers_archive = BasF.load_data(self.workers_archive_path)
        self.comp_structure = BasF.load_data(self.comp_structure_path)
        # Create company structure file if it not exist.
        if not os.path.exists(self.comp_structure_path):
            self.upd_comp_structure()

    @classmethod
    def _add_worker_emp_date(cls, temp_worker):
        """Add worker emp date."""
        emp_date = input("Введите дату в формате 2018-11-30: ")
        temp_worker.employing_lay_off_dates['employing'] = emp_date
        return temp_worker

    @classmethod
    def _add_penalties(cls, temp_worker):
        """Add penalties to worker."""
        pen_date = input("Введите дату в формате 2018-11-30: ")
        penalti = input("Введите причину взыскания: ")
        temp_worker.penalties[pen_date] = penalti
        return temp_worker

    @classmethod
    def _change_phone_number(cls, temp_worker):
        """Change worker phone number"""
        number = input("Введите новый номер (без восьмерки): ")
        new_number = ('+7(' + number[:3] + ')' + number[3:6]
                      + '-' + number[6:8] + '-' + number[8:])
        print(new_number)
        temp_worker.telefone_number = new_number
        return temp_worker

    @classmethod
    def _show_salary(cls, temp_worker):
        """Show worker salary"""
        salary_count = 0
        for salary_date in sorted(temp_worker.salary):
            print(salary_date, '-', temp_worker.salary[salary_date], 'р.')
            salary_count += temp_worker.salary[salary_date]
        if temp_worker.salary:
            unzero = BasF.count_unzero_items(temp_worker.salary)
            average_sallary = round(salary_count / unzero)
            print("\033[93mСредняя з/п:\033[0m ", average_sallary, 'p.')

    def _show_penalties(self, temp_worker):
        """Show worker penalties."""
        for pen_date in temp_worker.penalties:
            print("{} - {}".format(pen_date, temp_worker.penalties[pen_date]))
        add = input("Добавить взыскание? Д/н: ")
        if add.lower() == 'д':
            temp_worker = self._add_penalties(temp_worker)
        return temp_worker

    def _add_working_place(self, profession):
        """Change worker working place"""
        if not profession:
            profession = input("Введите название профессии: ")
        print("Выберете подразделение:")
        division = BasF.choise_from_list(self.interkamen)
        print("Выберете отдел:")
        subdivision = BasF.choise_from_list(
            self.interkamen[division])
        print("Выберете смену:")
        shift = BasF.choise_from_list(
            self.interkamen[division][subdivision])
        working_place = {'division': division,
                         'subdivision': subdivision,
                         'profession': profession,
                         'shift': shift}
        return working_place

    def _add_worker_to_structure(self, name, working_place):
        """Add worker to company structure."""
        division = working_place['division']
        subdivision = working_place['subdivision']
        shift = working_place['shift']
        self.comp_structure[division][subdivision][shift].append(name)
        BasF.dump_data(self.comp_structure_path, self.comp_structure)

    def _change_worker_name(self, temp_worker):
        """Change worker name."""
        self._delete_worker_from_structure(temp_worker)
        self.workers_base.pop(temp_worker.name, None)
        new_name = input("Введите новые ФИО:")
        temp_worker.name = new_name
        self._add_worker_to_structure(new_name, temp_worker.working_place)
        return temp_worker

    def _delete_worker(self, temp_worker):
        """Delete worker."""
        self._delete_worker_from_structure(temp_worker)
        self.workers_base.pop(temp_worker.name, None)
        log = f"\033[91m{temp_worker.name} - удален. \033[0m"
        print(log)
        BasF.save_log_to_temp_file("\033[91m - worker deleted. \033[0m")
        temp_worker = None
        return temp_worker

    def _delete_worker_from_structure(self, worker):
        """Delete worker name from company structure."""
        print(worker)
        division = worker.working_place['division']
        subdivision = worker.working_place['subdivision']
        shift = worker.working_place['shift']
        self.comp_structure[division][subdivision][shift].remove(worker.name)
        BasF.dump_data(self.comp_structure_path, self.comp_structure)

    def _lay_off_worker(self, temp_worker):
        """Lay off worker and put him in archive"""
        temp_worker.employing_lay_off_dates['lay_off'] = str(date.today())
        self.workers_archive[temp_worker.name] = temp_worker
        BasF.dump_data(self.workers_archive_path, self.workers_archive)
        print(f"\033[91m{temp_worker.name} - уволен. \033[0m")
        BasF.save_log_to_temp_file("\033[91m - layed off\033[0m")
        temp_worker = self._delete_worker(temp_worker)
        return temp_worker

    def _change_worker_shift(self, temp_worker):
        """Change worker shift."""
        self._delete_worker_from_structure(temp_worker)
        division = temp_worker.working_place['division']
        subdivision = temp_worker.working_place['subdivision']
        print("Выберете смену:")
        new_shift = BasF.choise_from_list(
            self.interkamen[division][subdivision])
        temp_worker.working_place['shift'] = new_shift
        self._add_worker_to_structure(
            temp_worker.name, temp_worker.working_place)
        log = f"{temp_worker.name} - переведен в '{new_shift}'."
        print(log)
        BasF.save_log_to_temp_file(f" - shifted in '{new_shift}'.")
        return temp_worker

    def _change_working_place(self, temp_worker):
        """Change worker shift."""
        self._delete_worker_from_structure(temp_worker)
        profession = temp_worker.working_place['profession']
        new_working_place = self._add_working_place(profession)
        temp_worker.working_place = new_working_place
        self._add_worker_to_structure(
            temp_worker.name, temp_worker.working_place)
        log = f"{temp_worker.name} - перемещен'."
        print(log)
        BasF.save_log_to_temp_file(f" - shifted.")
        return temp_worker

    def edit_worker(self):
        """
        Edit worker information.
        """
        print("Выберете работника для редактирования:")
        division_workers = self.give_workers_from_division()
        worker = BasF.choise_from_list(division_workers, none_option=True)
        if worker:
            BasF.save_log_to_temp_file(worker)
        print("Редактирование отменено.")
        BasF.clear_screen()
        while worker:
            temp_worker = self.workers_base[worker]
            print(temp_worker)
            edit_menu_dict = {
                'редактировать ФИО': self._change_worker_name,
                'уДАлить работника': self._delete_worker,
                'уВОлить работника': self._lay_off_worker,
                'перевести в другую смену': self._change_worker_shift,
                'редактировать место работы': self._change_working_place,
                'изменить номер телефона': self._change_phone_number,
                'показать зарплату': self._show_salary,
                'дата устройства на работу': self._add_worker_emp_date,
                'показать взыскания': self._show_penalties,
                '[закончить редактирование]': 'break'
                }
            print("\nВыберете пункт для редактирования:")
            action_name = BasF.choise_from_list(edit_menu_dict)
            print()
            if action_name in ['[закончить редактирование]', '']:
                break

            temp_worker = edit_menu_dict[action_name](temp_worker)

            # If worker deleted.
            if not temp_worker:
                break
            worker = temp_worker.name
            self.workers_base[worker] = temp_worker
            BasF.dump_data(self.workers_base_path, self.workers_base)
            BasF.clear_screen()

    def upd_comp_structure(self):
        """Add new division in base"""
        for division in self.interkamen:
            if division not in self.comp_structure:
                self.comp_structure[division] = self.interkamen[division]
                print(f"{division} added.")
        BasF.dump_data(self.comp_structure_path, self.comp_structure)

    def print_comp_structure(self):
        """Print company structure"""
        for division in self.comp_structure:
            print(division + ':')
            pprint(self.comp_structure[division])

    def add_new_worker(self):
        """Create new worker."""
        name = input("Введите ФИО: ")
        working_place = self._add_working_place(None)
        new_worker = Worker(name, working_place)
        self.workers_base[name] = new_worker
        BasF.dump_data(self.workers_base_path, self.workers_base)
        self._add_worker_to_structure(name, working_place)
        log = f"\033[92m Добавлен сотрудник '{name}'. \033[0m"
        print(log)
        BasF.save_log_to_temp_file(f"\033[92m '{name}' \033[0m")

    def print_archive_workers(self):
        """Print layed off workers"""
        for worker in self.workers_archive:
            print(
                worker,
                self.workers_archive[worker].employing_lay_off_dates['lay_off']
                )

    def add_salary_to_workers(self, salary_dict,
                              salary_date, unofficial_workers):
        """Add monthly salary to workers."""
        for worker in salary_dict:
            if worker not in unofficial_workers:
                temp_worker = self.workers_base[worker]
                temp_worker.salary[salary_date] = salary_dict[worker]
                self.workers_base[worker] = temp_worker
        BasF.dump_data(self.workers_base_path, self.workers_base)

    def return_from_archive(self):
        """Return worker from archive."""
        print("Выберете работника для возвращения:")
        choose = BasF.choise_from_list(self.workers_archive, none_option=True)
        if choose:
            worker = self.workers_archive[choose]
            self.workers_archive.pop(choose, None)
            BasF.dump_data(self.workers_archive_path, self.workers_archive)
            self.workers_base[worker.name] = worker
            BasF.dump_data(self.workers_base_path, self.workers_base)
            self._add_worker_to_structure(worker.name, worker.working_place)
            print(f"\033[92mCотрудник '{worker.name}' возвращен\033[0m")
            BasF.save_log_to_temp_file(
                f"\033[92m'{worker.name}' returned.\033[0m")

    def give_workers_from_shift(self, shift, division='Карьер',
                                subdivision='Добычная бригада'):
        """Give worker list from shift."""
        worker_list = self.comp_structure[division][subdivision][shift]
        return worker_list

    def give_workers_from_division(self):
        """Print all users from base"""
        print("Выберете подразделение:")
        division = BasF.choise_from_list(self.comp_structure, none_option=True)
        worker_list = [
            worker for subdivision in self.comp_structure[division]
            for shift in self.comp_structure[division][subdivision]
            for worker in self.comp_structure[division][subdivision][shift]
        ]
        return worker_list

    def give_mining_workers(self):
        """Give all mining workers from both shifts."""
        mining_workers_list = (
            self.comp_structure['Карьер']['Добычная бригада']['Смена 1']
            + self.comp_structure['Карьер']['Добычная бригада']['Смена 2']
        )
        return mining_workers_list

    def print_workers_from_division(self):
        """Output workers from division"""
        workers_list = self.give_workers_from_division()
        for worker in sorted(workers_list):
            print(self.workers_base[worker])

    def print_telefon_numbers(self, itr_shift=None):
        """Print telefone numbers of workers from division.
        if itr shift, print numbers from itr users with short names"""
        workers_list = []
        space = 32
        if itr_shift:
            workers = self.comp_structure[
                'Карьер']['Инженерная служба'][itr_shift]
        else:
            workers = self.give_workers_from_division()
        for worker in sorted(workers):
            name = self.workers_base[worker].name
            if itr_shift:
                name = BasF.make_name_short(name)
                space = 15
            profession = self.workers_base[worker].working_place['profession']
            telefone = self.workers_base[worker].telefone_number
            workers_list.append("{:<{space}}- {:<24}тел.: {}".format(
                name, profession, telefone, space=space))
        if not itr_shift:
            print('\n'.join(workers_list))
        return workers_list

    def show_anniversary_workers(self):
        """Show workers with this year anniversary."""
        anniv_list = []
        for wor in self.workers_base:
            emp_date = (self.workers_base[wor]
                        .employing_lay_off_dates['employing'][:4])
            if emp_date:
                anniv_list.extend(self._give_anniv_workers(wor, emp_date))
        if anniv_list:
            print("Юбиляры этого года:")
            for worker in sorted(anniv_list):
                print(worker)
        else:
            print("Нет юбиляров в этом году")

    def _give_anniv_workers(self, wor, emp_date):
        """Give anniversary workers for current year."""
        temp_list = []
        if date.today().year - int(emp_date) in [10, 15, 20, 25, 30]:
            temp_list.append(' '.join([
                self.workers_base[wor].name,
                self.workers_base[wor].employing_lay_off_dates['employing']]))
        return temp_list
