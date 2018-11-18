#!usr/bin/env python3
"""
Main career report
classes: MainReport:'add_brigad_bonus',
                    'add_delta_ktu_to_worker',
                    'check_number_in_range',
                    'choise_from_list',
                    'count_all_workers_in_report',
                    'count_result',
                    'count_sal_workers_and_drill',
                    'count_salary',
                    'count_totall',
                    'coutn_delta_ktu',
                    'create_ktu_list',
                    'create_short_name'
         Reports: '_add_worker_from_diff_shift',
                  'check_date_format',
                  '_check_if_report_exist',
                  'check_number_in_range',
                  'choise_from_list',
                  'clear_screen',
                  'confirm_deletion',
                  'create_report',
                  'create_workers_hours_list',
                  'delete_report',
                  'edit_main_report',
                  'edit_report',
                  'give_avaliable_to_edit',
                  'make_status_in_process',
                  'save_log_to_temp_file',
                  '_uncomplete_main_report',
                  'work_with_main_report'
"""

import pickle
import sys
import os
from pprint import pprint
from modules.workers_module import AllWorkers
from modules.absolyte_path_module import AbsolytePath


class MainReport:
    """
    Main career report.
    """
    def __init__(self, status, shift, date):
        self.status = {'status': status,
                       'shift': shift,
                       'date': date}
        # Avaliable statuses: '\033[91m[не завершен]\033[0m'
        #                     '\033[93m[в процессе]\033[0m'
        #                     '\033[92m[завершен]\033[0m'
        self.workers_showing = {
            'бух.': {
                'КТУ': {},
                'часы': {},
                'зарплата': {}
            },
            'факт': {
                'КТУ': {},
                'часы': {},
                'зарплата': {}
            }}
        self.result = {
            'машины второго сорта': 0,
            'шпурометры': 0,
            'категории': {'меньше 0.7': 0,
                          '0.7-1.5': 0,
                          'выше 1.5': 0},
            'погоризонтно': {'+108': 0,
                             '+114': 0,
                             '+120': 0,
                             '+126': 0,
                             '+132': 0}
            }
        self.bonuses = {'более 250 кубов': False,
                        'победа по критериям': False}
        self.rock_mass = {'+108': 0,
                          '+114': 0,
                          '+120': 0,
                          '+126': 0,
                          '+132': 0}
        self.totall = 0

    @classmethod
    def count_totall(cls, value_list):
        """Count totall hours"""
        totall = 0
        for worker in value_list:
            totall += value_list[worker]
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

    @classmethod
    def create_short_name(cls, name):
        """Create short worker name."""
        n_m = name.split(' ')
        short_name = n_m[0] + ' ' + n_m[1][0] + '.' + n_m[2][0] + '.'
        return short_name

    def __str__(self):
        """Print main report"""
        output = "\n{date} {shift} {status}".format(**self.status)
        output += ("""\n
машины второго сорта: {0[машины второго сорта]}
шпурометры: {0[шпурометры]}\n""".format(self.result) +
                   """\nкубатура:
меньше 0.7: {0[меньше 0.7]}
0.7-1.5: {0[0.7-1.5]}
выше 1.5: {0[выше 1.5]}\n""".format(self.result['категории']))
        by_horisont = {
            key: value for (key, value) in self.result['погоризонтно'].items()
            if value > 0}
        output += "\nпогоризонтный выход блоков:\n"
        for horizont in by_horisont:
            output += horizont + ': ' + str(by_horisont[horizont]) + '\n'
        if self.status['status'] == '\033[91m[не завершен]\033[0m':
            output += '\n'
            for name in sorted(self.workers_showing['факт']['часы']):
                short_name = self.create_short_name(name)
                output += "{:<14}: {}\n".format(
                    short_name, self.workers_showing['факт']['часы'][name])
            return output
        output += "\nГорная масса:\n"
        for gorizont in sorted(self.rock_mass):
            output += gorizont + ': ' + str(self.rock_mass[gorizont]) + '\n'
        output += '\nСумма к распределению: ' + str(self.totall) + '\n'
        if self.bonuses['более 250 кубов']:
            output += "\033[92m[Премия за 250]\033[0m\n"
        if self.bonuses['победа по критериям']:
            output += "\033[92m[Победа в соц. соревновании]\033[0m\n"
        output += "\n    ФИО       ф.часы ф.КТУ  ф.З/п б.часы б.КТУ   б.З/п\n"
        for name in sorted(self.workers_showing['бух.']['часы']):
            short_name = self.create_short_name(name)
            output += "{:<14}: {:^4} {:^5} {:^8} {:^4}  {:^5} {:^8}\n".format(
                short_name, self.workers_showing['факт']['часы'][name],
                self.workers_showing['факт']['КТУ'][name],
                self.workers_showing['факт']['зарплата'][name],
                self.workers_showing['бух.']['часы'][name],
                self.workers_showing['бух.']['КТУ'][name],
                self.workers_showing['бух.']['зарплата'][name])
        unofficial_workers = self.unofficial_workers()
        for name in unofficial_workers:
            short_name = self.create_short_name(name)
            output += "{:<14}: {:^4} {:^5} {:^8}\n".format(
                short_name, self.workers_showing['факт']['часы'][name],
                self.workers_showing['факт']['КТУ'][name],
                self.workers_showing['факт']['зарплата'][name])
        return output

    def unofficial_workers(self):
        """Return unofficial workers"""
        unofficial_workers = [
            worker for worker in self.workers_showing['факт']['часы']
            if worker not in self.workers_showing['бух.']['часы']
            ]
        return unofficial_workers

    def count_result(self):
        """Count totall stone result"""
        result = 0
        for item in self.result['категории']:
            result += self.result['категории'][item]
        if result > 250:
            self.bonuses['более 250 кубов'] = True

    def count_all_workers_in_report(self):
        """Apply action to all workers in report"""
        self.count_result()
        for direction in self.workers_showing:
            for worker in self.workers_showing[direction]['КТУ']:
                if ((worker.split(' ')[0] in Reports().salary_workers or
                     worker.split(' ')[0] in Reports().drillers) and
                        direction == 'факт'):
                    self.count_sal_workers_and_drill(worker)
                else:
                    self.count_salary(direction, worker)
                self.add_brigad_bonus(worker)

    def count_salary(self, direction, worker):
        """Count totall salary"""
        self.workers_showing[direction]['зарплата'][worker] = round(
            self.workers_showing[direction]['КТУ'][worker]
            * self.totall * 1.5
            / len(self.workers_showing[direction]['КТУ']), 2)

    def count_sal_workers_and_drill(self, worker):
        """Count sallary workers and drillers"""
        oklad = 0
        if worker.split(' ')[0] in Reports().salary_workers:
            oklad = (self.workers_showing['факт']['часы'][worker]
                     / 11 * 50000 / 15)
        elif worker.split(' ')[0] in Reports().drillers:
            oklad = (self.result['шпурометры'] * 36)
        if self.bonuses['более 250 кубов']:
            oklad += (5000 / 15 / 11
                      * self.workers_showing['факт']['часы'][worker])
        self.workers_showing['факт']['зарплата'][worker] = round(oklad, 2)

    def add_brigad_bonus(self, worker):
        """Add bonus if brigad win monthly challenge"""
        if self.bonuses['победа по критериям']:
            self.workers_showing['факт']['зарплата'][worker] += 3000

    def create_ktu_list(self):
        """Create ktu list"""
        for direction in self.workers_showing:
            totall_hours = self.count_totall(
                self.workers_showing[direction]['часы'])
            for worker in self.workers_showing[direction]['часы']:
                ktu = (
                    self.workers_showing[direction]['часы'][worker]
                    / totall_hours
                    * len(self.workers_showing[direction]['часы'])
                    )
                self.workers_showing[direction]['КТУ'][worker] = round(ktu, 2)
            self.coutn_delta_ktu(direction)

    def coutn_delta_ktu(self, direction):
        """Add delta ktu to worker"""
        totall_ktu = self.count_totall(self.workers_showing[direction]['КТУ'])
        delta_ktu = len(self.workers_showing[direction]['КТУ']) - totall_ktu
        delta_ktu = round(delta_ktu, 2)
        if delta_ktu != 0:
            print(f"\nВ процессе округления образовался остаток: {delta_ktu}")
            self.add_delta_ktu_to_worker(delta_ktu, direction)

    def add_delta_ktu_to_worker(self, delta, direction):
        """Add delta ktu to worker"""
        print('\n' + 'КТУ: ' + direction)
        workers_list = self.workers_showing[direction]['КТУ'].items()
        print("\nВыберете работника, которому хотите добавить остаток:")
        worker = self.choise_from_list(workers_list)
        worker_ktu = self.workers_showing[direction]['КТУ'][worker[0]]
        result = round(delta + worker_ktu, 2)
        self.workers_showing[direction]['КТУ'][worker[0]] = result
        print("Остаток добавлен.\n")
        print(direction)
        pprint(self.workers_showing[direction]['КТУ'])


