#!/usr/bin/env python3
"""News module."""

import os
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsolytePath


class News(BasicFunctions):
    """Show news to users."""
    news_path = AbsolytePath('').get_absolyte_path()[:-5] + 'news/'
    news_memory = AbsolytePath('news_memory').get_absolyte_path()

    def __init__(self):
        if not os.listdir('news/') or not os.path.exists(self.news_memory):
            self.news_memory_file = {}
            super().dump_data(self.news_memory, self.news_memory_file)
        else:
            self.news_memory_file = super().load_data(self.news_memory)

    @classmethod
    def show_new_news(cls, new_news):
        """Show new news in screen."""
        print("\033[93m[НОВОСТИ]\033[0m\n")
        while True:
            print('\n', '-' * 80)
            if not new_news:
                break
            print(new_news[0])
            new_news = new_news[1:]
            input("\n[ENTER] - дальше")

    def _add_news_to_user(self, user_login, news):
        """Add news to user."""
        self.news_memory_file[user_login].append(news)

    def _check_if_user_in_file(self, user_login):
        """Check if user in memory file."""
        user_news = []
        if user_login in self.news_memory_file:
            user_news = self.news_memory_file[user_login]
        else:
            self.news_memory_file[user_login] = []
        return user_news

    def print_news(self, user_login):
        """Print news for user."""
        new_news = []
        user_news = self._check_if_user_in_file(user_login)
        if os.listdir('news/'):
            for news in sorted(os.listdir('news/')):
                if news not in user_news:
                    with open(self.news_path + news, 'r') as file:
                        new_news.append(file.read())
                    self._add_news_to_user(user_login, news)
                    super().dump_data(self.news_memory, self.news_memory_file)
        self.show_new_news(new_news)

    def show_actual_news(self):
        """Show all news that actual."""
        new_news = []
        if os.listdir('news/'):
            for news in sorted(os.listdir('news/')):
                with open(self.news_path + news, 'r') as file:
                    new_news.append(file.read())
        if new_news:
            self.show_new_news(new_news)
        else:
            print("Новых новостей нет.")
