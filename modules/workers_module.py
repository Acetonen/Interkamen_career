#!/usr/bin/env python3.7
"""
This module containe classes that provide accesse to information about workers.

"""
from pprint import pprint
from datetime import date
from typing import Dict, List
from modules.support_modules.standart_functions import BasicFunctions
from modules.administration.logger_cfg import Logs
from modules.support_modules.custom_exceptions import MainMenu


LOGGER = Logs().give_logger(__name__)


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


class AllWorkers(BasicFunctions):
    """Infofmation about all workers and tools to manipulate."""

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

    def __init__(self, user: Dict[str, str]):
        self.user = user
        self.workers_base_path = (
            super().get_root_path() / 'data' / 'workers_base')
        self.workers_archive_path = (
            super().get_root_path() / 'data' / 'workers_archive')
        self.comp_structure_path = (
            super().get_root_path() / 'data' / 'company_structure')
        self.workers_base = super().load_data(self.workers_base_path)
        self.workers_archive = super().load_data(self.workers_archive_path)
        self.comp_structure = super().load_data(self.comp_structure_path)
        # Create company structure file if it not exist.
        if not self.comp_structure_path.exists():
            self.upd_comp_structure()

    @classmethod
    def _add_worker_emp_date(cls, temp_worker: Worker) -> Worker:
        """Add worker emp date."""
        emp_date = input("Введите дату в формате 2018-11-30: ")
        temp_worker.employing_lay_off_dates['employing'] = emp_date
        return temp_worker

    @classmethod
    def _add_penalties(cls, temp_worker: Worker) -> Worker:
        """Add penalties to worker."""
        pen_date = input("Введите дату в формате 2018-11-30: ")
        penalti = input("Введите причину взыскания: ")
        temp_worker.penalties[pen_date] = penalti
        return temp_worker

    @classmethod
    def _change_phone_number(cls, temp_worker: Worker) -> Worker:
        """Change worker phone number"""
        number = input("Введите новый номер (без восьмерки): ")
        new_number = ('+7(' + number[:3] + ')' + number[3:6]
                      + '-' + number[6:8] + '-' + number[8:])
        print(new_number)
        temp_worker.telefone_number = new_number
        return temp_worker

    @classmethod
    def _show_salary(cls, temp_worker: Worker):
        """Show worker salary"""
        salary_count = 0
        for salary_date in sorted(temp_worker.salary):
            print(salary_date, '-', temp_worker.salary[salary_date], 'р.')
            salary_count += temp_worker.salary[salary_date]
        if temp_worker.salary:
            unzero = super().count_unzero_items(temp_worker.salary)
            average_sallary = round(salary_count / unzero)
            print("\033[93mСредняя з/п:\033[0m ", average_sallary, 'p.')

    def _show_penalties(self, temp_worker: Worker) -> Worker:
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
        division = super().choise_from_list(self.interkamen)
        print("Выберете отдел:")
        subdivision = super().choise_from_list(
            self.interkamen[division])
        print("Выберете смену:")
        shift = super().choise_from_list(
            self.interkamen[division][subdivision])
        working_place = {'division': division,
                         'subdivision': subdivision,
                         'profession': profession,
                         'shift': shift}
        return working_place

    def _add_worker_to_structure(self, name: str,
                                 working_place: Dict[str, str]):
        """Add worker to company structure."""
        division = working_place['division']
        subdivision = working_place['subdivision']
        shift = working_place['shift']
        self.comp_structure[division][subdivision][shift].append(name)
        super().dump_data(self.comp_structure_path, self.comp_structure)

    def _change_worker_name(self, temp_worker: Worker) -> Worker:
        """Change worker name."""
        self._delete_worker_from_structure(temp_worker)
        self.workers_base.pop(temp_worker.name, None)
        new_name = input("Введите новые ФИО:")
        temp_worker.name = new_name
        self._add_worker_to_structure(new_name, temp_worker.working_place)
        return temp_worker

    def _delete_worker(self, temp_worker: Worker) -> None:
        """Delete worker."""
        self._delete_worker_from_structure(temp_worker)
        self.workers_base.pop(temp_worker.name, None)
        print(f"\033[91m{temp_worker.name} - удален. \033[0m")
        LOGGER.warning(
            f"User '{self.user['login']}' delete worker: {temp_worker.name}"
        )
        temp_worker = None
        return temp_worker

    def _delete_worker_from_structure(self, worker: Worker):
        """Delete worker name from company structure."""
        print(worker)
        division = worker.working_place['division']
        subdivision = worker.working_place['subdivision']
        shift = worker.working_place['shift']
        self.comp_structure[division][subdivision][shift].remove(worker.name)
        super().dump_data(self.comp_structure_path, self.comp_structure)

    def _lay_off_worker(self, temp_worker: Worker) -> Worker:
        """Lay off worker and put him in archive"""
        temp_worker.employing_lay_off_dates['lay_off'] = str(date.today())
        self.workers_archive[temp_worker.name] = temp_worker
        super().dump_data(self.workers_archive_path, self.workers_archive)
        print(f"\033[91m{temp_worker.name} - уволен. \033[0m")
        LOGGER.warning(
            f"User '{self.user['login']}' lay off worker: {temp_worker.name}"
        )
        temp_worker = self._delete_worker(temp_worker)
        return temp_worker

    def _change_worker_shift(self, temp_worker: Worker) -> Worker:
        """Change worker shift."""
        self._delete_worker_from_structure(temp_worker)
        division = temp_worker.working_place['division']
        subdivision = temp_worker.working_place['subdivision']
        print("Выберете смену:")
        new_shift = super().choise_from_list(
            self.interkamen[division][subdivision])
        temp_worker.working_place['shift'] = new_shift
        self._add_worker_to_structure(
            temp_worker.name, temp_worker.working_place)
        print(f"{temp_worker.name} - переведен в '{new_shift}'.")
        LOGGER.warning(
            f"User '{self.user['login']}' shift worker: {temp_worker.name} -> "
            + f"{new_shift}"
        )
        return temp_worker

    def _change_working_place(self, temp_worker: Worker) -> Worker:
        """Change worker shift."""
        self._delete_worker_from_structure(temp_worker)
        profession = temp_worker.working_place['profession']
        new_working_place = self._add_working_place(profession)
        temp_worker.working_place = new_working_place
        self._add_worker_to_structure(
            temp_worker.name, temp_worker.working_place)
        print(f"{temp_worker.name} - перемещен'.")
        LOGGER.warning(
            f"User '{self.user['login']}' shift worker: {temp_worker.name}"
        )
        return temp_worker

    @classmethod
    def _change_profession(cls, temp_worker: Worker) -> Worker:
        """Change worker profession."""
        new_profession = input("Введите новую профессию: ")
        temp_worker.working_place['profession'] = new_profession
        return temp_worker

    def edit_worker(self):
        """
        Edit worker information.
        """
        print("[ENTER] - выйти."
              "\nВыберете работника для редактирования:")
        division_workers = self.give_workers_from_division()
        while True:
            worker = super().choise_from_list(division_workers,
                                              none_option=True)
            if not worker:
                break
            super().clear_screen()
            self._manage_worker_properties(worker)

    def _manage_worker_properties(self, worker: str):
        """Manage worker property."""
        while True:
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
                'изменить профессию': self._change_profession,
                '[закончить редактирование]': 'break',
            }
            print("\nВыберете пункт для редактирования:")
            action_name = super().choise_from_list(edit_menu_dict)
            print()
            if action_name in ['[закончить редактирование]', '']:
                break

            temp_worker = edit_menu_dict[action_name](temp_worker)

            # If worker deleted.
            if not temp_worker:
                break
            worker = temp_worker.name
            self.workers_base[worker] = temp_worker
            super().dump_data(self.workers_base_path, self.workers_base)
            super().clear_screen()

    def upd_comp_structure(self):
        """Add new division in base"""
        for division in self.interkamen:
            if division not in self.comp_structure:
                self.comp_structure[division] = self.interkamen[division]
                print(f"{division} added.")
                LOGGER.warning(
                    f"User '{self.user['login']}' update company structure."
                )
        super().dump_data(self.comp_structure_path, self.comp_structure)
        input('\n[ENTER] - выйти')

    def print_comp_structure(self):
        """Print company structure"""
        for division in self.comp_structure:
            print(division + ':')
            pprint(self.comp_structure[division])
        input('\n[ENTER] - выйти')

    def add_new_worker(self):
        """Create new worker."""
        name = input("Введите ФИО: ")
        working_place = self._add_working_place(None)
        new_worker = Worker(name, working_place)
        self.workers_base[name] = new_worker
        super().dump_data(self.workers_base_path, self.workers_base)
        self._add_worker_to_structure(name, working_place)
        print(f"\033[92m Добавлен сотрудник '{name}'. \033[0m")
        LOGGER.warning(
            f"User '{self.user['login']}' add worker: {name}"
        )
        input('\n[ENTER] - выйти.')

    def print_archive_workers(self):
        """Print layed off workers"""
        for worker in self.workers_archive:
            print(
                worker,
                self.workers_archive[worker].employing_lay_off_dates['lay_off']
            )
        input('\n[ENTER] - выйти.')

    def add_salary_to_workers(
            self,
            salary_dict: Dict[str, float],
            salary_date: str,
            unofficial_workers: List[str],
    ):
        """Add monthly salary to workers."""
        for worker in salary_dict:
            if worker not in unofficial_workers:
                temp_worker = self.workers_base[worker]
                temp_worker.salary[salary_date] = salary_dict[worker]
                self.workers_base[worker] = temp_worker
        super().dump_data(self.workers_base_path, self.workers_base)

    def return_from_archive(self):
        """Return worker from archive."""
        print("Выберете работника для возвращения:")
        choose = super().choise_from_list(self.workers_archive,
                                          none_option=True)
        if choose:
            worker = self.workers_archive[choose]
            self.workers_archive.pop(choose, None)
            super().dump_data(self.workers_archive_path, self.workers_archive)
            self.workers_base[worker.name] = worker
            super().dump_data(self.workers_base_path, self.workers_base)
            self._add_worker_to_structure(worker.name, worker.working_place)
            print(f"\033[92mCотрудник '{worker.name}' возвращен\033[0m")
            LOGGER.warning(
                f"User '{self.user['login']}' retun worker from archive: "
                + f"{worker.name}"
            )

    def give_workers_from_shift(
            self,
            shift: str,
            division: str = 'Карьер',
            subdivision: str = 'Добычная бригада',
    ) -> List[str]:
        """Give worker list from shift."""
        worker_list = self.comp_structure[division][subdivision][shift]
        return worker_list

    def give_workers_from_division(self) -> List[str]:
        """Print all users from base"""
        print("[ENTER] - выйти."
              "\nВыберете подразделение:")
        division = super().choise_from_list(self.comp_structure,
                                            none_option=True)
        if not division:
            raise MainMenu
        worker_list = [
            worker for subdivision in self.comp_structure[division]
            for shift in self.comp_structure[division][subdivision]
            for worker in self.comp_structure[division][subdivision][shift]
        ]
        return worker_list

    def give_mining_workers(self) -> List[str]:
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
        input('\n[ENTER] - выйти.')

    def print_telefon_numbers(self, itr_shift=None):
        """Print telefone numbers of workers from division.
        if itr shift, print numbers from itr users with short names"""
        workers_list = []
        if itr_shift:
            workers = self.comp_structure[
                'Карьер']['Инженерная служба'][itr_shift]
            itr_list = []
        else:
            workers = self.give_workers_from_division()
        for worker in sorted(workers):
            name = self.workers_base[worker].name
            profession = self.workers_base[worker].working_place['profession']
            telefone = self.workers_base[worker].telefone_number
            if itr_shift:
                name = super().make_name_short(name)
                itr_list.append((name, profession, telefone))
            workers_list.append("{:<32}- {:<24}тел.: {}".format(
                name, profession, telefone))
        if not itr_shift:
            print('\n'.join(workers_list))
            input('\n[ENTER] - выйти')
        else:
            return itr_list

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
        input('\n[ENTER] - выйти.')

    def _give_anniv_workers(self, wor, emp_date) -> List[str]:
        """Give anniversary workers for current year."""
        temp_list = []
        if date.today().year - int(emp_date) in [10, 15, 20, 25, 30]:
            temp_list.append(' '.join([
                self.workers_base[wor].name,
                self.workers_base[wor].employing_lay_off_dates['employing']]))
        return temp_list
