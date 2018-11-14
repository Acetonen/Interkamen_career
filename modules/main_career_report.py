#!usr/bin/env python3
"""Main career report"""

import shelve
import sys
import os
from pprint import pprint
from modules.workers_module import AllWorkers
from modules.absolyte_path_module import AbsolytePath


class MainReport:
    """Main career report"""
    def __init__(self, status):
        self.status = status
        # Avaliable statuses: '\033[91m[не завершен]\033[0m'
        #                     '\033[93m[в процессе]\033[0m'
        #                     '\033[92m[завершен]\033[0m'
        self.drill = 0
        self.workers_hours = {'бухгалтерия': {},
                              'факт': {}}
        self.ktu_list = {'бухгалтерия': {},
                         'факт': {}}

    def create_ktu_list(self, version):
        """Create ktu list"""
        self.ktu_list[version] = {}
        totall_hours = self.count_totall(self.workers_hours, version)
        for worker in self.workers_hours[version]:
            ktu = (
                self.workers_hours[version][worker]
                / totall_hours
                * len(self.workers_hours[version])
                )
            self.ktu_list[version][worker] = round(ktu, 2)

    def coutn_delta_ktu(self, version):
        """Add delta ktu to worker"""
        totall_ktu = self.count_totall(self.ktu_list, version)
        delta_ktu = len(self.ktu_list[version]) - totall_ktu
        print(f"В процессе округления образовался остаток: {delta_ktu}")
        return delta_ktu

    def add_delta_ktu_to_worker(self, delta, version):
        """Add delta ktu to worker"""
        print("Выберете работника, которому хотите добавить остаток:")
        worker = self.choise_from_list(self.ktu_list[version])
        self.ktu_list[version][worker] += delta
        print("Остаток добавлен.")
        print(version)
        pprint(self.ktu_list[version])

    @classmethod
    def count_totall(cls, value_list, version):
        """Count totall hours"""
        totall = 0
        for worker in value_list[version]:
            totall += value_list[version][worker]
        return totall

    @classmethod
    def choise_from_list(cls, variants_list, none_option=False):
        """Chose variant from list."""
        sort_list = sorted(variants_list)
        for index, item in enumerate(sort_list, 1):
            print("\t[{}] - {}".format(index, item))
        while True:
            choise = input()
            if choise == '' and none_option:
                chosen_item = None
                break
            elif cls.check_number_in_range(choise, len(sort_list)):
                chosen_item = sort_list[int(choise)-1]
                break
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


