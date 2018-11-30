#!/usr/bin/env python3
"""Mechanics reports."""

import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams as window_parametrs
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsolytePath


class MechReports(BasicFunctions):
    """
    Class to work with statistic of machine maintainence.
    """

    mech_path = AbsolytePath('mechanics_report').get_absolyte_path()
    mech_data = {}
    machine_list = {
        'Хоз. Машина': ['УАЗ 390945', 'УАЗ 220695', 'ГАЗ-3307'],
        'Буровая': ['Commando - 110', 'Commando - 120'],
        'Погрузчик': ['Komazu WA470-3', 'Volvo L 150C'],
        'Кран': ['КС- 5363А', 'КС- 5363Б', 'КС - 5363Б2 '],
        'Компрессор': ['Atlas Copca XAS 881', 'Atlas Copca XAS 882'],
        'Экскаватор': ['Hitachi zx350', 'Hitachi zx400'],
        'Самосвал': ['КрАЗ 914', 'КрАЗ-413', 'КрАЗ-069'],
        'Бульдозер': ['Б-10'],
        'Дизельная эл. ст.': ['ДЭС-AD']
    }
    columns = ['year', 'month', 'day', 'mach_type', 'mach_name',
               'st_plan', 'st_acs', 'st_sep', 'work', 'notes']

    @classmethod
    def check_date_format(cls, date):
        """Check if date format correct"""
        date_numbers = date.split('-')
        correct = (date[4] == '-' and
                   date_numbers[0].isdigit() and
                   date_numbers[1].isdigit() and
                   date_numbers[2].isdigit() and
                   int(date_numbers[1]) < 13 and
                   int(date_numbers[1]) > 0)
        return correct

    @classmethod
    def check_hours_input(cls, hours):
        """Check input hours are correct"""
        hours = hours.split('-')
        for hour in hours:
            try:
                correct = int(hour) < 13
            except ValueError:
                correct = False
            except IndexError:
                correct = False
        return correct

    def __init__(self):
        self.temp_df = pd.DataFrame()
        if os.path.exists(self.mech_path):
            self.mech_file = super().load_data(self.mech_path)
        else:
            self.mech_file = pd.DataFrame(self.mech_data, index=[0])
            super().dump_data(self.mech_path, self.mech_file)

    def _create_blanc(self, rep_date):
        """Create blanc for report."""
        for mach_type in self.machine_list:
            for mach_name in self.machine_list[mach_type]:
                self.mech_data['year'] = rep_date[0]
                self.mech_data['month'] = rep_date[1]
                self.mech_data['day'] = rep_date[2]
                self.mech_data['mach_type'] = mach_type
                self.mech_data['mach_name'] = mach_name
                self.mech_data['st_plan'] = 0
                self.mech_data['st_acs'] = 0
                self.mech_data['st_sep'] = 0
                self.mech_data['work'] = 0
                self.mech_data['notes'] = ''
                self.temp_df = self.temp_df.append(self.mech_data,
                                                   ignore_index=True)
        self.temp_df = self.temp_df[self.columns]

    def _input_date(self):
        """Input date."""
        check_date = False
        while not check_date:
            rep_date = input("Введите число в формате 2018-12-31: ")
            check_date = self.check_date_format(rep_date)
        rep_date = list(map(int, rep_date.split('-')))
        return rep_date

    def _select_machine(self, choise):
        """Select machine from data frame."""
        machine = list(self.temp_df.mach_name)[int(choise)]
        select_mach = self.temp_df['mach_name'] == machine
        print('\n', '\033[92m', machine, '\033[0m')
        return select_mach

    def _input_hours(self):
        """Input hours."""
        check_input = False
        while not check_input:
            h_data = input(
                "Введите часы через тире\n\tПлан-Авар-Зап-Раб: ")
            check_input = self.check_hours_input(h_data)
        h_data = list(map(float, h_data.split('-')))
        return h_data

    def _add_hours_to_mach(self, select_mach, h_data):
        """Add hous to machine."""
        for item in ['st_plan', 'st_acs', 'st_sep', 'work']:
            self.temp_df.loc[select_mach, item] = h_data[0]
            h_data = h_data[1:]

    def _add_note_to_mach(self, select_mach):
        """Add note to mach."""
        note = input("Введите примечание: ")
        self.temp_df.loc[select_mach, 'notes'] = note

    def _save_report(self):
        """Save daily report to base."""
        if self.mech_file.empty:
            self.mech_file = self.temp_df
        else:
            self.mech_file = self.mech_file.append(self.temp_df)
        super().dump_data(self.mech_path, self.mech_file)

    def _check_if_report_exist(self, *rep_date):
        """Check if report allready exist."""
        if self.mech_file.empty:
            check = False
        elif len(rep_date) == 3:
            check = ((self.mech_file['year'] == rep_date[0]) &
                     (self.mech_file['month'] == rep_date[1]) &
                     (self.mech_file['day'] == rep_date[2])).any()
        elif len(rep_date) == 2:
            check = ((self.mech_file['year'] == rep_date[0]) &
                     (self.mech_file['month'] == rep_date[1])).any()
        elif len(rep_date) == 1:
            check = (self.mech_file['year'] == rep_date[0]).any()
        return check

    def _print_current_date_report(self, rep_date):
        """Print current date report."""
        data_frame = self.mech_file[
            (self.mech_file['year'] == rep_date[0]) &
            (self.mech_file['month'] == rep_date[1]) &
            (self.mech_file['day'] == rep_date[2])
            ]
        print(data_frame[
            ['mach_name', 'st_plan', 'st_acs', 'st_sep', 'work', 'notes']
            ])

    def _stat_by_month(self):
        year = int(input("Введите год: "))
        month = int(input("Введите месяц: "))
        if self._check_if_report_exist(year, month):
            self._visualise_stat(year, month=month)
        else:
            print("Отчета за этот период не существует.")

    def _stat_by_year(self):
        year = int(input("Введите год: "))
        if self._check_if_report_exist(year):
            self._visualise_stat(year)
        else:
            print("Отчета за этот период не существует.")

    def _visualise_stat(self, year, month=None):
        """Count KTI and KTG."""

        period_base, shift1_base, shift2_base = self._count_data_for_period(
            year, month)
        period_coef_df = self._create_coef_df(period_base)
        shift1_coef_df = self._create_coef_df(shift1_base)
        shift2_coef_df = self._create_coef_df(shift2_base)
        self._create_plot(
            period_coef_df, shift1_coef_df, shift2_coef_df
        )

    def _create_plot(self, period_coef_df, shift1_coef_df, shift2_coef_df):
        """Create statistic plots."""
        bar_width = 0.35
        opacity = 0.4
        machines = sorted(set(self.mech_file.mach_name))
        x_ktg = list(range(len(machines)))
        x_kti = [x - bar_width for x in x_ktg]
        shot_mach = [x[:3]+' '+x[-3:] for x in period_coef_df.mach]

        window_parametrs['figure.figsize'] = [22.0, 8.0]
        window_parametrs['figure.dpi'] = 100
        window_parametrs['savefig.dpi'] = 100
        window_parametrs['font.size'] = 12
        window_parametrs['legend.fontsize'] = 'large'
        window_parametrs['figure.titlesize'] = 'large'

        plt.subplot(1, 3, 1)
        plt.barh(x_ktg, period_coef_df.ktg, bar_width,
                 alpha=opacity, color='b', label='КТГ')
        plt.barh(x_kti, period_coef_df.rel_kti, bar_width,
                 alpha=opacity, color='r', label='КТИ')
        plt.yticks(x_ktg, period_coef_df.mach)
        plt.title('КТГ и КТИ за выбранный период.')
        plt.xlabel('%')
        plt.legend()
        plt.grid(True, linestyle='--', which='major',
                 color='grey', alpha=.25, axis='x')

        plt.subplot(1, 3, 2)
        plt.barh(x_ktg, shift1_coef_df.kti, bar_width,
                 alpha=opacity, color='b', label='КТИ бригады 1')
        plt.barh(x_kti, shift2_coef_df.kti, bar_width,
                 alpha=opacity, color='g', label='КТИ бригады 2')
        plt.title('Сравнительные КТИ бригад.')
        plt.yticks(x_ktg, shot_mach)
        plt.xlabel('%')
        plt.legend()
        plt.grid(True, linestyle='--', which='major',
                 color='grey', alpha=.25, axis='x')

        plt.subplot(1, 3, 3)
        plt.barh(x_ktg, shift1_coef_df.ktg, bar_width,
                 alpha=opacity, color='b', label='КТГ бригады 1')
        plt.barh(x_kti, shift2_coef_df.ktg, bar_width,
                 alpha=opacity, color='g', label='КТГ бригады 2')
        plt.title('Сравнительные КТГ бригад.')
        plt.yticks(x_ktg, shot_mach)
        plt.xlabel('%')
        plt.legend()
        plt.grid(True, linestyle='--', which='major',
                 color='grey', alpha=.25, axis='x')
        plt.show()

    def _count_data_for_period(self, year, month):
        """Create data frames for current period)"""
        if month:
            period_base = self.mech_file[
                (self.mech_file.year == year) & (self.mech_file.month == month)
                ]
        else:
            period_base = self.mech_file[(self.mech_file.year == year)]
        shift1_base = period_base[period_base.day < 16]
        shift2_base = period_base[period_base.day > 15]
        return period_base, shift1_base, shift2_base

    def _create_coef_df(self, curr_base):
        """Create coef DF for cerrent period."""
        machines = sorted(set(self.mech_file.mach_name))
        temp_coef_list = {
            'mach': [],
            'ktg': [],
            'kti': [],
            'rel_kti': []
        }
        for mach in machines:
            mach_period = curr_base[curr_base.mach_name == mach]
            kalendar_time = mach_period.shape[1] * 12
            stand_time = sum(
                mach_period.st_plan + mach_period.st_sep + mach_period.st_acs)
            avail_time = kalendar_time - stand_time
            ktg = avail_time / kalendar_time * 100
            kti = sum(mach_period.work) / avail_time * 100
            rel_kti = ktg / 100 * kti
            temp_coef_list['mach'].append(mach)
            temp_coef_list['ktg'].append(round(ktg, 1))
            temp_coef_list['kti'].append(round(kti, 1))
            temp_coef_list['rel_kti'].append(round(rel_kti, 1))
        coef_df = pd.DataFrame(temp_coef_list)
        return coef_df

    def create_report(self):
        """Create daily report."""
        check = True
        while check:
            rep_date = self._input_date()
            check = self._check_if_report_exist(*rep_date)
            if check:
                print("Отчет за это число уже существует.")

        self._create_blanc(rep_date)
        while True:
            super().clear_screen()
            print('.'.join(map(str, rep_date)))
            print(self.temp_df[
                ['mach_name', 'st_plan', 'st_acs', 'st_sep', 'work', 'notes']
                ])

            choise = input("\nВыберете технику для внесения данных"
                           "\n(ENTER - выход без сохранения)"
                           "\n('c' - сохранить отчет): ")
            if choise in ['c', 'C', 'с', 'С']:
                self._save_report()
                super().save_log_to_temp_file('.'.join(map(str, rep_date)))
                break
            elif not choise:
                break
            elif not choise.isdigit():
                continue
            elif int(choise) > 18:
                continue

            select_mach = self._select_machine(choise)
            h_data = self._input_hours()
            self._add_hours_to_mach(select_mach, h_data)
            self._add_note_to_mach(select_mach)

    def show_report(self):
        """Show report for current date."""
        check = False
        while not check:
            rep_date = self._input_date()
            check = self._check_if_report_exist(*rep_date)
            if not check:
                print("Отчет за это число отстутствует.")
        super().clear_screen()
        print('.'.join(map(str, rep_date)))
        self._print_current_date_report(rep_date)

    def show_statistic(self):
        """Show statistic for mechanics report."""
        stat_variants = {
            'Месячная статистика': self._stat_by_month,
            'Годовая статистика': self._stat_by_year
        }
        print("Выберете вид отчета:")
        stat = super().choise_from_list(stat_variants, none_option=True)
        if stat:
            stat_variants[stat]()


if __name__ == '__main__':
    TEST = MechReports()
    TEST.show_statistic()
