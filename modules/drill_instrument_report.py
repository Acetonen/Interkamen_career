#!/usr/bin/env python3
"""
Working with statistic of drill instrument.
"""

import os
from matplotlib import pyplot as plt
from matplotlib import rcParams as window_parametrs
import pandas as pd
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.main_career_report import Reports
from modules.support_modules.standart_functions import BasicFunctions


class DrillInstruments(BasicFunctions):
    """
    All information about drill instruments.
    """
    drill_path = AbsolytePath('drill_instruments').get_absolyte_path()
    month_list = ['01', '02', '03', '04', '05', '06',
                  '07', '08', '09', '10', '11', '12']
    drill_data = {}

    def __init__(self):
        if os.path.exists(self.drill_path):
            self.drill_file = super().load_data(self.drill_path)
        else:
            self.drill_file = pd.DataFrame(self.drill_data, index=[0])
            super().dump_data(self.drill_path, self.drill_file)

    @classmethod
    def create_meters_by_month(cls, figure, data_by_year, shifts):
        """Totall drill meters in month by each shift."""
        met_bu_mon = figure.add_subplot(221)
        met_bu_mon.plot(data_by_year[shifts[0]].month,
                        data_by_year[shifts[0]].meters,
                        marker='D', markersize=4)
        met_bu_mon.plot(data_by_year[shifts[1]].month,
                        data_by_year[shifts[1]].meters,
                        marker='D', markersize=4)
        met_bu_mon.legend(['Смена 1', 'Смена 2'])
        met_bu_mon.set_ylabel('шпурометры, м.')
        met_bu_mon.grid(b=True, linestyle='--', linewidth=0.5)
        met_bu_mon.set_title('Пробурено за смену.')

    @classmethod
    def create_all_bits(cls, figure, data_by_year, shifts, bits):
        """Totall used bits by shift and bits in rock."""
        all_bits = figure.add_subplot(222)
        all_bits.plot(data_by_year[shifts[0]].month, bits[0],
                      marker='D', markersize=4)
        all_bits.plot(data_by_year[shifts[1]].month, bits[1],
                      marker='D', markersize=4)
        all_bits.plot(data_by_year[shifts[0]].month,
                      data_by_year[shifts[0]].bits_in_rock,
                      marker='D', markersize=4)
        all_bits.plot(data_by_year[shifts[1]].month,
                      data_by_year[shifts[1]].bits_in_rock,
                      marker='D', markersize=4)
        all_bits.legend(['коронки, см.1', 'коронки, см.2',
                         'коронки в скале, см.1', 'коронки в скале, см.2'])
        all_bits.set_ylabel('количество, шт')
        all_bits.grid(b=True, linestyle='--', linewidth=0.5)
        all_bits.set_title('Истрачено коронок.')

    @classmethod
    def create_meters_by_bits(cls, figure, data_by_year, shifts, bits):
        """Meters passed by one average bit."""
        met_by_bit = figure.add_subplot(223)
        meters_by_bits1 = data_by_year[shifts[0]].meters / bits[0]
        meters_by_bits2 = data_by_year[shifts[1]].meters / bits[1]
        met_by_bit.plot(data_by_year[shifts[0]].month, meters_by_bits1,
                        marker='D', markersize=4)
        met_by_bit.plot(data_by_year[shifts[1]].month, meters_by_bits2,
                        marker='D', markersize=4)
        met_by_bit.legend(['Смена 1', 'Смена 2'])
        met_by_bit.set_ylabel('метров / коронку')
        met_by_bit.set_xlabel('месяцы')
        met_by_bit.grid(b=True, linestyle='--', linewidth=0.5)
        met_by_bit.set_title('Проход одной коронки.')

    @classmethod
    def create_bits_by_thousand_rocks(cls, figure, data_by_year, shifts, bits):
        """Bits by thousand rock mass."""
        bit_by_rock = figure.add_subplot(224)
        bits_by_thousand_rocks1 = (
            bits[0] / (data_by_year[shifts[0]].rock_mass / 1000)
            )
        bits_by_thousand_rocks2 = (
            bits[1] / (data_by_year[shifts[1]].rock_mass / 1000)
            )
        bit_by_rock.plot(data_by_year[shifts[0]].month,
                         bits_by_thousand_rocks1,
                         marker='D', markersize=4)
        bit_by_rock.plot(data_by_year[shifts[1]].month,
                         bits_by_thousand_rocks2,
                         marker='D', markersize=4)
        bit_by_rock.legend(['Смена 1', 'Смена 2'])
        bit_by_rock.set_ylabel('коронок / 1000м\u00B3 горной массы')
        bit_by_rock.set_xlabel('месяцы')
        bit_by_rock.grid(b=True, linestyle='--', linewidth=0.5)
        bit_by_rock.set_title('Коронок на тысячу кубов горной массы.')

    @classmethod
    def print_statistic_by_year(cls, data):
        """Showing all drill data"""
        with pd.option_context(
            'display.max_rows', None, 'display.max_columns', None
        ):
            print(data)

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

            self.drill_file = self.drill_file.append(self.drill_data,
                                                     ignore_index=True)
            super().dump_data(self.drill_path, self.drill_file)

            print("Отчет по инструменту создан.")
            super().save_log_to_temp_file(
                '{}-{}-{}\033[94m created\033[0m'.format(
                    self.drill_data['year'],
                    self.drill_data['month'],
                    self.drill_data['shift'])
                )

    def _visualise_statistic(self, year):
        """Visualise statistic."""
        drill_year = self.drill_file.year == year
        data_by_year = self.drill_file[drill_year].sort_values(by=['month'])
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

        figure = plt.figure()
        suptitle = figure.suptitle("Отчет по буровому инструменту.",
                                   fontsize="x-large")
        self.create_meters_by_month(figure, data_by_year, shifts)
        self.create_all_bits(figure, data_by_year, shifts, bits)
        self.create_meters_by_bits(figure, data_by_year, shifts, bits)
        self.create_bits_by_thousand_rocks(figure, data_by_year, shifts, bits)

        figure.tight_layout()
        suptitle.set_y(0.95)
        figure.subplots_adjust(top=0.85)
        plt.show()

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
        drill_data_year = []
        if isinstance(self.drill_file, pd.DataFrame):
            drill_data_year = list(self.drill_file.year)
        if year in drill_data_year:
            self._visualise_statistic(year)
        else:
            print("Отстутствует статистика за {} год".format(year))
