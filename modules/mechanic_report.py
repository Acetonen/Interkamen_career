#!/usr/bin/env python3
"""
Mechanics reports.

MechReports:
 'create_report', - create mechanics report.
 'machine_list', - all career machines.
 'show_report', - show choosen report.
 'show_statistic' - show month or year stats.
"""

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
        'Хоз. Машина': ['УАЗ-390945', 'УАЗ-220695', 'ГАЗ-3307'],
        'Буровая': ['Commando-110', 'Commando-120'],
        'Погрузчик': ['Komazu-WA470', 'Volvo-L150'],
        'Кран': ['КС-5363А', 'КС-5363Б', 'КС-5363Б2 '],
        'Компрессор': ['AtlasC-881', 'AtlasC-882'],
        'Экскаватор': ['Hitachi-350', 'Hitachi-400'],
        'Самосвал': ['КрАЗ-914', 'КрАЗ-413', 'КрАЗ-069'],
        'Бульдозер': ['Бул-10'],
        'Дизельная эл. ст.': ['ДЭС-AD']
    }
    columns = ['year', 'month', 'day', 'mach_type', 'mach_name',
               'st_plan', 'st_acs', 'st_sep', 'work', 'notes']

    def __init__(self):
        self.temp_df = pd.DataFrame()
        if os.path.exists(self.mech_path):
            self.mech_file = super().load_data(self.mech_path)
        else:
            self.mech_file = pd.DataFrame(self.mech_data, index=[0])
            super().dump_data(self.mech_path, self.mech_file)

    @classmethod
    def check_date_format(cls, date):
        """Check if date format correct"""
        date_numbers = date.split('-')
        correct = (date[4] == '-' and
                   len(date_numbers) == 2 and
                   date_numbers[0].isdigit() and
                   date_numbers[1].isdigit() and
                   int(date_numbers[1]) < 13 and
                   int(date_numbers[1]) > 0)
        return correct

    @classmethod
    def check_hours_input(cls, hours):
        """Check input hours are correct"""
        hours = hours.split('-')
        try:
            correct = sum(list(map(int, hours))) < 13 and len(hours) == 4
        except ValueError:
            correct = False
        except IndexError:
            correct = False
        return correct

    @classmethod
    def create_coeff_compare(cls, fig_plot, coefs, labels, title):
        """Create plot for compare KTG by shifts."""
        x_ktg = list(range(len(labels[0])))
        x_kti = [x - 0.35 for x in x_ktg]

        axle = fig_plot[0].add_subplot(fig_plot[1])
        axle.barh(x_ktg, coefs[0], 0.35, alpha=0.4, color='b',
                  label=labels[1], tick_label=labels[0])
        axle.barh(x_kti, coefs[1], 0.35, alpha=0.4, color='g',
                  label=labels[2])
        axle.set_title(title)
        axle.set_xlabel('%')
        axle.legend()
        axle.grid(True, linestyle='--', which='major', color='grey',
                  alpha=.25, axis='x')

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
            rep_date = input("Введите год и месяц формате 2018-12: ")
            if not rep_date:
                return rep_date
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
            if not check_input:
                print("Необходимо ввести 4 числа, сумма которых не более 12!")
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
            avail_days = self.mech_file[
                (self.mech_file['year'] == rep_date[0]) &
                (self.mech_file['month'] == rep_date[1])].day
            print("Имеющиеся отчеты: {}".format(sorted(set(avail_days))))
        elif len(rep_date) == 1:
            check = (self.mech_file['year'] == rep_date[0]).any()
            avail_months = self.mech_file[
                (self.mech_file['year'] == rep_date[0])].month
            print("Имеющиеся отчеты: {}".format(sorted(set(avail_months))))
        return check

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
        # Create compact machine names.
        machines = sorted(set(self.mech_file.mach_name))
        shot_mach = [x[:3]+' '+x[-3:] for x in machines]

        window_parametrs['figure.figsize'] = [22.0, 8.0]
        window_parametrs['figure.dpi'] = 100
        window_parametrs['savefig.dpi'] = 100
        window_parametrs['font.size'] = 12
        window_parametrs['legend.fontsize'] = 'large'
        window_parametrs['figure.titlesize'] = 'large'

        figure = plt.figure()
        suptitle = figure.suptitle("Ремонты техники.", fontsize="x-large")
        self.create_coeff_compare(
            (figure, 131),
            labels=(period_coef_df.mach, 'КТГ', 'КТИ'),
            title='КТГ и КТИ за выбранный период.',
            coefs=(period_coef_df.ktg, period_coef_df.rel_kti)
            )
        self.create_coeff_compare(
            (figure, 132),
            labels=(shot_mach, 'Бригада 1', 'Бригада 2'),
            title='Сравнительные КТИ бригад.',
            coefs=(shift1_coef_df.kti, shift2_coef_df.kti)
            )
        self.create_coeff_compare(
            (figure, 133),
            labels=(shot_mach, 'Бригада 1', 'Бригада 2'),
            title='Сравнительные КТГ бригад.',
            coefs=(shift1_coef_df.ktg, shift2_coef_df.ktg)
            )
        figure.tight_layout()
        suptitle.set_y(0.95)
        figure.subplots_adjust(top=0.85)
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
            kalendar_time = mach_period.shape[0] * 12
            stand_time = sum(
                mach_period.st_plan + mach_period.st_sep + mach_period.st_acs)
            avail_time = kalendar_time - stand_time
            ktg = avail_time / kalendar_time * 100
            if avail_time:
                kti = sum(mach_period.work) / avail_time * 100
            else:
                kti = 0
            rel_kti = ktg / 100 * kti
            temp_coef_list['mach'].append(mach)
            temp_coef_list['ktg'].append(round(ktg, 1))
            temp_coef_list['kti'].append(round(kti, 1))
            temp_coef_list['rel_kti'].append(round(rel_kti, 1))
        coef_df = pd.DataFrame(temp_coef_list)
        return coef_df

    def _working_with_report(self, rep_date):
        """Edit report."""
        while True:
            super().clear_screen()
            print('.'.join(map(str, rep_date)))
            print(self.temp_df[
                ['mach_name', 'st_plan', 'st_acs', 'st_sep', 'work', 'notes']
                ])
            choise = input("\n[у] - выйти и \033[91mУДАЛИТЬ\033[m данные."
                           "\n[c] - \033[92mСОХРАНИТЬ\033[0m отчет.\n"
                           "\nВыберете технику для внесения данных: ")
            if choise in ['c', 'C', 'с', 'С']:
                self._save_report()
                super().save_log_to_temp_file('.'.join(map(str, rep_date)))
                print("\n\033[92mДанные сохранены.\033[0m")
                break
            elif choise in ['у', 'У', 'y', 'Y']:
                confirm = super().confirm_deletion('отчет')
                if confirm:
                    break
            elif not choise.isdigit():
                continue
            elif int(choise) > 18:
                continue
            select_mach = self._select_machine(choise)
            h_data = self._input_hours()
            self._add_hours_to_mach(select_mach, h_data)
            self._add_note_to_mach(select_mach)

    def _make_day_report_temp(self, rep_date):
        """Make report of day temr and drop it from DF."""
        self.temp_df = self.mech_file[
            (self.mech_file['year'] == rep_date[0]) &
            (self.mech_file['month'] == rep_date[1]) &
            (self.mech_file['day'] == rep_date[2])
            ]
        self.mech_file = self.mech_file.append(
            self.temp_df).drop_duplicates(keep=False)
        super().dump_data(self.mech_path, self.mech_file)

    def create_report(self):
        """Create daily report."""
        while True:
            rep_date = self._input_date()
            if not rep_date:
                break
            check = self._check_if_report_exist(*rep_date)
            day = input("Введите день: ")
            rep_date.append(int(day))
            check = self._check_if_report_exist(*rep_date)
            if check:
                print("Отчет за это число уже существует.")
            else:
                self._create_blanc(rep_date)
                self._working_with_report(rep_date)
                break

    def edit_report(self):
        """Show report for current date."""
        while True:
            rep_date = self._input_date()
            if not rep_date:
                break
            check = self._check_if_report_exist(*rep_date)
            if not check:
                print("Отчеты за этот месяц отстутствует.")
            else:
                day = input("Введите день: ")
                rep_date.append(int(day))
                self._make_day_report_temp(rep_date)
                self._working_with_report(rep_date)
                break

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
