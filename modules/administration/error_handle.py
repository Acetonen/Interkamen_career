#!/usr/bin/env python3
"""Provide working with errors logs."""

from modules.support_modules.absolyte_path_module import AbsPath
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.emailed import EmailSender


class ErrorCatch(BasicFunctions):
    """Provide working with errors logs."""
    error_log_path = AbsPath.get_path('data', 'error_log')

    def try_email_error_log(self, trace):
        """Try to email error log."""
        unsucsesse = EmailSender().try_email(
            recivers='resivers list',
            subject='PROGRAM ERROR',
            message=trace,
        )
        if unsucsesse:
            self._save_error_log_to_file(trace)

    def _save_error_log_to_file(self, trace):
        """Save log to file."""
        super().dump_data(self.error_log_path, trace)
