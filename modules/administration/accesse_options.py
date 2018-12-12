#!/usr/bin/env python3
"""
This module give to program choise tree and meny depend on user access.

Classes: Accesse: 'create_list',
                  'get_menue_list',
                  'get_actions_list'
                  'get_actions_with_input'
                  'get_sub_menu'
"""

from modules.administration.log_class import Logs
from modules.administration.users import Users

from modules.support_modules.emailed import EmailSender

from modules.workers_module import AllWorkers
from modules.main_career_report import Reports
from modules.report_analysis import ReportAnalysis
from modules.drill_instrument_report import DrillInstruments
from modules.mechanic_report import MechReports
from modules.rating import Rating
from modules.support_modules.backup import make_backup
from modules.drill_passports import DrillPassports
from modules.work_calendar import WorkCalendars
from modules.career_status import Statuses


class Accesse:
    """
    Give to program 'choise tree' and 'meny' depend on user access.
    """

    menu_options = {
        'info': {
            '--> [Статистика_ремонтов]': 'sub-menu',
            '--> [Статистика_добычи]': 'sub-menu',
            'Состояние карьера':
            lambda arg: Statuses().show_status()
        },
        'basic': {
            'Телефоны работников':
            lambda arg: AllWorkers().print_telefon_numbers(),
            'Календарь пересменок':
            lambda arg: WorkCalendars().show_year_shifts(),
            'Поменять пароль':
            lambda arg: Users().change_password(arg),
            '\033[93mВыйти из программы\033[0m': 'exit program'
        },
        'mechanic': {
            '--> [Статистика_ремонтов]': 'sub-menu',
            'Создать отчет по ремонтам':
            lambda arg: MechReports().create_report(),
            'Редактировать отчет\n------------------------------':
            lambda arg: MechReports().edit_report(),
            'Календарь обслуживания\n------------------------------':
            lambda arg: MechReports().maintenance_calendar()
        },
        'master': {
            '--> [Статистика_добычи]': 'sub-menu',
            'Создать табель добычной бригады':
            lambda arg: Reports().create_report(),
            'Редактировать табель\n------------------------------':
            lambda arg: Reports().edit_report(),
            'Создать буровой паспорт':
            lambda arg: DrillPassports().create_drill_passport(arg),
            'Редактировать буровой паспорт\n------------------------------':
            lambda arg: DrillPassports().edit_passport(),
            'Создать отчет по буровым инструментам':
            lambda arg: DrillInstruments().create_drill_report(),
            'Поставить рейтинг бригаде':
            lambda arg: Rating().give_rating(arg),
            'Ежедневный отчет мастера\n------------------------------':
            lambda arg: Statuses().create_career_status('master')
        },
        'boss': {
            '--> [Работники] ': 'sub-menu',
            '--> [Финансы]': 'sub-menu',
            '--> [Меню_механика]': 'sub-menu',
            '--> [Меню_мастера]': 'sub-menu',
            'Состояние карьера':
            lambda arg: Statuses().show_status()
        },
        'admin': {'\033[91m--> [administration]\033[0m': 'sub-menu'}
    }

    sub_menus = {
        '\033[91m--> [administration]\033[0m': {
            '\033[91m--> [log_menu] \033[0m': 'sub-menu',
            '\033[91m--> [users_menu] \033[0m': 'sub-menu',
            '\033[91m--> [databases] \033[0m': 'sub-menu',
            '\033[91mmake backup now\033[0m':
            lambda arg: make_backup(),
            '\033[91mbackup email settings\033[0m':
            lambda arg: EmailSender().edit_mail_propeties()
        },
        '\033[91m--> [log_menu] \033[0m': {
            'search in logs': lambda arg: Logs().search_in_logs(),
            'delete all logs': lambda arg: Logs().delete_all_logs(),
            'show all logs': lambda arg: Logs().show_all_logs(),
        },
        '\033[91m--> [users_menu] \033[0m': {
            'create new user': lambda arg: Users().create_new_user(),
            'edit user': lambda arg: Users().edit_user(),
            'show all users': lambda arg: Users().show_all_users()
        },
        '--> [Работники] ': {
            'Новый работник':
            lambda arg: AllWorkers().add_new_worker(),
            'Показать работников подразделения':
            lambda arg: AllWorkers().print_workers_from_division(),
            'Показать уволеных работников':
            lambda arg: AllWorkers().print_archive_workers(),
            'Вернуть работника из архива':
            lambda arg: AllWorkers().return_from_archive(),
            'Редактировать работника':
            lambda arg: AllWorkers().edit_worker(),
            'Бригадиры, окладники, бурильщики':
            lambda arg: Reports().choose_salary_or_drillers(),
            'Показать юбиляров этого года':
            lambda arg: AllWorkers().show_anniversary_workers(),
            'Создать календарь пересменок':
            lambda arg: WorkCalendars().create_calendar()
        },
        '\033[91m--> [databases] \033[0m': {
            'upd company structure':
            lambda arg: AllWorkers().upd_comp_structure(),
            'print company structure':
            lambda arg: AllWorkers().print_comp_structure()
        },
        '--> [Финансы]': {
            'Наряд бригады':
            lambda arg: Reports().work_with_main_report(arg),
            'Сформировать итог по рейтингу':
            lambda arg: Rating().count_brigade_winner()
        },
        '--> [Меню_механика]': menu_options['mechanic'],
        '--> [Меню_мастера]': menu_options['master'],
        '--> [Статистика_ремонтов]': {
            'Показать статистику КТГ и КТИ':
            lambda arg: MechReports().show_statistic(),
            'Статистика по причинам простоев':
            lambda arg: MechReports().show_statistic(True)
        },
        '--> [Статистика_добычи]': {
            'Статистика добычи по кубатуре':
            lambda arg: ReportAnalysis().result_analysis(),
            'Статистика по горной массе':
            lambda arg: ReportAnalysis().rock_mass_analysis(),
            'Статистика по буровому инструменту':
            lambda arg: DrillInstruments().show_statistic_by_year(),
        }
    }

    sub_standart_options = {
        '<-- [Предыдущее меню]': 'menu before',
        '\033[93mВыйти из программы\033[0m': 'exit program',
    }

    def __init__(self, accesse='mechanic'):
        self.menu_list = self.create_list(accesse, self.menu_options)

    @classmethod
    def create_list(cls, accesse, options_list):
        """Create accesse and options menus"""
        for name in ('mechanic', 'master', 'boss', 'info'):
            options_list[name].update(options_list['basic'])
        options_list['admin'].update(options_list['boss'])
        return options_list[accesse]

    def get_sub_menu(self, sub_menu_name):
        """Return sub-menu"""
        self.sub_menus[sub_menu_name].update(self.sub_standart_options)
        return self.sub_menus[sub_menu_name]

    def get_menu_dict(self):
        """Give menu dict"""
        return self.menu_list
