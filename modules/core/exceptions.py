# Copyright (c) 2026 realgarit
"""Custom exception handlers."""

from __future__ import annotations


class PrettyException(Exception):
    """A base class for exceptions that can be printed with nice formatting."""

    exit_code: int | None = 1
    message_template: str = "{}"
    message_color = "[bold red]"
    recommendation: str = ""
    recommendation_color = "[bold yellow]"

    def bare_message(self) -> PrettyException:
        """Create an exception that doesn't use the pretty formatting."""
        message = self.message_template.format(self.args)
        message = f"{message}\n{self.recommendation}"
        return PrettyException(message)


class PrettyValueError(PrettyException):
    """Used to print a nice error message instead of a standard ValueError."""


class CriticalDirectoryMissing(PrettyException):
    """Exception for when a required directory is missing."""

    message_template = "Could not load {}, the directory does not exist or is not readable."
    recommendation = "Make sure the directory exists and the user has read access."


class CriticalFileMissing(PrettyException):
    """Exception for when a required file is missing."""

    message_template = "Could not load {}, file does not exist."
    recommendation = "Please re-download the program or restore the missing file."


class InvalidConfigData(PrettyException):
    """Exception for when there's an issue with a config file."""

    message_template = "Config file {} is invalid!"
    recommendation = "Please re-download the program or restore/amend the file contents."
