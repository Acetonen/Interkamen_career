#!usr/bin/env python3
"""Main career report"""

import shelve
from pprint import pprint
from modules.workers_module import AllWorkers
from modules.absolyte_path_module import AbsolytePath


class MainReport:
    """Main career report"""
    def __init__(self, date, status):
        self.date = date
        self.status = status
        self.delta_ktu = 0
        self.ktu_list = {}
        self.drill = 0


class Reports:
    """Class to manage with reports"""
    def __init__(self, data_file=AbsolytePath('main_career_report')):

        self.data_file = data_file.get_absolyte_path()
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
        report = MainReport(date, '\033[91m[не завершен]\033[0m')

        shifts = ['Смена 1', 'Смена 2']
        print("Выберете бригаду:")
        shift = self.choise_from_list(shifts)
        workers_list = AllWorkers().give_workers_from_shift(shift)
        print(shift)
        for worker in workers_list:
            print(worker)

        # Add additional workers from enother shift.
        shifts.remove(shift)
        added_workers = self.add_worker_from_diff_shift(shifts[0])
        workers_list.extend(added_workers)

        workers_hours, totall_hours = self.create_workers_hours_list(
            workers_list)

        report.drill = float(input("Ведите колличество пробуренных метров:"))
        print("\nТабель бригады заполнен.\n")

        report.ktu_list, totall_ktu = self.create_ktu_list(
            workers_hours, totall_hours)
        report.delta_ktu = len(workers_list) - totall_ktu

        with shelve.open(self.data_file) as report_file:
            report_file[date + '\033[91m [не завершен]\033[0m'] = report

    def edit_report(self, current_user):
        """Edit report."""
        pass  # TODO: finish

    def delete_report(self, current_user):
        """Delete report."""
        pass  # TODO: finish

    def show_all_reports(self):
        """Show all reports in base"""
        with shelve.open(self.data_file) as report_file:
            for report in sorted(report_file):
                print(report)

    @classmethod
    def create_ktu_list(cls, workers_hours, totall_hours):
        """Create ktu list"""
        ktu_list = {}
        totall_ktu = 0
        for worker in workers_hours:
            ktu = workers_hours[worker] / totall_hours * len(workers_hours)
            ktu_list[worker] = round(ktu, 2)
            totall_ktu += ktu_list[worker]
        return ktu_list, totall_ktu

    @classmethod
    def create_workers_hours_list(cls, workers_list):
        """Create workers hous list."""
        print("\nВведите колличество отработанных часов.")
        workers_hours = {}
        totall_hours = 0
        for worker in workers_list:
            print(worker, end="")
            hours = input('; часов: ')
            totall_hours += int(hours)
            workers_hours[worker] = int(hours)
        return workers_hours, totall_hours

    def add_worker_from_diff_shift(self, different_shift):
        """Add worker from different shift to current."""
        added_workers = []
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
    def choise_from_list(cls, variants_list):
        """Chose variant from list."""
        sort_list = sorted(variants_list)
        for index, item in enumerate(sort_list, 1):
            print("\t[{}] - {}".format(index, item))
        while True:
            choise = input()
            if cls.check_number_in_range(choise, len(sort_list)):
                chosen_item = sort_list[int(choise)-1]
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