class Reports:
    """Class to manage with reports"""
    def __init__(self, data_file=AbsolytePath('main_career_report')):

        self.data_file = data_file.get_absolyte_path()
        self.shifts = ['Смена 1', 'Смена 2']
        self.salary_workers = {
            'Смена 1': ['Зинкович', 'Кочерин', 'Кокорин', 'Ягонен'],
            'Смена 2': ['Никулин', 'Медведев', 'Фигурин']
        }
        self.drillers = {
            'Смена 1': ['Краснов'],
            'Смена 2': ['Фролов']
        }

    def create_report(self):
        """Create New main report."""
        date = input("Введите дату отчета в формате 2018-12: ")
        # TODO: check data format
        print("Выберете бригаду:")
        shift = self.choise_from_list(self.shifts)
        workers_list = AllWorkers().give_workers_from_shift(shift)
        print(shift)
        for worker in workers_list:
            print(worker)

        # Add additional workers from another shift.
        added_workers = self.add_worker_from_diff_shift(shift)
        workers_list.extend(added_workers)

        report = MainReport('\033[91m[не завершен]\033[0m')
        workers_hours_list = self.create_workers_hours_list(workers_list)
        report.workers_hours['факт'] = workers_hours_list
        report.drill = float(input("\nВедите колличество пробуренных метров:"))
        print("\nТабель бригады заполнен.\n")
        with shelve.open(self.data_file) as report_file:
            report_file[date + ' ' + report.status] = report
        self.save_log_to_temp_file(
            "\033[92m" + date + ' ' + report.status + "\033[0m")

    def edit_report(self):
        """Edit report."""

        def delete_report(report):
            """Delete worker."""
            if self.confirm_deletion(report):
                report_file.pop(report, None)
                self.save_log_to_temp_file(
                    "\033[91m - report deleted. \033[0m")

        def change_drill(temp_report):
            """Change drill value."""
            new_drill = input("Введите новое значение метров: ")
            temp_report.drill = float(new_drill)
            return temp_report

        def change_hours(temp_report):
            """Change hours value."""
            print("Выберете работника для редактирования:")
            worker = self.choise_from_list(temp_report.workers_hours['факт'])
            new_hours = input("Введите новое значение часов:")
            temp_report.workers_hours['факт'][worker] = int(new_hours)
            return temp_report

        avaliable_reports = self.give_avaliable_to_edit()
        print("""\
Вам доступны для редактирования только отчеты со статусом: \
\033[91m[не завершен]\033[0m
Выберет отчет для редактирования:
""")
        report = self.choise_from_list(avaliable_reports, none_option=True)
        if report:
            self.save_log_to_temp_file(report)
        report_file = shelve.open(self.data_file)
        self.clear_screen()
        while report:
            temp_report = report_file[report]
            print(report)
            pprint(temp_report.workers_hours['факт'])
            print('\nКолличество шпурометров:', temp_report.drill, '\n')
            edit_menu_dict = {
                'изменить часы': change_hours,
                'изменить пробуренные метры': change_drill,
                'удалить отчет': delete_report,
                '[закончить редактирование]': 'break'
                }
            print("Выберете пункт для редактирования:")
            action_name = self.choise_from_list(edit_menu_dict)

            print()
            if action_name in ['[закончить редактирование]', '']:
                break
            elif action_name == 'удалить отчет':
                temp_report = edit_menu_dict[action_name](report)
                break

            temp_report = edit_menu_dict[action_name](temp_report)

            report_file[report] = temp_report
            self.clear_screen()
        report_file.close()

    def give_avaliable_to_edit(self):
        """Give reports that avaliable to edit"""
        avaliable_reports = []
        with shelve.open(self.data_file) as report_file:
            for report in report_file:
                if '\033[91m[не завершен]\033[0m' in report:
                    avaliable_reports.append(report)
        return avaliable_reports

    def show_all_reports(self):
        """Show all reports in base"""
        with shelve.open(self.data_file) as report_file:
            for report in sorted(report_file):
                print(report)

    def add_worker_from_diff_shift(self, shift):
        """Add worker from different shift to current."""
        added_workers = []
        self.shifts.remove(shift)
        different_shift = self.shifts[0]
        other_shift_workers = (
            AllWorkers().give_workers_from_shift(different_shift))
        while True:
            add_worker = input(
                "\nДобавить работника из другой бригады? д/н: ")
            if add_worker == 'д':
                worker = self.choise_from_list(other_shift_workers)
                print(worker, '- добавлен.')
                added_workers.append(worker)
                other_shift_workers.remove(worker)
            elif add_worker == 'н':
                return added_workers
            else:
                print("Введите 'д' или 'н'.")

    @classmethod
    def confirm_deletion(cls, item):
        """Action conformation"""
        confirm = input(
            "Вы уверены что хотите удалить '{}'? Д/н: ".format(item))
        if confirm.lower() == 'д':
            confirm = True
            print("\033[91m'{}' - удален. \033[0m".format(item))
        else:
            confirm = False
            print("\nВы отменили удаление.\n")
        return confirm

    @classmethod
    def create_workers_hours_list(cls, workers_list):
        """Create workers hous list."""
        print("\nВведите колличество отработанных часов:")
        workers_hours = {}
        for worker in workers_list:
            print(worker, end="")
            hours = input('; часов: ')
            workers_hours[worker] = int(hours)
        return workers_hours

    @classmethod
    def choise_from_list(cls, variants_list, none_option=False):
        """Chose variant from list."""
        sort_list = sorted(variants_list)
        for index, item in enumerate(sort_list, 1):
            print("\t[{}] - {}".format(index, item))
        while True:
            choise = input()
            if choise == '' and none_option:
                chosen_item = None
                break
            elif cls.check_number_in_range(choise, len(sort_list)):
                chosen_item = sort_list[int(choise)-1]
                break
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

    @classmethod
    def clear_screen(cls):
        """Clear shell screen"""
        if sys.platform == 'win':
            os.system('cls')
        else:
            os.system('clear')
