#!/usr/bin/env python3
"""
This module contain class that provide working with brigade rating.
"""

import os
import pandas as pd
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsolytePath


class Rating(BasicFunctions):
    """Working with ratings in DataFrame."""

    brig_rating_path = AbsolytePath('brig_rating').get_absolyte_path()
    brig_columns = ['year', 'month', 'shift', 'cleanness', 'discipline',
                    'KTI', 'roads', 'maintainence', '']
    shifts = ['Смена 1', 'Смена 2']

    def __init__(self):
        if os.path.exists(self.brig_rating_path):
            self.brig_rating_file = super().load_data(self.brig_rating_path)
        else:
            self.brig_rating_file = pd.DataFrame(columns=self.brig_columns)
            super().dump_data(self.brig_rating_path, self.brig_rating_file)

    def give_rating(self, user):
        """Give rating to shift."""
        while True:
            rep_date = self._input_date()
            if not rep_date:
                break
            check = super().check_date_in_dataframe(self.mech_file, rep_date)
            day = input("Введите день: ")
            rep_date.update({'day': int(day)})
            check = super().check_date_in_dataframe(self.mech_file, rep_date)
            if check:
                print("Отчет за это число уже существует.")
            else:
                self._create_blanc(rep_date)
                self._working_with_report(rep_date)
                break
