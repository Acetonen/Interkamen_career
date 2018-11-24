#!/usr/bin/env python3
"""
Working with statistic of drill instrument.
"""

import os
from matplotlib import pyplot as plt
from matplotlib import rcParams as window_parametrs
import pandas as pd
from modules.absolyte_path_module import AbsolytePath
from modules.main_career_report import Reports
from modules.standart_functions import BasicFunctions


class DrillInstruments(BasicFunctions):
    """
    All information about drill instruments.
    """
    def __init__(self, data_file=AbsolytePath('drill_instruments')):
        self.drill_file = data_file.get_absolyte_path()
        self.month_list = ['01', '02', '03', '04', '05', '06',
                           '07', '08', '09', '10', '11', '12']
        self.drill_data = {}

    def _check_if_report_avaliable(self):
        """Check if main report exist and complate."""
        self.drill_data['year'] = input("Введите год: ")
        print("Выберете месяц:")
        self.drill_data['month'] = super().choise_from_list(self.month_list)
        print("Выберете смену:")
        self.drill_data['shift'] = super().choise_from_list(Reports().shifts)
        main_report_results = Reports().give_main_results(
            self.drill_data['year'],
            self.drill_data['month'],
            self.drill_data['shift'])
        return main_report_results

    def _input_other_stats(self, main_report_results):
        """Input other stats about drill instrument."""
        (self.drill_data['meters'],
         self.drill_data['result'],
         self.drill_data['rock_mass']) = main_report_results
        self.drill_data['bits32'] = int(input("коронки 32: "))
        self.drill_data['bits35'] = int(input("коронки 35: "))
        self.drill_data['bar3'] = int(input("штанги 3м: "))
        self.drill_data['bar6'] = int(input("штанги 6м: "))
        self.drill_data['bits_in_rock'] = int(input("коронки в скале: "))
        self.drill_data['driller'] = Reports().drillers[
            Reports().shifts.index(self.drill_data['shift'])]

    def _check_correctly_input(self):
        """Check if data input corretly."""
        print("Отчет: ")
        for item in sorted(self.drill_data):
            print(item, ':', self.drill_data[item])
        confirm = input("\nПроверьте корректность ввода данных,\
если данные введены верно введите 'д': ")
        if confirm == 'д':
            self._save_to_drill_file()
            print("Отчет по инструменту создан.")
            super().save_log_to_temp_file(
                '{}-{}-{}\033[94m created\033[0m'.format(
                    self.drill_data['year'],
                    self.drill_data['month'],
                    self.drill_data['shift'])
                )

    def _save_to_drill_file(self):
        """Save new data to drill file"""
        if os.path.exists(self.drill_file):
            old_data = super().load_data(self.drill_file)
            new_data = old_data.append(self.drill_data, ignore_index=True)
        else:
            new_data = pd.DataFrame(self.drill_data, index=[0])
        super().dump_data(self.drill_file, new_data)

    def _visualise_statistic(self, year):
        """Visualise statistic."""
        drill_data = super().load_data(self.drill_file)
        drill_year = drill_data.year == year
        data_by_year = drill_data[drill_year].sort_values(by=['month'])
        self.print_statistic_by_year(data_by_year)
        shift1 = data_by_year['shift'] == 'Смена 1'
        shift2 = data_by_year['shift'] == 'Смена 2'
        all_bits1 = (data_by_year[shift1].bits32
                     + data_by_year[shift1].bits35)
        all_bits2 = (data_by_year[shift2].bits32
                     + data_by_year[shift2].bits35)
        self._create_plots(
            data_by_year,
            (shift1, shift2),
            (all_bits1, all_bits2)
            )

    def _create_plots(self, data_by_year, shifts, bits):
        """Create plots for drill data."""
        window_parametrs['figure.figsize'] = [18.0, 10.0]
        window_parametrs['figure.dpi'] = 100
        window_parametrs['savefig.dpi'] = 100
        window_parametrs['font.size'] = 12
        window_parametrs['legend.fontsize'] = 'large'
        window_parametrs['figure.titlesize'] = 'large'
        plt.subplot(2, 2, 1)
        self.create_meters_by_month(data_by_year, shifts)
        plt.subplot(2, 2, 2)
        self.create_all_bits(data_by_year, shifts, bits)
        plt.subplot(2, 2, 3)
        self.create_meters_by_bits(data_by_year, shifts, bits)
        plt.subplot(2, 2, 4)
        self.create_bits_by_thousand_rocks(data_by_year, shifts, bits)
        plt.show()

    @classmethod
    def create_meters_by_month(cls, data_by_year, shifts):
        """Totall drill meters in month by each shift."""
        plt.plot(data_by_year[shifts[0]].month, data_by_year[shifts[0]].meters,
                 marker='D', markersize=4)
        plt.plot(data_by_year[shifts[1]].month, data_by_year[shifts[1]].meters,
                 marker='D', markersize=4)
        plt.legend(['Смена 1', 'Смена 2'])
        plt.ylabel('шпурометры, м.')
        plt.grid(b=True, linestyle='--', linewidth=0.5)
        plt.title('Пробурено за смену.')

    @classmethod
    def create_all_bits(cls, data_by_year, shifts, bits):
        """Totall used bits by shift and bits in rock."""
        plt.plot(data_by_year[shifts[0]].month, bits[0],
                 marker='D', markersize=4)
        plt.plot(data_by_year[shifts[1]].month, bits[1],
                 marker='D', markersize=4)
        plt.plot(data_by_year[shifts[0]].month,
                 data_by_year[shifts[0]].bits_in_rock,
                 marker='D', markersize=4)
        plt.plot(data_by_year[shifts[1]].month,
                 data_by_year[shifts[1]].bits_in_rock,
                 marker='D', markersize=4)
        plt.legend(['коронки, см.1', 'коронки, см.2',
                    'коронки в скале, см.1', 'коронки в скале, см.2'])
        plt.ylabel('количество, шт')
        plt.grid(b=True, linestyle='--', linewidth=0.5)
        plt.title('Истрачено коронок.')

    @classmethod
    def create_meters_by_bits(cls, data_by_year, shifts, bits):
        """Meters passed by one average bit."""
        meters_by_bits1 = data_by_year[shifts[0]].meters / bits[0]
        meters_by_bits2 = data_by_year[shifts[1]].meters / bits[1]
        plt.plot(data_by_year[shifts[0]].month, meters_by_bits1,
                 marker='D', markersize=4)
        plt.plot(data_by_year[shifts[1]].month, meters_by_bits2,
                 marker='D', markersize=4)
        plt.legend(['Смена 1', 'Смена 2'])
        plt.ylabel('метров / коронку')
        plt.xlabel('месяцы')
        plt.grid(b=True, linestyle='--', linewidth=0.5)
        plt.title('Проход одной коронки.')

    @classmethod
    def create_bits_by_thousand_rocks(cls, data_by_year, shifts, bits):
        """Bits by thousand rock mass."""
        bits_by_thousand_rocks1 = (
            bits[0] / (data_by_year[shifts[0]].rock_mass / 1000)
            )
        bits_by_thousand_rocks2 = (
            bits[1] / (data_by_year[shifts[1]].rock_mass / 1000)
            )
        plt.plot(data_by_year[shifts[0]].month, bits_by_thousand_rocks1,
                 marker='D', markersize=4)
        plt.plot(data_by_year[shifts[1]].month, bits_by_thousand_rocks2,
                 marker='D', markersize=4)
        plt.legend(['Смена 1', 'Смена 2'])
        plt.ylabel('коронок / 1000м\u00B3 горной массы')
        plt.xlabel('месяцы')
        plt.grid(b=True, linestyle='--', linewidth=0.5)
        plt.title('Коронок на тысячу кубов горной массы.')

    @classmethod
    def print_statistic_by_year(cls, data):
        """Showing all drill data"""
        with pd.option_context(
            'display.max_rows', None, 'display.max_columns', None
        ):
            print(data)

    def create_drill_report(self):
        """Create drill report"""
        main_report_results = self._check_if_report_avaliable()
        if main_report_results:
            print("Введите данные по инструменту:")
            self._input_other_stats(main_report_results)
            super().clear_screen()
            self._check_correctly_input()
        else:
            print("Наряд данной смены еще не сфомирован, отчет о расходе \
инструмента возможно сформировать только после оформления наряда.")

    def show_statistic_by_year(self):
        """Showing statistic about drill instrument."""
        year = input("Введите год: ")
        drill_data = super().load_data(self.drill_file)
        drill_data_year = []
        if isinstance(drill_data, pd.DataFrame):
            drill_data_year = list(drill_data.year)
        if year in drill_data_year:
            self._visualise_statistic(year)
        else:
            print("Отстутствует статистика за {} год".format(year))
