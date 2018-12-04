#!/usr/bin/env python3
"""
Main career report.
This module for create main career report by 'master' and complate it by 'boss'
users.
It can count worker salary and compilate statistic of brigades results.

class Reports :
 'brigadiers_path', - path to brigadier database.
 'check_comma_error', - check error for wrong result input (if comma in FPN).
 'check_date_format', - check correct date format.
 'choose_salary_or_drillers', - edit salary, drillers or brigadiers workers.
 'create_report', - create main report.
 'create_workers_hours_list', - input workers hours.
 'data_path', - path to main reports database.
 'drillers_path', - path to drillers database.
 'edit_report', - edit main report.
 'give_avaliable_to_edit', - give reports, avaliable to edit.
 'give_main_results', - give main results.
 'salary_path', - path to salary workers database.
 'shifts', - shifts list.
 'work_with_main_report' - complete main report.
"""

from pprint import pprint
from modules.workers_module import AllWorkers
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.backup import make_backup


class MainReport(BasicFunctions):
    """
    Main career report.
    """
    workers_showing = {
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
    result = {
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
    bonuses = {'более 250 кубов': False,
               'победа по критериям': False}
    rock_mass = {'+108': 0,
                 '+114': 0,
                 '+120': 0,
                 '+126': 0,
                 '+132': 0}
    totall = 0

    def __init__(self, status, shift, date):
        self.status = {'status': status,
                       'shift': shift,
                       'date': date}
        # Avaliable statuses: '\033[91m[не завершен]\033[0m'
        #                     '\033[93m[в процессе]\033[0m'
        #                     '\033[92m[завершен]\033[0m'

    @classmethod
    def count_totall(cls, value_list):
        """Count totall hours"""
        totall = 0
        for worker in value_list:
            totall += value_list[worker]
        return totall

    @classmethod
    def create_short_name(cls, name):
        """Create short worker name."""
        n_m = name.split(' ')
        short_name = n_m[0] + ' ' + n_m[1][0] + '.' + n_m[2][0] + '.'
        return short_name

    @classmethod
    def _colorise_salary_and_drillers(cls, name, output):
        """Colorise sallary and drillers in report output."""
        if name in Reports().salary_workers or name in Reports().drillers:
            output = ''.join(['\033[36m', output, '\033[0m'])
        return output

    @classmethod
    def _colorise_brigadiers(cls, name, output):
        """Colorise sallary and drillers in report output."""
        if name in Reports().brigadiers:
            if '\033[36m' in output:
                output = output.replace('\033[36m', '\033[91m')
            else:
                output = ''.join(['\033[91m', output, '\033[0m'])
        return output

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
        output += "                   \
Фактические               Бухгалтерские"
        output += "\n    ФИО         часы   КТУ       З/п     |\
 часы   КТУ      З/п\n"
        for name in sorted(self.workers_showing['бух.']['часы']):
            short_name = self.create_short_name(name)
            t_output = (
                "{:<14}: {:>3} | {:>4} | {:<9,}р. | ".format(
                    short_name,
                    self.workers_showing['факт']['часы'][name],
                    self.workers_showing['факт']['КТУ'][name],
                    self.workers_showing['факт']['зарплата'][name],
                )
                + "{:>3} | {:>4} | {:<9,}р.\n".format(
                    self.workers_showing['бух.']['часы'][name],
                    self.workers_showing['бух.']['КТУ'][name],
                    self.workers_showing['бух.']['зарплата'][name]
                )
            )
            t_output = self._colorise_salary_and_drillers(name, t_output)
            t_output = self._colorise_brigadiers(name, t_output)
            output += t_output
        unofficial_workers = self.unofficial_workers()
        for name in unofficial_workers:
            short_name = self.create_short_name(name)
            t_output = "{:<14}: {:>3} | {:>4} | {:<9,}\n".format(
                short_name, self.workers_showing['факт']['часы'][name],
                self.workers_showing['факт']['КТУ'][name],
                self.workers_showing['факт']['зарплата'][name])
            t_output = self._colorise_salary_and_drillers(name, t_output)
            t_output = self._colorise_brigadiers(name, t_output)
            output += t_output
        return output

    def _count_salary(self, direction, worker, coefficient):
        """Count totall salary"""
        self.workers_showing[direction]['зарплата'][worker] = round(
            self.workers_showing[direction]['КТУ'][worker]
            * self.totall * coefficient
            / len(self.workers_showing[direction]['КТУ']), 2)

    def _count_sal_workers_and_drill(self, worker):
        """Count sallary workers and drillers"""
        oklad = 0
        if worker in Reports().salary_workers:
            oklad = (self.workers_showing['факт']['часы'][worker]
                     / 11 * 50000 / 15)
        elif worker in Reports().drillers:
            oklad = (self.result['шпурометры'] * 36)
        if self.bonuses['более 250 кубов']:
            oklad += (5000 / 15 / 11
                      * self.workers_showing['факт']['часы'][worker])
        self.workers_showing['факт']['зарплата'][worker] = round(oklad, 2)

    def _add_brigad_bonus(self, worker):
        """Add bonus if brigad win monthly challenge"""
        if self.bonuses['победа по критериям']:
            self.workers_showing['факт']['зарплата'][worker] += 3000

    def _add_brigadiers_persent(self, worker, direction):
        """Add persent if worker are brigadier."""
        if worker in Reports().brigadiers:
            oklad = self.workers_showing[direction]['зарплата'][worker] * 1.1
            self.workers_showing[direction]['зарплата'][worker] = round(
                oklad, 2)

    def _add_delta_ktu_to_worker(self, delta, direction):
        """Add delta ktu to worker"""
        print('\n' + 'КТУ: ' + direction)
        workers_list = self.workers_showing[direction]['КТУ'].items()
        print("\nВыберете работника, которому хотите добавить остаток:")
        worker = super().choise_from_list(workers_list)
        worker_ktu = self.workers_showing[direction]['КТУ'][worker[0]]
        result = round(delta + worker_ktu, 2)
        self.workers_showing[direction]['КТУ'][worker[0]] = result
        print("Остаток добавлен.\n")
        print(direction)
        pprint(self.workers_showing[direction]['КТУ'])

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
        return result

    def count_rock_mass(self):
        """Count totall rock_mass"""
        result = 0
        for item in self.rock_mass:
            result += self.rock_mass[item]
        return result

    def count_all_workers_in_report(self):
        """Apply action to all workers in report"""
        self.count_result()
        for direction in self.workers_showing:
            for worker in self.workers_showing[direction]['КТУ']:
                if ((worker in Reports().salary_workers or
                     worker in Reports().drillers) and
                        direction == 'факт'):
                    self._count_sal_workers_and_drill(worker)
                elif direction == 'бух.':
                    coefficient = 1
                    self._count_salary(direction, worker, coefficient)
                elif direction == 'факт':
                    coefficient = 1.5
                    self._count_salary(direction, worker, coefficient)
                self._add_brigad_bonus(worker)
                self._add_brigadiers_persent(worker, direction)

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
            self._add_delta_ktu_to_worker(delta_ktu, direction)


class Reports(BasicFunctions):
    """
    Class to manage with reports.
    """

    shifts = ['Смена 1', 'Смена 2']
    data_path = AbsolytePath('main_career_report').get_absolyte_path()
    salary_path = AbsolytePath('salary_worker').get_absolyte_path()
    drillers_path = AbsolytePath('drillers').get_absolyte_path()
    brigadiers_path = AbsolytePath('brigadiers').get_absolyte_path()

    def __init__(self):
        self.salary_workers = super().load_data(self.salary_path)
        self.drillers = super().load_data(self.drillers_path)
        self.brigadiers = super().load_data(self.brigadiers_path)
        self.data_base = super().load_data(self.data_path)

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
    def check_comma_error(cls):
        """Check input floats for commas."""
        while True:
            inpt = input()
            if ',' in inpt or inpt == '':
                print("Некорректный ввод, повторите:", end='')
            else:
                return inpt

    def _input_result(self, report):
        """Input working result"""
        for item in report.result:
            if isinstance(report.result[item], dict):
                for sub_item in report.result[item]:
                    print(sub_item, end=': ')
                    inpt = self.check_comma_error()
                    report.result[item][sub_item] = float(inpt)
            else:
                print(item, end=': ')
                inpt = self.check_comma_error()
                report.result[item] = float(inpt)
        return report

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
                worker = super().choise_from_list(other_shift_workers)
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
        for report in self.data_base:
            if shift in report and date in report:
                check = False
                print("Такой отчет уже существует.")
        return check

    def _uncomplete_main_report(self, report_name):
        """Uncomlete main report"""
        choise = input("Are you shure, you want to uncomplete report? Y/n: ")
        if choise.lower() == 'y':
            tmp_rpt = self.data_base[report_name]
            tmp_rpt.status['status'] = '\033[93m[в процессе]\033[0m'
            new_name = "{date} {shift} {status}".format(
                **tmp_rpt.status)
            self.data_base[new_name] = tmp_rpt
            self.data_base.pop(report_name, None)
            super().dump_data(self.data_path, self.data_base)
            super().save_log_to_temp_file(
                ' --> ' + tmp_rpt.status['status'])

    def _delete_report(self, report_name):
        """Delete report."""
        if super().confirm_deletion(report_name):
            self.data_base.pop(report_name, None)
            super().dump_data(self.data_path, self.data_base)
            super().save_log_to_temp_file(
                "\033[91m - report deleted. \033[0m")

    def _edit_salary_or_drillers(self, data_path):
        """Edit sallary or drillers lists."""

        def add_salary_or_driller(data_path):
            """Add worker from salary or driller list."""
            worker_list = super(Reports, self).load_data(data_path)
            if not worker_list:
                worker_list = []
            print("Выберете работника:")
            worker = super(Reports, self).choise_from_list(
                AllWorkers().give_mining_workers(), none_option=True
            )
            if worker:
                worker_list.append(worker)
                super(Reports, self).dump_data(data_path, worker_list)
                log = " worker {} aded".format(worker)
                print(log)
                super(Reports, self).save_log_to_temp_file(log)

        def delete_salary_or_driller(data_path):
            """Delete worker from salary or driller list."""
            worker_list = super(Reports, self).load_data(data_path)
            if not worker_list:
                worker_list = []
            print("Выберете работника для удаления:")
            worker = super(Reports, self).choise_from_list(
                worker_list, none_option=True)
            if worker:
                worker_list.remove(worker)
                super(Reports, self).dump_data(data_path, worker_list)
                log = " worker {} deleted".format(worker)
                print(log)
                super(Reports, self).save_log_to_temp_file(log)

        super().clear_screen()
        while True:
            worker_list = super(Reports, self).load_data(data_path)
            print("Работники в данной группе:")
            for worker in worker_list:
                print('\t', worker)
            edit_menu_dict = {'д': add_salary_or_driller,
                              'у': delete_salary_or_driller}
            action_name = input("Добавить или удалить работника (д/у): ")
            if action_name not in edit_menu_dict:
                print("Вы отменили редактирование.")
                break
            else:
                edit_menu_dict[action_name](data_path)

    def _edit_main_report(self, report_name):
        """
        Edition main report by boss or admin usser.
        """

        def enter_rock_mass(tmp_rpt):
            """Enter rock_mass"""
            print("Введите горную массу:")
            for gorizont in sorted(tmp_rpt.rock_mass):
                print(gorizont, end=': ')
                tmp_rpt.rock_mass[gorizont] = float(input())
            return tmp_rpt

        def enter_totall(tmp_rpt):
            """Enter totall money"""
            tmp_rpt.totall = float(input("Введите итоговую сумму: "))
            return tmp_rpt

        def enter_bonus(tmp_rpt):
            """Enter monthly bonus"""
            choise = input("Бригада победила в соревновании? Д/н: ")
            if choise.lower() == 'д':
                tmp_rpt.bonuses['победа по критериям'] = True
            return tmp_rpt

        def change_ktu(tmp_rpt):
            """Manualy change worker KTU"""
            print("Выберете вид КТУ:")
            ktu_option = tmp_rpt.workers_showing
            direction = super(Reports, self).choise_from_list(ktu_option)
            print("Выберете работника:")
            workers = tmp_rpt.workers_showing[direction]['КТУ']
            ch_worker = super(Reports, self).choise_from_list(workers)
            new_ktu = float(input("Введите новое значение КТУ: "))
            delta = (tmp_rpt.workers_showing[direction]['КТУ'][ch_worker]
                     - new_ktu)

            workers = super(Reports, self).count_unzero_items(
                tmp_rpt.workers_showing[direction]['КТУ'])
            tmp_rpt.workers_showing[direction]['КТУ'][ch_worker] = new_ktu
            for worker in tmp_rpt.workers_showing[direction]['КТУ']:
                unzero_worker = (
                    tmp_rpt.workers_showing[direction]['КТУ'][worker] != 0)
                if worker != ch_worker and unzero_worker:
                    tmp_rpt.workers_showing[direction]['КТУ'][worker] = round(
                        tmp_rpt.workers_showing[direction]['КТУ'][worker]
                        + round(delta/(workers-1), 2), 2)
            tmp_rpt.coutn_delta_ktu(direction)
            return tmp_rpt

        def complete_main_report(tmp_rpt):
            """Complete main report"""
            choise = input("Вы уверены что хотите завершить отчет? Д/н: ")
            if choise.lower() == 'д':
                tmp_rpt.count_all_workers_in_report()
                tmp_rpt.status['status'] = '\033[92m[завершен]\033[0m'
                AllWorkers().add_salary_to_workers(
                    tmp_rpt.workers_showing['факт']['зарплата'],
                    tmp_rpt.status['date'],
                    tmp_rpt.unofficial_workers()
                )
                super(Reports, self).save_log_to_temp_file(
                    ' --> ' + tmp_rpt.status['status'])
                make_backup()
            return tmp_rpt

        while True:
            tmp_rpt = self.data_base[report_name]
            print(tmp_rpt)
            if '[завершен]' in report_name:
                break
            edit_menu_dict = {
                'ввести горную массу': enter_rock_mass,
                'ввести итоговую сумму': enter_totall,
                'ежемесячный бонус': enter_bonus,
                'изменить КТУ работника': change_ktu,
                'удалить отчет': self._delete_report,
                '\033[92mсформировать отчет\033[0m': complete_main_report,
                '[закончить редактирование]': 'break'
                }
            print("Выберете пункт для редактирования:")
            action_name = super().choise_from_list(edit_menu_dict)
            print()
            if action_name in ['[закончить редактирование]', '']:
                break
            elif action_name == 'удалить отчет':
                tmp_rpt = edit_menu_dict[action_name](report_name)
                break
            tmp_rpt = edit_menu_dict[action_name](tmp_rpt)
            self.data_base.pop(report_name, None)
            report_name = "{date} {shift} {status}".format(
                **tmp_rpt.status)
            self.data_base[report_name] = tmp_rpt
            super().dump_data(self.data_path, self.data_base)
            super().clear_screen()

    def _make_status_in_process(self, report_name):
        """Change status from 'not complete' to 'in process'"""
        print(self.data_base[report_name])
        tmp_report = self.data_base[report_name]
        print("Введите ОФИЦИАЛЬНЫЕ часы работы:")
        shift = tmp_report.status['shift']
        workers_list = AllWorkers().give_workers_from_shift(shift)
        workers_hours_list = self.create_workers_hours_list(workers_list)
        tmp_report.workers_showing['бух.']['часы'] = workers_hours_list
        super().clear_screen()
        tmp_report.create_ktu_list()
        tmp_report.count_all_workers_in_report()
        tmp_report.status['status'] = '\033[93m[в процессе]\033[0m'
        self.data_base.pop(report_name, None)
        new_name = "{date} {shift} {status}".format(**tmp_report.status)
        self.data_base[new_name] = tmp_report
        super().dump_data(self.data_path, self.data_base)
        super().save_log_to_temp_file(
            ' --> ' + tmp_report.status['status'])
        self._edit_main_report(new_name)

    def _print_workers_group(self):
        """Print additional workers group."""
        workers_group = {
            '[1] Окладники:': self.salary_workers,
            '[2] Бурильщики:': self.drillers,
            '[3] Бригадиры:': self.brigadiers
        }
        for workers_type in sorted(workers_group):
            print(workers_type)
            for worker in workers_group[workers_type]:
                print('\t', worker)

    def choose_salary_or_drillers(self):
        """Chose list to edit, salary or drillers."""
        self._print_workers_group()
        choose = input("\nВыберете тип работников для редактирования: ")
        if choose == '1':
            self._edit_salary_or_drillers(self.salary_path)
            super().save_log_to_temp_file(' salary')
        elif choose == '2':
            self._edit_salary_or_drillers(self.drillers_path)
            super().save_log_to_temp_file(' drillers')
        elif choose == '3':
            self._edit_salary_or_drillers(self.brigadiers_path)
            super().save_log_to_temp_file(' brigadiers')

    def give_main_results(self, year, month, shift):
        """Return drill meters, result and rock_mass.
        Return None, if report not exist."""
        report_name = year + '-' + month + ' ' + shift
        result_tuplet = ()
        for report in self.data_base:
            if (report_name in report and
                    self.data_base[report].count_rock_mass() != 0):
                drill_meters = self.data_base[report].result['шпурометры']
                result = self.data_base[report].count_result()
                rock_mass = self.data_base[report].count_rock_mass()
                result_tuplet = drill_meters, result, rock_mass
        return result_tuplet

    def give_avaliable_to_edit(self, *statuses):
        """Give reports that avaliable to edit"""
        avaliable_reports = []
        avaliable_reports = [report for status in statuses
                             for report in self.data_base
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
            shift = super().choise_from_list(self.shifts)
            if self._check_if_report_exist(shift, date):
                break

        workers_list = AllWorkers().give_workers_from_shift(shift)
        print(shift)
        for worker in workers_list:
            print(worker)

        # Add additional workers from another shift.
        added_workers = self._add_worker_from_diff_shift(shift)
        workers_list.extend(added_workers)
        super().clear_screen()

        report = MainReport('\033[91m[не завершен]\033[0m', shift, date)
        workers_hours_list = self.create_workers_hours_list(workers_list)
        report.workers_showing['факт']['часы'] = workers_hours_list
        print("\nВведите результаты добычи бригады.")
        report = self._input_result(report)
        print("\nТабель бригады заполнен.\n")
        report_name = "{date} {shift} {status}".format(**report.status)
        self.data_base[report_name] = report
        super().dump_data(self.data_path, self.data_base)
        super().save_log_to_temp_file(report_name)

    def edit_report(self):
        """
        Edition uncompleted report by user with 'master' accesse.
        """

        def change_hours(tmp_rpt):
            """Change hours value."""
            print("Выберете работника для редактирования:")
            workers = tmp_rpt.workers_showing['факт']['часы']
            worker = super(Reports, self).choise_from_list(workers)
            new_hours = int(input("Введите новое значение часов: "))
            tmp_rpt.workers_showing['факт']['часы'][worker] = new_hours
            return tmp_rpt

        avaliable_reports = self.give_avaliable_to_edit(
            '[не завершен]')
        print("""\
Вам доступны для редактирования только отчеты со статусом: \
\033[91m[не завершен]\033[0m
Выберет отчет для редактирования:
""")
        report_name = super().choise_from_list(
            avaliable_reports, none_option=True)
        if report_name:
            super().save_log_to_temp_file(report_name)
        super().clear_screen()
        while report_name:
            tmp_rpt = self.data_base[report_name]
            print(tmp_rpt)
            edit_menu_dict = {
                'изменить часы': change_hours,
                'удалить отчет': self._delete_report,
                'изменить добычу': self._input_result,
                '[закончить редактирование]': 'break'
                }
            print("Выберете пункт для редактирования:")
            action_name = super().choise_from_list(edit_menu_dict)
            print()
            if action_name in ['[закончить редактирование]', '']:
                break
            elif action_name == 'удалить отчет':
                tmp_rpt = edit_menu_dict[action_name](report_name)
                break
            tmp_rpt = edit_menu_dict[action_name](tmp_rpt)
            self.data_base[report_name] = tmp_rpt
            super().dump_data(self.data_path, self.data_base)
            super().clear_screen()

    def work_with_main_report(self, current_user):
        """Finish MainReport"""
        years = set([report.split('-')[0] for report in self.data_base])
        print("Выберете год:")
        year = super().choise_from_list(years, none_option=True)
        if year:
            reports_by_years = [report for report in self.data_base
                                if report.startswith(year)]
            print("Выберет отчет:")
            report_name = super().choise_from_list(reports_by_years,
                                                   none_option=True)
        else:
            report_name = None
        if report_name:
            super().save_log_to_temp_file(' ' + report_name)
            if '[не завершен]' in report_name:
                self._make_status_in_process(report_name)
            elif '[завершен]' in report_name:
                print(self.data_base[report_name])
                if current_user['accesse'] == 'admin':
                    choise = input("""\
\033[91m[un]\033[0m Возвратить статус '\033[93m[в процессе]\033[0m'\n""")
                    if choise == 'un':
                        self._uncomplete_main_report(report_name)
            elif '[в процессе]' in report_name:
                self._edit_main_report(report_name)
