#!/usr/bin/env python3
"""Dump data to xlsx file."""

from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.support_modules.standart_functions import BasicFunctions


class DumpToExl(BasicFunctions):
    """Dump data to xlsx file."""
    months = [
        '', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    drill_img_path = (AbsolytePath('').get_absolyte_path()[:-5]
                      + 'exl_blancs/scheme.png')
    blanc_drill_path = (AbsolytePath('').get_absolyte_path()[:-5]
                        + 'exl_blancs/drill_passport.xlsx')
    drill_pass_path = (AbsolytePath('').get_absolyte_path()[:-5]
                       + 'Буровые_паспорта/')

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
        workbook.save(self.drill_pass_path + pass_name + '.xlsx')
        print("\nФайл сохранен:\n", self.drill_pass_path + pass_name + '.xlsx')
