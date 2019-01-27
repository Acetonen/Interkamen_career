#!/usr/bin/env python3
"""Count workers salary."""

import pandas as pd
from .workers_module import AllWorkers
from .workers_salary import WorkersSalary
from .administration.logger_cfg import Logs
from .support_modules.custom_exceptions import MainMenu


LOGGER = Logs().give_logger(__name__)


class SalaryCounter(AllWorkers):
    """Count workers salary."""

    __slots__ = (
        'temp_salary_file',
        'workers_salary_path',
        'workers_salary_file',
    )

    columns = ['year', 'month', 'shift', 'name', 'days', 'salary']

    def __init__(self, user):
        """Load salary and workers data."""
        super().__init__(user)
        self.temp_salary_file = pd.DataFrame()
        self.workers_salary_path = (
            super().get_root_path() / 'data' / 'workers_salary'
        )
        if self.workers_salary_path.exists():
            self.workers_salary_file = super().load_data(
                data_path=self.workers_salary_path,
                user=user,
            )
        else:
            self.workers_salary_file = None

    def _dump_salary_data(self):
        """Dump salary data to file."""
        super().dump_data(
            data_path=self.workers_salary_path,
            base_to_dump=self.workers_salary_file,
            user=self.user,
        )

    def _save_workers_salary(self):
        """Save mech econom and create log file."""
        if not self.workers_salary_file:
            self.workers_salary_file = self.temp_salary_file
        else:
            self.workers_salary_file = self.workers_salary_file.append(
                self.temp_salary_file
            )
        self._dump_salary_data()
        self._log_salary_creation()

    def _log_salary_creation(self):
        """Save log about salary creation."""
        report_name = '{}-{}'.format(
            self.workers_salary_data['year'],
            self.workers_salary_data['month'],
        )
        LOGGER.warning(
            f"User '{self.user.login}' create workers salary.: {report_name}"
        )

    def _give_workers_list(self, shift):
        """Made workers list."""
        career_workers = super().comp_structure['Карьер']
        if shift == 'Смена 1':
            workers_list = (
                career_workers['Инженерная служба']['Смена 1']
                + career_workers['Инженерная служба']['Смена 2']
                + career_workers['Механическая служба']['Смена 1']
                + career_workers['Другие работники']['Смена 1']
                + career_workers['Другие работники']['Регуляный']
            )
        elif shift == 'Смена 2':
            workers_list = (
                career_workers['Механическая служба']['Смена 2']
                + career_workers['Другие работники']['Смена 2']
            )
        return workers_list

    def _input_work_days(self, salary_date):
        """Input workers work days."""
        workers_list = self._give_workers_list(salary_date['shift'])
        salary_dict = {}
        print("Введите количество отработанных смен:")
        for worker in workers_list:
            salary_dict['year'] = salary_date['year']
            salary_dict['month'] = salary_date['month']
            salary_dict['shift'] = salary_date['shift']
            salary_dict['name'] = worker
            salary_dict['days'] = int(input(f"{worker}: "))
            salary_dict['salary'] = self._count_salary(
                worker,
                salary_dict['days']
            )
            self.temp_salary_file = self.temp_salary_file.append(
                salary_dict, ignore_index=True
            )
        self.temp_salary_file = self.temp_salary_file[self.columns]
        self._check_and_save(salary_date)

    def _count_salary(self, worker, days):
        """Count salary to worker."""
        w_profession = super().workers_base[worker].working_place['profession']
        w_salary = WorkersSalary(self.user).salary_list['Карьер'][w_profession]
        month_salary = round(w_salary / 15 * days, 2)
        return month_salary

    def _check_and_save(self, salary_date):
        """Check data and save to base."""
        super().clear_screen()
        print('{}.{}-{}'.format(*map(str, salary_date.values())))
        print(self.temp_salary_file[['name', 'days', 'salary']])
        input()

    def count_salary_workers(self):
        """Count salary to non_brigade workers."""
        while True:
            salary_date = super().input_date()
            if not salary_date:
                break
            print("Выберете смену:")
            shift = super().choise_from_list(['Смена 1', 'Смена 2'])
            if not shift:
                raise MainMenu
            salary_date.update({'shift': shift})
            check = super().check_date_in_dataframe(
                self.workers_salary_file,
                salary_date
            )
            if check:
                print("Данные за этот месяц уже внесены.")
                input("\n[ENTER] - выйти.")
            else:
                self._input_work_days(salary_date)
                break
