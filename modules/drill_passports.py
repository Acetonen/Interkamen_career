#!/usr/bin/env python3
"""Module to work with drill passports."""


import pandas as pd
from numpy import nan as Nan
from typing import Union
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.dump_to_exl import DumpToExl
from modules.administration.logger_cfg import Logs
from modules.support_modules.custom_exceptions import MainMenu


LOGGER = Logs().give_logger(__name__)


class DPassport(BasicFunctions):
    """Drill passport."""

    horizonds = ['+108', '+114', '+120', '+126', '+132']

    def __init__(self, pass_number, master, empty_df, massive_type):
        self.pass_number = pass_number
        self.master = master
        self.params = empty_df
        self.bareholes = {}
        self.params.massive_type = massive_type

    def __repr__(self):
        bareholes_table = '\nдлина, м  количество, шт'
        for key in self.bareholes:
            bareholes_table = (bareholes_table +
                               f"\n  {key}    -    {int(self.bareholes[key])}")
        output = (
            "Дата паспорта: {}"
            .format('.'.join(map(str, [
                self.params.year, self.params.month, self.params.day]))) +
            "\nНомер паспорта: {}; Тип взрыва: {}".format(
                int(self.params.number),
                str(self.params.massive_type)) +
            "\nГорный мастер: {}".format(str(self.params.master)) +
            "\nБурильщик: {}".format(str(self.params.driller)) +
            "\nГоризонт: {}".format(str(self.params.horizond)) +
            "\n\nПараметры блока:" +
            "\nОбъем блока: {}м.кб.".format(float(self.params.block_vol)) +
            "\nГабариты: {}м x {}м x {}м".format(*map(float, [
                self.params.block_width,
                self.params.block_height,
                self.params.block_depth])) +
            "\n\nПараметры взрывания:\n" +
            "Расход пороха: {}г/м.куб".format(int(self.params.pownd_consump)) +
            "\nКоличество пороха: {}кг".format(float(self.params.pownder)) +
            "\nКоличество ДШ: {}м".format(int(self.params.d_sh)) +
            "\nКоличество ЭД: {}шт.".format(int(self.params.detonators)) +
            "\n\nПараметры шпуров:" +
            "\nПробурено метров: {}м".format(round(
                float(self.params.totall_meters), 1)) +
            "\nКоличество шпуров: {}шт.".format(int(round(
                (self.params.block_width - 0.4) / 0.35, 0)))
            )
        output += bareholes_table
        output += "\n\nКоронки в скале: {}".format(
            int(self.params.bits_in_rock))
        return output

    def _input_bareholes(self):
        """Input totall bareholes."""
        print("\nВведите шпуры.\n"
              "Если вы хотите ввести несколько шпуров одной длины, \n"
              "введите их в следующем формате: колличество*длинна.\n"
              "Например: 6*5.5"
              "\n[з] - закончить ввод\n")
        bareholes_number = 0
        totall_meters = 0
        temp_bareholes = {}
        while True:
            barehole = input("Введите значения шпуров: ")
            if barehole == '' and not temp_bareholes:
                continue
            if barehole.lower() in ['з', '']:
                break
            elif '*' in barehole:
                barehole = barehole.split('*')
                bar_lenght = super().float_input(inp=barehole[1])
                totall_meters += bar_lenght * int(barehole[0])
                temp_bareholes[bar_lenght] = int(barehole[0])
                bareholes_number += int(barehole[0])
            else:
                bar_lenght = super().float_input(inp=barehole)
                totall_meters += bar_lenght
                temp_bareholes[bar_lenght] = bar_lenght
                bareholes_number += 1
        self.bareholes = temp_bareholes
        self.params.totall_meters = totall_meters
        return bareholes_number

    def _set_date(self):
        """Set report date."""
        rep_date = super().input_date()
        day = int(input("Введите день: "))
        rep_date.update({'day': day})
        for item in rep_date:
            self.params[item] = rep_date[item]

    def _set_horizond(self):
        """Choose horizond."""
        print("Выберете горизонт:")
        self.params.horizond = super().choise_from_list(self.horizonds)

    def _set_pownder_parametrs(self):
        """Set pownder."""
        # Pownder consumption:
        pownd_consump = int(input("Введите расход ДП в граммах: "))
        self.params.pownd_consump = pownd_consump
        # Detonators:
        self.params.detonators = int(input("Введите количество ЭД: "))

    def _set_driller(self):
        """Choose driller."""
        drillers_path = super().get_root_path() / 'data' / 'drillers'
        drillers = super().load_data(drillers_path)
        print("Выберете бурильщика:")
        self.params.driller = super().choise_from_list(drillers)

    def _set_block_parametrs(self, bareholes_number):
        """Block parametrs (height, width, volume)"""
        block_height = super().float_input(msg="Введите высоту блока: ")
        self.params.block_height = block_height
        block_width = round(bareholes_number * 0.35 + 0.4, 1)
        self.params.block_width = block_width
        block_depth = self.params.totall_meters / bareholes_number
        self.params.block_depth = round(block_depth, 2)
        block_vol = round(block_height * block_width * block_depth, 1)
        self.params.block_vol = block_vol

    def _set_bits_in_rock(self):
        """Number of drill bits in rock."""
        self.params.bits_in_rock = int(input("Коронки в скале: "))

    def _count_expl_volume(self, bareholes_number):
        """Count amounts of DH and pownder."""
        pownder = round(
            self.params.block_vol * self.params.pownd_consump / 1000, 1)
        self.params.pownder = self._round_to_half(pownder)
        d_sh = (
            float(self.params.totall_meters) + (bareholes_number * 0.3)
            + self.params.block_width + 30
        )
        self.params.d_sh = round(d_sh / 10, 0) * 10

    @classmethod
    def _round_to_half(cls, number):
        number = (number // 0.5 * 0.5
                  if number % 0.5 < 0.29
                  else number // 0.5 * 0.5 + 0.5)
        return number

    def _bareholes_and_dependencies(self):
        """Count bareholes parametrs and dependenses.
        (block param, expl vol)"""
        bareholes_number = self._input_bareholes()
        self._set_block_parametrs(bareholes_number)
        self._count_expl_volume(bareholes_number)

    def fill_passport(self):
        """Fill passport."""
        self.params.number = self.pass_number
        self.params.master = self.master
        self._set_date()
        self._set_horizond()
        self._set_pownder_parametrs()
        self._set_driller()
        self._bareholes_and_dependencies()
        self._set_bits_in_rock()

    def change_parametrs(self):
        """Change passport parametrs."""
        edit_menu_dict = {
            'Изменить горизонт': self._set_horizond,
            'Изменить расход ВВ и ЭД': self._set_pownder_parametrs,
            'Изменить бурильщика': self._set_driller,
            'Ввести новые длины шпуров': self._bareholes_and_dependencies,
            'Удалить паспорт': 'del',
            '[закончить редактирование]': 'exit'
        }
        while True:
            super().clear_screen()
            print(self.__repr__())
            print("\nВыберете пункт для редактирования:")
            action_name = super().choise_from_list(edit_menu_dict)
            if action_name in ['[закончить редактирование]', '']:
                break
            elif action_name == 'Удалить паспорт':
                if super().confirm_deletion('паспорт'):
                    self.params.number = None
                    break
            else:
                edit_menu_dict[action_name]()


class NPassport(DPassport):
    """Nongabarites passport."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nk_count = self._input_count()

    @classmethod
    def _input_count(cls):
        """Input NG count."""
        count = int(input("Введите число негабаритов: "))
        return count

    def __repr__(self):
        output = super().__repr__()
        output = output.replace(
            "\nГорный мастер:",
            f": {self.nk_count}шт.\nГорный мастер:")
        return output


class DrillPassports(BasicFunctions):
    """Class to create and working with drill passports."""
    massive_type = ['Массив', 'Повторный', 'Негабариты']
    pass_columns = [
        'number', 'year', 'month', 'day', 'horizond', 'totall_meters',
        'driller', 'block_height', 'block_width', 'block_depth', 'block_vol',
        'pownd_consump', 'pownder', 'detonators', 'd_sh', 'master',
        'bits_in_rock', 'massive_type'
    ]

    def __init__(self, user):
        self.drill_pass_path = (
            super().get_root_path() / 'data' / 'drill_passports')
        self.user = user
        self._create_empty_df()
        if self.drill_pass_path.exists():
            self.drill_pass_file = super().load_data(self.drill_pass_path)
        else:
            self.drill_pass_file = {}
            super().dump_data(self.drill_pass_path, self.drill_pass_file)

    @classmethod
    def _create_pass_name(cls, passport: Union[NPassport, DPassport]) -> str:
        """Create passport name."""
        if len(str(passport.params.month)) == 1:
            month = '0' + str(passport.params.month)
        else:
            month = str(passport.params.month)
        pass_name = ("{}-{}-{} №{}-{}"
                     .format(passport.params.year,
                             month,
                             passport.params.day,
                             int(passport.params.number),
                             passport.params.massive_type))
        return pass_name

    def _create_empty_df(self):
        """Create blanc DF list."""
        self.empty_df = pd.DataFrame(columns=self.pass_columns)
        self.empty_serial = pd.Series([Nan for name in self.pass_columns],
                                      index=self.pass_columns)

    def _check_if_report_exist(self, number):
        """Check if report exist in base"""
        check = True
        for report in self.drill_pass_file:
            if number in report.split(' ')[-1]:
                check = False
                print("Паспорт с этим номером уже существует.")
        return check

    def _save_or_not(self, passport):
        """Save passport or not."""
        save = input("\n[c] - сохранить паспорт: ")
        if save in ['c', 'C', 'с', 'С']:
            pass_name = self._create_pass_name(passport)
            print('\033[92m', pass_name, ' - cохранен.\033[0m')
            self.drill_pass_file[pass_name] = passport
            super().dump_data(self.drill_pass_path, self.drill_pass_file)
            LOGGER.warning(
                f"User '{self.user['login']}' create drill pass.: {pass_name}"
            )
            exel = input("\nЖелаете создать exel файл? д/н: ")
            if exel == 'д':
                if passport.__class__.__name__ == 'DPassport':
                    DumpToExl().dump_drill_pass(passport)
                else:
                    DumpToExl().dump_drill_pass(passport,
                                                negab=passport.nk_count)
        else:
            print("Вы отменили сохранение.")

    def _choose_passport_from_bd(self):
        """Choose passport from BD."""
        years = set([passp.split('-')[0] for passp in self.drill_pass_file])
        print("[ENTER] - выйти."
              "\nВыберете год:")
        year = super().choise_from_list(years, none_option=True)
        if not year:
            raise MainMenu
        months = set([
            report.split('-')[1] for report in self.drill_pass_file
            if report.startswith(year)])
        print("Выберет месяц:")
        month = super().choise_from_list(months)
        if month:
            reports = [
                report
                for report in self.drill_pass_file
                if report.startswith('-'.join([year, month]))
            ]
            passport_name = super().choise_from_list(reports, none_option=True)

        return passport_name

    def _last_number_of_passport(self):
        """Return last exist number."""
        last_passport = sorted(
            [passport for passport in self.drill_pass_file])[-1]
        last_number = last_passport.split(' ')[-1]
        return last_number

    def count_drill_meters(self, driller: str, date: str) -> float:
        """Count totall meters for current driller."""
        drill_meters = 0
        for passport in self.drill_pass_file:
            pas_file = self.drill_pass_file[passport]
            if (str(pas_file.params.driller) == driller and
                    passport.startswith(date)):
                drill_meters += round(float(pas_file.params.totall_meters), 1)
        return drill_meters

    def create_drill_passport(self):
        """Create drill passport."""
        if self.drill_pass_file:
            print("Номер последнего паспорта: ",
                  self._last_number_of_passport())
        while True:
            number = input("\nВведите номер паспорта: ")
            if not number:
                raise MainMenu
            if self._check_if_report_exist(number):
                break

        print("Выберете тип паспорта:")
        pass_type = super().choise_from_list(self.massive_type)
        if pass_type == 'Негабариты':
            pass_blanc = NPassport
        else:
            pass_blanc = DPassport
        passport = pass_blanc(
            pass_number=number,
            master=self.user['name'],
            empty_df=self.empty_serial,
            massive_type=pass_type,
            )
        passport.fill_passport()
        super().clear_screen()
        print(passport)
        self._save_or_not(passport)

    def edit_passport(self):
        """Print passport for current number."""
        passport_name = self._choose_passport_from_bd()
        passport = self.drill_pass_file[passport_name]
        passport.change_parametrs()
        if not passport.params.number:
            self.drill_pass_file.pop(passport_name)
            super().dump_data(self.drill_pass_path, self.drill_pass_file)
            LOGGER.warning(
                f"User '{self.user['login']}' delete drill pass.: "
                + f"{passport_name}"
            )
        else:
            self._save_or_not(passport)
