#!/usr/bin/env python3
"""Add reminder under maim meny, different for different user access"""

from modules.support_modules.standart_functions import BasicFunctions
from modules.main_career_report import Reports
from modules.mechanic_report import MechReports


class Reminder(BasicFunctions):
    """Make different reminder."""

    def __init__(self, user_access):

        self.remind_by_access = {
            'mechanic': [
                self.maintenance_remind
            ],
            'master': [],
            'boss': [
                self.main_report_remind
            ],
            'admin': [
                self.main_report_remind,
                self.maintenance_remind
            ]
        }

        self.remind = []
        for remind in self.remind_by_access[user_access]:
            if remind:
                self.remind.append(remind())

    @classmethod
    def main_report_remind(cls):
        """Remind if main report uncomplete."""
        header = ''
        reports_need_to_edit = Reports().give_avaliable_to_edit(
            '[не завершен]', '[в процессе]')
        if reports_need_to_edit:
            header = "Недооформленные документы:\n" + '\n'.join(
                sorted(reports_need_to_edit)
            )
        return header

    @classmethod
    def maintenance_remind(cls):
        """Remind for machine maintenance."""
        header = MechReports().walk_thrue_maint_calendar()
        return header

    def give_remind(self):
        """Make menu header"""
        header = ' '.join(self.remind)
        return header
