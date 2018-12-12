#!/usr/bin/env python3
"""Everyday career status."""

import os
from datetime import date, timedelta
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.work_calendar import WorkCalendars
from modules.workers_module import AllWorkers
from modules.main_career_report import Reports


class CareerStatus(BasicFunctions):
    """Current career status."""

    def __init__(self, user_acs):
        self.date = {
            "today": str(date.today()),
            "tomorrow": str(date.today() + timedelta(days=1))
        }
        date_numbers = list(map(int, self.date['today'].split('-')))
        self.cur = {
            "brig":
            WorkCalendars().give_current_brigade(date_numbers),
            "itr":
            WorkCalendars().give_current_itr(date_numbers),
            'month_shifts':
            WorkCalendars().give_current_month_shifts(date_numbers)
        }
        self.itr_list = AllWorkers().print_telefon_numbers(
            itr_shift=self.cur["itr"])
        self.mach = {
            "to_repare": None,
            "to_work": None
        }
        self.storage = {
            "KOTC": None,
            "sale": None
        }
        self.works_plan = {
            "expl_work": None,
            "rock_work": None
        }
        self.res = {
            "month": None,
            "shift": None
        }
        self.add_info(user_acs)

    def __repr__(self):
        """Print status."""
        output = (
            f"\n\033[7mCостояние карьера на вечер: {self.date['today']}\033[0m"
            "\n\n\033[4mРаботники:\033[0m"
            f"\nСейчас на смене: {self.cur['brig']}"
            f"\nСмена ИТР: {self.cur['itr']}"
            "\nРаботники ИТР:\n"
        )
        output += '\n'.join(self.itr_list)
        output += "\n\n\033[4mПересменки в этом месяце:\033[0m\n\t"
        output += (
            self.cur['month_shifts']
            .replace(
                ' ' + self.date['tomorrow'].split('-')[-1],
                ' \033[41m' + self.date['tomorrow'].split('-')[-1] + '\033[0m'
                )
        )
        output += (
            "\n\n\033[4mДобыто блок-заготовок:\033[0m"
            f"\n\tв текущем месяце: {self.res['month']} м.куб."
            f"\n\tтекущей вахтой: {self.res['shift']} м.куб."
            "\n\n\033[4mОбъем блоков на отгрузочном складе:\033[0m"
            f"\n\tЦеховой камень: {self.storage['KOTC']} м.куб."
            f"\n\tСторонний камень: {self.storage['sale']} м.куб."
            "\n\n\033[4mСостояние техники:\033[0m"
            "\n\t\033[91mВыведена на ремонт:\033[0m\n\t"
        )
        output += f'{self.mach["to_repare"]}'
        output += "\n\t\033[92mВведена в работу:\033[0m\n\t"
        output += f'{self.mach["to_work"]}'
        output += (
            f"\n\n\033[4mПлан работ на {self.date['tomorrow']}\033[0m"
            "\n\t\tВзрывные работы."
            "\n\tгоризонт  направление  качество\n\t"
        )
        output += f"{self.works_plan['expl_work']}"
        output += (
            "\n\n\t\tДобычные работы."
            "\n\tгоризонт  направление  качество\n\t"
        )
        output += f"{self.works_plan['rock_work']}"
        output = output.replace(
            'None', '\033[91m<Информация отсутствует>\033[0m')
        return output

    def _add_master_info(self):
        """Add info from master."""
        self._input_current_result()
        self._input_strage_volume()
        works = ['разборка', 'пассировка', 'бурение']
        quolity = ['блоки', 'масса']
        print("\033[4mБуровзрывные работы:\033[0m")
        self.works_plan['expl_work'] = self._plan_works(quolity)
        print("\033[4mДобычные работы:\033[0m")
        self.works_plan['rock_work'] = self._plan_works(works)
        print("Отчет создан.")

    def _input_strage_volume(self):
        """Add rocks from storage."""
        print("Введите объем склада:")
        self.storage["KOTC"] = super().float_input(msg='Цеховой камень: ')
        self.storage["sale"] = super().float_input(msg='На продажу: ')

    def _input_current_result(self):
        """Add current result."""
        self.res["shift"] = super().float_input(msg="Введите добычу вахты: ")
        if self.cur["brig"] == 'Бригада 1':
            self.res["month"] = self.res["shift"]
        else:
            self.res["month"] = (
                Reports()
                .give_main_results(*str(date.today()).split('-'), 'Смена 1')[1]
                + self.res["shift"])

    def _plan_works(self, quol):
        """Input rock or expl work"""
        horizonds = ['+108', '+114', '+120', '+126', '+132']
        directions = ['восток', 'запад', 'север', 'юг']
        print("Введите информацию по работам на {}"
              .format(self.date['tomorrow']))
        work_list = []
        print_list = ''
        while True:
            print("\tгоризонт  направление  качество")
            print('\t' + print_list)
            choose = input("Добавить работы на горизонте? д/н: ")
            if choose.lower() == 'д':
                print("Выберете горизонт:")
                horizond = super().choise_from_list(horizonds)
                print("Выберете направление:")
                direction = super().choise_from_list(directions)
                print("Выберете предполагаемое качество:")
                quoli = super().choise_from_list(quol)
                work_list.append(
                    "{:^10} {:^10} {:^10}".format(horizond, direction, quoli))
                print_list = '\n\t'.join(work_list)
                super().clear_screen()
            else:
                super().clear_screen()
                break
        if not work_list:
            work_list.append('Не запланированы.')
        else:
            work_list = '\n\t'.join(work_list)
        return work_list

    def _add_mechanic_info(self):
        """Add info from mechanic."""
        print("\033[4mВыберете технику, выведенную в ремонт:\033[0m")
        self.mach["to_repare"] = self._create_mach_list()
        print("\033[4mВыберете технику, введенную в работу:\033[0m")
        self.mach["to_work"] = self._create_mach_list()
        print("Отчет создан.")

    def _create_mach_list(self):
        """Create mach list to repare or from repare."""
        mach_name = [
            'УАЗ-390945', 'УАЗ-220695', 'ГАЗ-3307', 'Commando-110',
            'Commando-120', 'Komazu-WA470', 'Volvo-L150', 'КС-5363А',
            'КС-5363Б', 'КС-5363Б2 ', 'AtlasC-881', 'AtlasC-882',
            'Hitachi-350', 'Hitachi-400', 'КрАЗ-914', 'КрАЗ-413',
            'КрАЗ-069', 'Бул-10', 'ДЭС-AD'
        ]
        mach_list = []
        while True:
            print(mach_list)
            choose = input("Добавить технику? д/н: ")
            if choose.lower() == 'д':
                print("Выберете технику:")
                mach = super().choise_from_list(mach_name)
                mach_list.append(mach)
                super().clear_screen()
            else:
                super().clear_screen()
                break
        if not mach_list:
            mach_list.append('Отсутствуют.')
        return mach_list

    def add_info(self, user_acs):
        """Add info depend on user access."""
        info_type = {'master': self._add_master_info,
                     'mechanic': self._add_mechanic_info}
        info_type[user_acs]()


class Statuses(BasicFunctions):
    """Create and save curent status reports."""
    car_stat_path = AbsolytePath('carer_status').get_absolyte_path()

    def __init__(self):
        if os.path.exists(self.car_stat_path):
            self.car_stat_file = super().load_data(self.car_stat_path)
        else:
            self.car_stat_file = {}
            super().dump_data(self.car_stat_path, self.car_stat_file)

    def create_career_status(self, user_acs):
        """Create status if not exist."""
        try:
            self.car_stat_file[str(date.today())].add_info(user_acs)
        except KeyError:
            self.car_stat_file[str(date.today())] = CareerStatus(user_acs)
        super().dump_data(self.car_stat_path, self.car_stat_file)

    def show_status(self):
        """Show career status."""
        print("Выберете дату:")
        status = super().choise_from_list(self.car_stat_file, none_option=True)
        if status:
            super().clear_screen()
            print(self.car_stat_file[status])


if __name__ == '__main__':
    Statuses().create_career_status('master')
    Statuses().create_career_status('mechanic')
    Statuses().show_status()