#!/usr/bin/env python3
"""Count and change workers salsry."""

from modules.support_modules.standart_functions import (BasicFunctionsS
                                                        as Bas_F)


class WorkersSalary(Bas_F):
    """
    Count and manage workers salary.
    """

    __slots__ = ['salary_list_path', 'salary_list']

    def __init__(self):
        self.salary_list_path = (
            super().get_root_path() / 'data' / 'salary_list')
        if self.salary_list_path.exists():
            self.salary_list = super().load_data(self.salary_list_path)
        else:
            self.salary_list = {
                'Карьер': {},
                'Офис': {},
                'КОЦ': {},
            }
            super().dump_data(self.salary_list_path, self.salary_list)

    def _choose_division(self):
        """Choose divisioon to manage."""
        print("[ENTER] - выйти."
              "\nВыберете подразделение.")
        division = super().choise_from_list(self.salary_list, none_option=True)
        return division

    def _add_profession(self, division):
        """Add profession to list."""
        profession = input("Введите название новой профессии: ")
        self.salary_list[division][profession] = 0
        self._change_salary(division, profession)

    def _change_salary(self, division, profession=None):
        """Change salary for profession."""
        if not profession:
            print("Выберете профессию из списка:")
            profession = super().choise_from_list(self.salary_list[division])
        salary = super().float_input(msg="Введите оклад: ")
        self.salary_list[division][profession] = salary

    def _delete_profession(self, division):
        """Delete profession from list."""
        print("Выберете профессию для удаления:")
        profession = super().choise_from_list(self.salary_list[division])
        self.salary_list[division].pop(profession)

    def manage_salary_list(self):
        """Manage salary list."""
        division = self._choose_division()
        super().clear_screen()
        while division:
            for profession in sorted(self.salary_list[division]):
                print(
                    "{:<23} - {:<9,}p."
                    .format(profession, self.salary_list[division][profession])
                )

            actions_list = {
                'Добавить профессию': self._add_profession,
                'Изменить оклад': self._change_salary,
                'Удалить профессию': self._delete_profession,
            }
            print("\n[ENTER] - выход"
                  "\nВыберете действие:")
            action = super().choise_from_list(actions_list, none_option=True)
            if not action:
                break
            else:
                actions_list[action](division)
            super().dump_data(self.salary_list_path, self.salary_list)
            super().clear_screen()