class Reports:
    """
    Class to manage with reports.
    """

    def __init__(self, data_file=AbsolytePath('main_career_report')):

        self.data_file = data_file.get_absolyte_path()
        self.shifts = ['Смена 1', 'Смена 2']
        self.salary_workers = ['Кочерин', 'Кокорин', 'Ягонен',
                               'Никулин', 'Медведев', 'Фигурин']
        self.drillers = ['Краснов', 'Фролов']

    @classmethod
    def check_date_format(cls, date):
        """Check if date format correct"""
        date_numbers = date.split('-')
        correct = (date[4] == '-' and
                   date_numbers[0].isdigit() and
                   date_numbers[1].isdigit() and
                   int(date_numbers[1]) < 13 and
                   int(date_numbers[1]) > 0)
        return correct

    @classmethod
    def input_result(cls, report):
        """Input working result"""
        for item in report.result:
            if isinstance(report.result[item], dict):
                for sub_item in report.result[item]:
                    print(sub_item, end=': ')
                    report.result[item][sub_item] = float(input())
            else:
                print(item, end=': ')
                report.result[item] = float(input())
        return report

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
        print("\nВведите количество часов:")
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
        with open(file_path, 'a', encoding='utf-8') as temp_file:
            temp_file.write(log)

    @classmethod
    def clear_screen(cls):
        """Clear shell screen"""
        if sys.platform[:3] == 'win':
            os.system('cls')
        else:
            os.system('clear')

    def _load_data(self):
        """Load file from pickle"""
        with open(self.data_file, 'rb') as report_file:
            report_base = pickle.load(report_file)
        return report_base

    def _dump_data(self, report_base):
        """Dumb data to pickle."""
        with open(self.data_file, 'wb') as report_file:
            pickle.dump(report_base, report_file)

    def _add_worker_from_diff_shift(self, shift):
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

    def _check_if_report_exist(self, shift, date):
        """Check if report exist in base"""
        check = True
        report_file = self._load_data()
        for report in report_file:
            if shift in report and date in report:
                check = False
                print("Такой отчет уже существует.")
        return check

    def _uncomplete_main_report(self, report_name):
        """Uncomlete main report"""
        choise = input("Are you shure, you want to uncomplete report? Y/n: ")
        if choise.lower() == 'y':
            report_file = self._load_data()
            temp_report = report_file[report_name]
            temp_report.status['status'] = '\033[93m[в процессе]\033[0m'
            new_name = "{date} {shift} {status}".format(
                **temp_report.status)
            report_file[new_name] = temp_report
            report_file.pop(report_name, None)
            self._dump_data(report_file)
            self.save_log_to_temp_file(' --> ' + temp_report.status['status'])

    def give_avaliable_to_edit(self, *statuses):
        """Give reports that avaliable to edit"""
        avaliable_reports = []
        report_file = self._load_data()
        avaliable_reports = [report for status in statuses
                             for report in report_file
                             if status in report]
        return avaliable_reports

    def create_report(self):
        """Create New main report."""
        while True:
            date = input("Введите дату отчета в формате 2018-12: ")
            if not self.check_date_format(date):
                print("Введите дату корректно.")
                continue
            print("Выберете бригаду:")
            shift = self.choise_from_list(self.shifts)
            if self._check_if_report_exist(shift, date):
                break

        workers_list = AllWorkers().give_workers_from_shift(shift)
        print(shift)
        for worker in workers_list:
            print(worker)

        # Add additional workers from another shift.
        added_workers = self._add_worker_from_diff_shift(shift)
        workers_list.extend(added_workers)
        self.clear_screen()

        report = MainReport('\033[91m[не завершен]\033[0m', shift, date)
        workers_hours_list = self.create_workers_hours_list(workers_list)
        report.workers_showing['факт']['часы'] = workers_hours_list
        print("\nВведите результаты добычи бригады.")
        report = self.input_result(report)
        print("\nТабель бригады заполнен.\n")
        report_file = self._load_data()
        report_name = "{date} {shift} {status}".format(**report.status)
        report_file[report_name] = report
        self._dump_data(report_file)
        self.save_log_to_temp_file(report_name)

    def delete_report(self, report_name):
        """Delete report."""
        report_file = self._load_data()
        if self.confirm_deletion(report_name):
            report_file.pop(report_name, None)
            self._dump_data(report_file)
            self.save_log_to_temp_file(
                "\033[91m - report deleted. \033[0m")

    def edit_report(self):
        """
        Edition uncompleted report by user with 'master' accesse.
        """

        def change_hours(temp_report):
            """Change hours value."""
            print("Выберете работника для редактирования:")
            worker = self.choise_from_list(
                temp_report.workers_showing['факт']['часы'])
            new_hours = int(input("Введите новое значение часов: "))
            temp_report.workers_showing['факт']['часы'][worker] = new_hours
            return temp_report

        avaliable_reports = self.give_avaliable_to_edit(
            '[не завершен]')
        print("""\
Вам доступны для редактирования только отчеты со статусом: \
\033[91m[не завершен]\033[0m
Выберет отчет для редактирования:
""")
        report_name = self.choise_from_list(
            avaliable_reports, none_option=True)
        if report_name:
            self.save_log_to_temp_file(report_name)
        report_file = self._load_data()
        self.clear_screen()
        while report_name:
            temp_report = report_file[report_name]
            print(temp_report)
            edit_menu_dict = {
                'изменить часы': change_hours,
                'удалить отчет': self.delete_report,
                'изменить добычу': self.input_result,
                '[закончить редактирование]': 'break'
                }
            print("Выберете пункт для редактирования:")
            action_name = self.choise_from_list(edit_menu_dict)
            print()
            if action_name in ['[закончить редактирование]', '']:
                break
            elif action_name == 'удалить отчет':
                temp_report = edit_menu_dict[action_name](report_name)
                break
            temp_report = edit_menu_dict[action_name](temp_report)
            report_file[report_name] = temp_report
            self._dump_data(report_file)
            self.clear_screen()

    def work_with_main_report(self, current_user):
        """Finish MainReport"""
        report_file = self._load_data()
        print("Выберет отчет:")
        report_name = self.choise_from_list(report_file, none_option=True)
        if report_name:
            self.save_log_to_temp_file(report_name)
            if '[не завершен]' in report_name:
                self.make_status_in_process(report_name)
            elif '[завершен]' in report_name:
                print(report_file[report_name])
                if current_user['accesse'] == 'admin':
                    choise = input("""\
\033[91m[un]\033[0m Возвратить статус '\033[93m[в процессе]\033[0m'\n""")
                    if choise == 'un':
                        self._uncomplete_main_report(report_name)
            elif '[в процессе]' in report_name:
                self.edit_main_report(report_name)

    def edit_main_report(self, report_name):
        """
        Edition main report by boss or admin usser.
        """

        def enter_rock_mass(temp_report):
            """Enter rock_mass"""
            print("Введите горную массу:")
            for gorizont in sorted(temp_report.rock_mass):
                print(gorizont, end=': ')
                temp_report.rock_mass[gorizont] = float(input())
            return temp_report

        def enter_totall(temp_report):
            """Enter totall money"""
            temp_report.totall = float(input("Введите итоговую сумму: "))
            return temp_report

        def enter_bonus(temp_report):
            """Enter monthly bonus"""
            choise = input("Бригада победила в соревновании? Д/н: ")
            if choise.lower() == 'д':
                temp_report.bonuses['победа по критериям'] = True
            return temp_report

        def change_ktu(temp_report):
            """Manualy change worker KTU"""
            print("Выберете вид КТУ:")
            direction = self.choise_from_list(temp_report.workers_showing)
            print("Выберете работника:")
            ch_worker = self.choise_from_list(
                temp_report.workers_showing[direction]['КТУ'])
            new_ktu = float(input("Введите новое значение КТУ: "))
            delta = (temp_report.workers_showing[direction]['КТУ'][ch_worker]
                     - new_ktu)
            workers = len(temp_report.workers_showing[direction]['КТУ'])
            temp_report.workers_showing[direction]['КТУ'][ch_worker] = new_ktu
            for worker in temp_report.workers_showing[direction]['КТУ']:
                if worker != ch_worker:
                    temp_report.workers_showing[direction]['КТУ'][worker] = (
                        temp_report.workers_showing[direction]['КТУ'][worker]
                        + round(delta/(workers-1), 2))
            temp_report.coutn_delta_ktu(direction)
            return temp_report

        def complete_main_report(temp_report):
            """Complete main report"""
            choise = input("Вы уверены что хотите завершить отчет? Д/н: ")
            if choise.lower() == 'д':
                temp_report.count_all_workers_in_report()
                temp_report.status['status'] = '\033[92m[завершен]\033[0m'
                AllWorkers().add_salary_to_workers(
                    temp_report.workers_showing['факт']['зарплата'],
                    temp_report.status['date'],
                    temp_report.unofficial_workers()
                )
                self.save_log_to_temp_file(
                    ' --> ' + temp_report.status['status'])
            return temp_report

        report_file = self._load_data()
        while True:
            temp_report = report_file[report_name]
            print(temp_report)
            if '[завершен]' in report_name:
                break
            edit_menu_dict = {
                'ввести горную массу': enter_rock_mass,
                'ввести итоговую сумму': enter_totall,
                'ежемесячный бонус': enter_bonus,
                'изменить КТУ работника': change_ktu,
                'удалить отчет': self.delete_report,
                '\033[92mсформировать отчет\033[0m': complete_main_report,
                '[закончить редактирование]': 'break'
                }
            print("Выберете пункт для редактирования:")
            action_name = self.choise_from_list(edit_menu_dict)
            print()
            if action_name in ['[закончить редактирование]', '']:
                break
            elif action_name == 'удалить отчет':
                temp_report = edit_menu_dict[action_name](report_name)
                break
            temp_report = edit_menu_dict[action_name](temp_report)
            report_file.pop(report_name, None)
            report_name = "{date} {shift} {status}".format(
                **temp_report.status)
            report_file[report_name] = temp_report
            self._dump_data(report_file)
            self.clear_screen()

    def make_status_in_process(self, report_name):
        """Change status from 'not complete' to 'in process'"""
        report_file = self._load_data()
        print(report_file[report_name])
        tmp_report = report_file[report_name]
        print("Введите ОФИЦИАЛЬНЫЕ часы работы:")
        shift = tmp_report.status['shift']
        workers_list = AllWorkers().give_workers_from_shift(shift)
        workers_hours_list = self.create_workers_hours_list(workers_list)
        tmp_report.workers_showing['бух.']['часы'] = workers_hours_list
        self.clear_screen()
        tmp_report.create_ktu_list()
        tmp_report.count_all_workers_in_report()
        tmp_report.status['status'] = '\033[93m[в процессе]\033[0m'
        report_file.pop(report_name, None)
        new_name = "{date} {shift} {status}".format(**tmp_report.status)
        report_file[new_name] = tmp_report
        self._dump_data(report_file)
        self.save_log_to_temp_file(
            ' --> ' + tmp_report.status['status'])
        self.edit_main_report(new_name)
