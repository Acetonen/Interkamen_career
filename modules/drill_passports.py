#!/usr/bin/env python3
"""Module to work with drill passports."""


import os
import pandas as pd
from numpy import nan as Nan
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsolytePath


class DPassport(BasicFunctions):
    """Drill passport."""

    horizonds = ['+108', '+114', '+120', '+126', '+132']

    def __init__(self, pass_number, master, empty_df):
        self.pass_number = pass_number
        self.master = master
        self.params = empty_df
        self.bareholes = {}

    def __repr__(self):
        bareholes_table = '\nдлина, м  количество, шт'
        for key in self.bareholes:
            bareholes_table = (bareholes_table +
                               f"\n  {key}    -    {int(self.bareholes[key])}")
        output = (
            "Дата паспорта: {}"
            .format('.'.join(map(str, [
                self.params.year, self.params.month, self.params.day]))) +
            "\nНомер паспорта: {}".format(int(self.params.number)) +
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
              "введите их в следующем формате: длина*колличество.\n"
              "Например: 5.5*6"
              "\n[з] - закончить ввод\n")
        bareholes_number = 0
        totall_meters = 0
        temp_bareholes = {}
        while True:
            barehole = input("Введите значения шпуров: ")
            if barehole.lower() in ['з', '']:
                break
            elif '*' in barehole:
                barehole = barehole.split('*')
                bar_lenght = super().float_input(inp=barehole[0])
                totall_meters += bar_lenght * int(barehole[1])
                temp_bareholes[bar_lenght] = int(barehole[1])
                bareholes_number += int(barehole[1])
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
        drillers_path = AbsolytePath('drillers').get_absolyte_path()
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
        self.params.pownder = round(
            self.params.block_vol * self.params.pownd_consump / 1000, 1)
        self.params.d_sh = (
            float(self.params.totall_meters) + (bareholes_number * 0.3)
            + self.params.block_width + 30
        )

    def _baareholes_and_dependencies(self):
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
        self._baareholes_and_dependencies()
        self._set_bits_in_rock()

    def change_parametrs(self):
        """Change passport parametrs."""
        edit_menu_dict = {
            'Изменить горизонт': self._set_horizond,
            'Изменить расход ВВ и ЭД': self._set_pownder_parametrs,
            'Изменить бурильщика': self._set_driller,
            'Ввести новые длины шпуров': self._baareholes_and_dependencies,
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


class DrillPassports(BasicFunctions):
    """Class to create and working with drill passports."""

    drill_pass_path = AbsolytePath('drill_passports').get_absolyte_path()
    pass_columns = [
        'number', 'year', 'month', 'day', 'horizond', 'totall_meters',
        'driller', 'block_height', 'block_width', 'block_depth', 'block_vol',
        'pownd_consump', 'pownder', 'detonators', 'd_sh', 'master',
        'bits_in_rock'
    ]
    months = [
        '', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    img_path = (AbsolytePath('').get_absolyte_path()[:-5]
                + 'exl_blancs/scheme.png')
    blanc_path = (AbsolytePath('').get_absolyte_path()[:-5]
                  + 'exl_blancs/drill_passport.xlsx')
    pass_path = (AbsolytePath('').get_absolyte_path()[:-5]
                 + 'Буровые_паспорта/')

    def __init__(self):
        self._create_empty_df()
        if os.path.exists(self.drill_pass_path):
            self.drill_pass_file = super().load_data(self.drill_pass_path)
        else:
            self.drill_pass_file = {}
            super().dump_data(self.drill_pass_path, self.drill_pass_file)

    def _create_empty_df(self):
        """Create blanc DF list."""
        self.empty_df = pd.DataFrame(columns=self.pass_columns)
        self.empty_ser = pd.Series(
            [Nan for name in self.pass_columns], index=self.pass_columns
            )

    def _check_if_report_exist(self, number):
        """Check if report exist in base"""
        check = True
        for report in self.drill_pass_file:
            if number in report.split(' '):
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
            super().save_log_to_temp_file(pass_name)
            exel = input("\nЖелаете создать exel файл? д/н: ")
            if exel == 'д':
                self._dump_to_exl(passport)
        else:
            print("Вы отменили сохранение.")

    def _choose_passport_from_bd(self):
        """Choose passport from BD."""
        years = set([passp.split('-')[0] for passp in self.drill_pass_file])
        print("Выберете год:")
        year = super().choise_from_list(years, none_option=True)
        if year:
            months = set([
                report.split('-')[1] for report in self.drill_pass_file
                if report.startswith(year)])
            print("Выберет месяц:")
            month = super().choise_from_list(months)
            if month:
                passport_name = super().choise_from_list(
                    [report for report in self.drill_pass_file
                     if report.startswith('-'.join([year, month]))])
        else:
            passport_name = None
        return passport_name

    def _last_number_of_passport(self):
        """Return last exist number."""
        last_passport = sorted(
            [passport for passport in self.drill_pass_file])[-1]
        last_number = last_passport.split(' ')[-1]
        return last_number

    def create_drill_passport(self, user):
        """Create drill passport."""
        if self.drill_pass_file:
            print("Номер последнего паспорта: ",
                  self._last_number_of_passport())
        while True:
            number = input("\nВведите номер паспорта: ")
            if self._check_if_report_exist(number):
                break
        passport = DPassport(number, user['name'], self.empty_ser)
        passport.fill_passport()
        super().clear_screen()
        print(passport)
        self._save_or_not(passport)

    def edit_passport(self):
        """Print passport for current number."""
        passport_name = self._choose_passport_from_bd()
        if passport_name:
            passport = self.drill_pass_file[passport_name]
            passport.change_parametrs()
            if not passport.params.number:
                self.drill_pass_file.pop(passport_name)
                super().dump_data(self.drill_pass_path, self.drill_pass_file)
                log = " \033[91mpassport deleted.\033[0m"
                super().save_log_to_temp_file(passport_name + log)
            else:
                self._save_or_not(passport)

    @classmethod
    def _create_pass_name(cls, passport):
        """Create passport name."""
        pass_name = ("{}-{}-{} {}"
                     .format(passport.params.year,
                             passport.params.month,
                             passport.params.day,
                             int(passport.params.number)))
        return pass_name

    def _dump_to_exl(self, passport):
        """Dump data to xlsx file."""
        workbook = load_workbook(self.blanc_path)
        worksheet = workbook.active
        img = Image(self.img_path)  # Add image.
        worksheet.add_image(img, 'A28')
        worksheet['F1'] = int(passport.params.number)  # Passport number.
        worksheet['F5'] = str(passport.params.day)  # Day.
        worksheet['G5'] = self.months[int(passport.params.month)]  # Month.
        worksheet['H5'] = str(passport.params.year)  # Year.
        worksheet['K7'] = str(passport.params.horizond)  # Horizond.
        worksheet['D11'] = float(passport.params.pownder)  # Pownder.
        worksheet['H11'] = int(passport.params.d_sh)  # D_SH.
        worksheet['K11'] = int(passport.params.detonators)  # Detonators.
        # Bareholes.
        row_number = 17
        for length in passport.bareholes:
            worksheet['C' + str(row_number)] = length
            worksheet['A' + str(row_number)] = int(passport.bareholes[length])
            row_number += 1
        # Volume.
        volume = float(passport.params.pownder) * 5
        worksheet['F25'] = volume
        # Block params.
        height = float(passport.params.block_height)
        worksheet['H23'] = height
        depth = float(passport.params.block_depth)
        worksheet['J23'] = depth
        worksheet['L23'] = round(volume / height / depth, 1)
        # Master.
        master = super().make_name_short(str(passport.params.master))
        worksheet['G49'] = master
        # Save file.
        pass_name = self._create_pass_name(passport)
        workbook.save(self.pass_path + pass_name + '.xlsx')
        print("\nФайл сохранен:\n", self.pass_path + pass_name + '.xlsx')
