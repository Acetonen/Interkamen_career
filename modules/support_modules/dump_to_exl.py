#!/usr/bin/env python3
"""Dump data to xlsx file."""

import os
import time
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from modules.support_modules.absolyte_path_module import AbsPath
from modules.support_modules.standart_functions import BasicFunctions


class DumpToExl(BasicFunctions):
    """Dump data to xlsx file."""
    months = [
        '', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    drill_img_path = AbsPath().get_path('exl_blancs', 'scheme.png')
    blanc_drill_path = AbsPath().get_path('exl_blancs', 'drill_passport.xlsx')
    blanc_ktu_path = AbsPath().get_path('exl_blancs', 'ktu.xlsx')
    drill_pass_path = AbsPath().get_path(
        'Documents', 'Буровые_паспорта', up_root=True)
    ktu_path = AbsPath().get_path(
        'Documents', 'КТУ', up_root=True)

    @classmethod
    def _create_pass_name(cls, passport):
        """Create passport name."""
        pass_name = ("{}-{}-{} {}"
                     .format(passport.params.year,
                             passport.params.month,
                             passport.params.day,
                             int(passport.params.number)))
        return pass_name

    def dump_drill_pass(self, passport):
        """Dump drill passport data to blanc exl file."""
        workbook = load_workbook(self.blanc_drill_path)
        worksheet = workbook.active
        img = Image(self.drill_img_path)  # Add image.
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
        workbook.save(os.path.join(self.drill_pass_path, pass_name) + '.xlsx')
        print(
            "\nФайл сохранен:\n",
            self.drill_pass_path + '/' + pass_name + '.xlsx'
        )

    def dump_ktu(self, tmp_rpt):
        """Dump KTU data to blanc exl file."""
        ktu = tmp_rpt.workers_showing['бух.']['КТУ']
        hours = tmp_rpt.workers_showing['бух.']['часы']
        year = tmp_rpt.status['date'].split('-')[0]
        month = (
            self.months[int(tmp_rpt.status['date'].split('-')[1][:2])][:-1]+'е'
        )
        shift = tmp_rpt.status['shift']
        brig_list = {
            'Смена 1': 'Бригадой №1',
            'Смена 2': 'Бригадой №2'
        }
        brig = brig_list[shift]

        workbook = load_workbook(self.blanc_ktu_path)
        worksheet = workbook.active
        worksheet['C4'] = brig
        worksheet['C5'] = month
        worksheet['D5'] = year
        worker_number = 1
        for worker in ktu:
            row_number = 7 + worker_number
            worksheet['A' + str(row_number)] = worker_number
            worksheet['B' + str(row_number)] = super().make_name_short(worker)
            worksheet['C' + str(row_number)] = hours[worker]
            worksheet['D' + str(row_number)] = ktu[worker]
            worker_number += 1
        # Save file.
        pass_name = '-'.join([
            year, tmp_rpt.status['date'].split('-')[1][:2], shift])
        workbook.save(os.path.join(self.ktu_path, pass_name) + '.xlsx')
        print(
            "\nФайл сохранен:\n",
            self.ktu_path + '/' + pass_name + '.xlsx'
        )
        time.sleep(3)
