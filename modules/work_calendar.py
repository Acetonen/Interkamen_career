#!/usr/bin/env python3
"""Working calendar module."""

import os
import calendar as cl
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsolytePath


class WCalendar(BasicFunctions):
    """Career working calendar ofr current year."""

    month_prnt = ''

    def __init__(self, year):
        self.year = year
        shifts = ["Смена 1", "Смена 2"]
        print("Выберете смену БРИГАДЫ"
              f", которая будет длинной в январе {year} года:")
        br_long = super().choise_from_list(shifts)
        print("Выберете смену ИТР"
              f", которая будет длинной в январе {year} года:")
        itr_long = super().choise_from_list(shifts)

        self.br_cal = self._set_cal(year, br_long, "brig")
        self.itr_cal = self._set_cal(year, itr_long, "itr")

    def __repr__(self):
        year = str(self.year)
        output = ('\n\t\t      \033[4mКалендарь пересменок \033[96m{}\033[0m.'
                  .format(year)) + '\n\n'
        for tripl_month in range(0, 12, 3):
            for month in range(tripl_month, tripl_month+3):
                self._colorized_month(month)
                month_end = self._count_end_spaces(month)
                tmp_month = list(self.month_prnt.split('\\n'))[:-1]
                tmp_month[-1] = tmp_month[-1] + month_end
                if len(tmp_month) == 7:
                    tmp_month.append(' '*20)
                if month in [4, 6]:
                    tmp_month[0] = tmp_month[0] + '    '
                if month in [0, 3, 6, 9]:
                    month_sum = tmp_month[:]
                else:
                    month_sum = [s1 + '\t' + s2
                                 for s1, s2 in zip(month_sum, tmp_month)]
            output += '\n'.join(month_sum) + '\n\n'
            month_sum = []
        output = output.replace(' ' + year, '     ')
        output += ("\033[93m*7\033[0m - пересменки ИТР\n"
                   + "\033[96m*31\033[0m - пересменки бригады.")
        return output

    @classmethod
    def _coin(cls, start):
        """Simple closures function that return True/False alternately."""
        stat = start

        def change():
            """Change coin state."""
            nonlocal stat
            tmp_stat = stat
            stat = not stat
            return tmp_stat
        return change

    def _set_cal(self, year, whos_long, workers):
        cal = cl.TextCalendar()
        self.working_days_in_month = []
        self.month_length = []
        for month in range(1, 12):
            days = [day for day in cal.itermonthdays(year, month) if day != 0]
            self.month_length.append(len(days))
            if len(days) % 2 != 0:
                self.working_days_in_month.append('diff')
            else:
                self.working_days_in_month.append('same')
        # In december both brigades have same days.
        self.working_days_in_month.append('same')
        self.month_length.append(30)

        changes_dates = self._count_changes_dates(whos_long, workers)
        return changes_dates

    def _count_changes_dates(self, whos_long, workers):
        """Count changes days in months."""
        changes_dates = []
        if whos_long == 'Смена 1':
            first_long = self._coin(True)
        else:
            first_long = self._coin(False)

        for month in range(0, 12):
            if self.working_days_in_month[month] == 'diff':
                add_day = 1 if first_long() else 0
            else:
                add_day = 0
            changes_dates.append(self._begin_and_end(workers, month, add_day))
        return changes_dates

    def _begin_and_end(self, workers, month, add_day):
        """Create begin and end dates."""
        if workers == "brig":
            begin = self.month_length[month] // 2 + add_day
            end = self.month_length[month]
            # January holydays fix.
            if month == 0:
                begin = begin + 2
        elif workers == "itr":
            begin = 7
            end = self.month_length[month] // 2 + 7 - add_day
            # January holydays fix.
            if month == 0:
                begin = begin + 2
                end = end + 2
        return begin, end

    def _colorized_days(self, days, color):
        """Colorize days in calendar."""
        for day in days:
            st_day = str(day)
            if len(st_day) == 1:
                st_day = ' ' + st_day
            self.month_prnt = self.month_prnt.replace(
                st_day, color + st_day + '\033[0m')

    def _colorized_month(self, month):
        """Colorize month."""
        cal = cl.TextCalendar()
        self.month_prnt = cal.formatmonth(self.year, month+1).__repr__()
        self._colorized_days(self.br_cal[month], '\033[96m')
        self._colorized_days(self.itr_cal[month], '\033[93m')

    def _count_end_spaces(self, month):
        """Count spaces at the end of month."""
        cal = cl.TextCalendar()
        days = [day for day in cal.itermonthdays(self.year, month + 1)]
        month_end = -1
        day = 0
        while not day:
            day = days[-1]
            month_end += 1
            days = days[:-1]
        month_end = month_end * '   '
        return month_end

    def give_month_shifts(self, month):
        """Print calendar."""
        self._colorized_month(month)
        self.month_prnt = self.month_prnt.replace('\\n', '\n\t')
        curr_month_shifts = (
            self.month_prnt +
            "\n\t\033[93m*пересменка ИТР\033[0m" +
            "\n\t\033[96m*пересменка бригад\033[0m ")
        return curr_month_shifts


class WorkCalendars(BasicFunctions):
    """Manage calendars."""
    calendar_path = AbsolytePath('working_calendar').get_absolyte_path()

    def __init__(self):
        self.calendar_file = {}
        if os.path.exists(self.calendar_path):
            self.calendar_file = super().load_data(self.calendar_path)

    def create_calendar(self):
        """Create working calendar."""
        year = int(input("Введите год: "))
        work_calendar = WCalendar(year)
        self.calendar_file[year] = work_calendar
        super().dump_data(self.calendar_path, self.calendar_file)
        print(f"Рабочий календарь {year} создан.")
        print(work_calendar)

    def show_year_shifts(self):
        """Show shift calendar by year."""
        print("Выберете год:")
        year = super().choise_from_list(self.calendar_file, none_option=True)
        if year:
            super().clear_screen()
            print(self.calendar_file[year])

    def give_current_brigade(self, cur_date):
        """Return current brigade."""
        shift_day = self.calendar_file[cur_date[0]].br_cal[cur_date[1]-1][0]
        if cur_date[2] <= shift_day:
            cur_brig = 'Бригада 1'
        else:
            cur_brig = 'Бригада 2'
        return cur_brig

    def give_current_itr(self, cur_date):
        """Return current ITR."""
        shift_days = self.calendar_file[cur_date[0]].itr_cal[cur_date[1]-1]
        if cur_date[2] <= shift_days[0] or cur_date[2] >= shift_days[1]:
            cur_itr = 'Смена 1'
        else:
            cur_itr = 'Смена 2'
        return cur_itr

    def give_current_month_shifts(self, cur_date):
        """Return current month shifts."""
        shifts_cal = (self.calendar_file[cur_date[0]]
                      .give_month_shifts(cur_date[1]-1))
        return shifts_cal