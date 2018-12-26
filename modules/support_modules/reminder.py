#!/usr/bin/env python3
"""Add reminder under maim meny, different for different user access"""

import os
import time
from datetime import date, timedelta
from modules.support_modules.standart_functions import BasicFunctions
from modules.main_career_report import Reports
from modules.mechanic_report import MechReports


class Reminder(BasicFunctions):
    """Make different reminder."""

    def __init__(self):
        self.reminder_path = super().get_root_path() / 'data' / 'reminds'
        self.remind_by_access = {
            'mechanic': [self._maintenance_remind],
            'info': [],
            'master': [],
            'boss': [self._main_report_remind],
            'admin': [
                self._main_report_remind,
                self._maintenance_remind,
                self._update_career_map,
            ]
        }

        if self.reminder_path.exists():
            self.reminder_file = super().load_data(self.reminder_path)
        else:
            self.reminder_file = {}
            for users in self.remind_by_access:
                self.reminder_file[users] = {}
            super().dump_data(self.reminder_path, self.reminder_file)

    @classmethod
    def _update_career_map(cls):
        """Reminder to update career map for daily report."""
        header = ''
        map_path = super().get_root_path() / 'html_blancs' / 'map.pdf'
        if map_path.exists():
            map_date = time.gmtime(os.path.getmtime(map_path)).tm_yday
            today = date.today().timetuple().tm_yday
            if today - map_date > 30:
                header = '\033[91mНеобходимо обновить карту карьера.\033[0m'
        return header

    @classmethod
    def _main_report_remind(cls):
        """Remind if main report uncomplete."""
        header = ''
        reports_need_to_edit = Reports(None).give_avaliable_to_edit(
            '[не завершен]', '[в процессе]')
        if reports_need_to_edit:
            header = "Недооформленные документы:\n" + '\n'.join(
                sorted(reports_need_to_edit)
            )
        return header

    @classmethod
    def _maintenance_remind(cls):
        """Remind for machine maintenance."""
        header = MechReports(None).walk_thrue_maint_calendar()
        return header

    def give_remind(self, user_access):
        """Make menu header"""
        remind_list = []
        for remind_cond in self.remind_by_access[user_access]:
            if remind_cond:
                remind_list.append(remind_cond())
        for remind in self.reminder_file[user_access]:
            if date.today() > self.reminder_file[user_access][remind]:
                self.reminder_file[user_access].pop(remind)
                super().dump_data(self.reminder_path, self.reminder_file)
            else:
                remind_list.append('\n' + remind)
        header = ' '.join(remind_list)
        return header

    def _choose_users_to_remind(self):
        """Choose users to remind."""
        print("Choose users to reminder:")
        ch_list = list(self.reminder_file.keys())
        ch_list.append('all')
        users = super().choise_from_list(ch_list)
        return users

    def _save_custom_remind(self, users, deadline, remind):
        """Save custom remind."""
        if users == 'all':
            for user in self.reminder_file:
                self.reminder_file[user][remind] = deadline
        else:
            self.reminder_file[users][remind] = deadline
        super().dump_data(self.reminder_path, self.reminder_file)
        print("remind save: ", remind, str(deadline))

    def _delete_remind(self):
        """Delete remind."""
        users = self._choose_users_to_remind()
        if users == 'all':
            users = 'admin'
        remind = super().choise_from_list(self.reminder_file[users])
        if users == 'admin':
            for user_access in self.reminder_file:
                self.reminder_file[user_access].pop(remind, None)
        else:
            self.reminder_file[users].pop(remind)
        super().dump_data(self.reminder_path, self.reminder_file)
        print("remind deleted.")

    def make_custom_remind(self):
        """Make custom remind for type of user."""
        users = self._choose_users_to_remind()
        remind = input("Input remind: ")
        importance_list = {
            'normal': '',
            'low': '\033[93m',
            'hi': '\033[91m',
            'hiest': '\033[5m\033[91m'
        }
        print("Choose importanсe:")
        importance = super().choise_from_list(importance_list)
        remind = importance_list[importance] + remind + '\033[0m'
        deadline = int(input("Input days to deadline: "))
        deadline = date.today() + timedelta(days=deadline)
        self._save_custom_remind(users, deadline, remind)

    def show_all_reminds(self):
        """Show All reminds."""
        for users in self.reminder_file:
            print('\033[4m' + users + '\033[0m:')
            for remind in self.reminder_file[users]:
                print('\t', str(self.reminder_file[users][remind]), remind)
        delete = input("\n[d] - to delete remind: ")
        if delete.lower() == 'd':
            self._delete_remind()
