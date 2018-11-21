#!/usr/bin/env python3
"""
Module that provide to analyse and visualise MainReport data.
classes: ReportAnalysis: result_analysis
"""

import sys
import os
from copy import deepcopy
from matplotlib import pyplot as plt
from matplotlib import rcParams as window_parametrs
from modules.main_career_report import Reports


class ReportAnalysis(Reports):
    """
    Class to anilise and visualisate data from reports.
    """
    def __init__(self):
        self.horizonts = ['+108', '+114', '+120', '+126', '+132']
        self.month_list = ['01', '02', '03', '04', '05', '06',
                           '07', '08', '09', '10', '11', '12']
        super().__init__()
        self.base = super()._load_data()
        self.result_by_horizont = {
            '+108': [],
            '+114': [],
            '+120': [],
            '+126': [],
            '+132': [],
            'totall': []
            }
        self.result_by_shift = {
            'Смена 1': [],
            'Смена 2': []
        }
        self.year_reports = {}

    @classmethod
    def clear_screen(cls):
        """Clear shell screen"""
        if sys.platform[:3] == 'win':
            os.system('cls')
        else:
            os.system('clear')

    @classmethod
    def count_persent(cls, rock_mass, result):
        """Count persent"""
        if rock_mass != 0:
            persent = round(result/rock_mass*100, 2)
        else:
            persent = 0
        return persent

    def _chose_year(self):
        """Chose avaliable year."""
        avaliable_years = {report.split(' ')[0].split('-')[0]
                           for report in self.base}
        return avaliable_years

    def _give_reports_by_year(self, year):
        """Give reports of current year from reports base"""
        for report in self.base:
            if year in report:
                self.year_reports[report] = self.base[report]

    def _data_print(self, year, data_dict):
        """Pretty data print"""
        output = "\033[92m" + year + ' год\n' + "\033[0m"
        output += "{:^100}\n".format('месяц')
        output += "           {}\n".format('     '.join(self.month_list))
        output += '-' * 94 + '\n'
        for item in sorted(data_dict):
            output += """\
{:<7}: |{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|\
{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|\

""".format(item, *data_dict[item])
        print(output)

    def result_analysis(self):
        """Analysis by result"""
        print("Выберете год:")
        year = super().choise_from_list(self._chose_year())
        self._give_reports_by_year(year)
        self.clear_screen()
        while True:
            data_type = {
                'Погоризонтная статистика': self._make_horizont_statistic,
                'Повахтовая статистика': self._make_shift_statistic
                }
            print("\nВыберете необходимый очет:")
            choise = super().choise_from_list(data_type, none_option=True)
            self.clear_screen()
            if choise in data_type:
                results_and_titles = data_type[choise]()
                self._data_print(year, results_and_titles[0])
                self._data_print(year, results_and_titles[2])
                self._two_plots_show(year, results_and_titles)

            elif not choise:
                break
            else:
                print("Нет такого варианта.")
                continue

    def _make_shift_statistic(self):
        """Make result and persent statistic by shift."""
        result1 = self._give_res_by_shift()
        title1 = 'Повахтовая добыча м\u00B3'
        result2 = self._give_persent_by_shift()
        title2 = 'Повахтовый выход, %'
        return (result1, title1, result2, title2)

    def _make_horizont_statistic(self):
        """Make result and persent statistic by horizont."""
        result1 = self._give_res_by_horiz()
        title1 = 'Погоризонтная добыча, м\u00B3'
        result2 = self._give_persent_by_horiz()
        title2 = 'Погоризонтный выход, %'
        return (result1, title1, result2, title2)

    def _two_plots_show(self, year, results_and_titles):
        """Combine two subplots"""
        window_parametrs['figure.figsize'] = [18.0, 8.0]
        window_parametrs['figure.dpi'] = 100
        window_parametrs['savefig.dpi'] = 100
        window_parametrs['font.size'] = 12
        window_parametrs['legend.fontsize'] = 'large'
        window_parametrs['figure.titlesize'] = 'large'
        plt.subplot(1, 2, 1)
        self._subplot_result(year, results_and_titles[:2])
        plt.subplot(1, 2, 2)
        self._subplot_result(year, results_and_titles[2:4])
        plt.show()

    def _subplot_result(self, year, results_and_titles):
        """visualise result."""
        # Count coefficient for annotations coordinate depend on scale.
        if results_and_titles[1].split(' ')[1] == 'добыча,':
            coef = 5
        else:
            coef = 0.1

        for item in sorted(results_and_titles[0]):
            plt.plot(self.month_list, results_and_titles[0][item],
                     marker='D', markersize=4)
            for point in zip(self.month_list, results_and_titles[0][item]):
                if point[1] != 0:
                    ann_text = str(point[1])
                    ann_coord = (point[0], point[1]+coef)
                    plt.annotate(ann_text, xy=ann_coord, fontsize='small')
        plt.legend(list(sorted(results_and_titles[0].keys())))
        plt.xlabel('месяц')
        plt.ylabel(results_and_titles[1].split(' ')[-1])
        plt.title(year + 'г., ' + results_and_titles[1])
        plt.grid(b=True, linestyle='--', linewidth=0.5)

    def _give_res_by_horiz(self):
        """Result by horizont"""
        result_lists = deepcopy(self.result_by_horizont)
        for month in self.month_list:
            for horizont in self.horizonts:
                horizont_sum = 0
                monthly_sum = 0
                for report in self.year_reports:
                    if report.split(' ')[0].split('-')[1] == month:
                        horizont_sum += (
                            self.base[report].result['погоризонтно'][horizont])
                        monthly_sum += self.base[report].count_result()
                result_lists[horizont].append(round(horizont_sum, 2))
            result_lists['totall'].append(round(monthly_sum, 2))
        return result_lists

    def _give_persent_by_horiz(self):
        """Persent by horizont"""
        result_lists = deepcopy(self.result_by_horizont)
        for month in self.month_list:
            for horizont in self.horizonts:
                horizont_sum = 0
                monthly_sum = 0
                rock_mass_month = 0
                rock_mass_horizont = 0
                for report in self.year_reports:
                    if report.split(' ')[0].split('-')[1] == month:
                        horizont_sum += (
                            self.base[report].result['погоризонтно'][horizont])
                        rock_mass_horizont += (
                            self.base[report].rock_mass[horizont])
                        monthly_sum += self.base[report].count_result()
                        rock_mass_month += self.base[report].count_rock_mass()
                persent = self.count_persent(rock_mass_horizont, horizont_sum)
                result_lists[horizont].append(persent)
            persent = self.count_persent(rock_mass_month, monthly_sum)
            result_lists['totall'].append(persent)
        return result_lists

    def _give_res_by_shift(self):
        """Give result by shift."""
        result_lists = deepcopy(self.result_by_shift)
        for month in self.month_list:
            for shift in self.result_by_shift:
                shift_sum = 0
                for report in self.year_reports:
                    report_month = report.split(' ')[0].split('-')[1]
                    report_shift = self.base[report].status['shift']
                    if shift == report_shift and report_month == month:
                        shift_sum += self.base[report].count_result()
                result_lists[shift].append(shift_sum)
        return result_lists

    def _give_persent_by_shift(self):
        """Give persent by shift."""
        result_lists = deepcopy(self.result_by_shift)
        for month in self.month_list:
            for shift in self.result_by_shift:
                shift_sum = 0
                rock_mass_shift = 0
                for report in self.year_reports:
                    report_month = report.split(' ')[0].split('-')[1]
                    report_shift = self.base[report].status['shift']
                    if shift == report_shift and report_month == month:
                        shift_sum += self.base[report].count_result()
                        rock_mass_shift += self.base[report].count_rock_mass()
                persent = self.count_persent(rock_mass_shift, shift_sum)
                result_lists[shift].append(persent)
        return result_lists
