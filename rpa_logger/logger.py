'''The main interface for using the `rpa_logger` package.

This module contains the `rpa_logger.logger.Logger` class and default
functions it uses for its callback parameters.
'''

from collections import Counter
from sys import stdout
from textwrap import indent
from threading import Event, Thread
from typing import Callable, Hashable, Tuple, TextIO
from uuid import uuid4

from .task import *
from .utils.terminal import clear_current_row, print_spinner_and_text, COLORS


def get_indicator(status: str, ascii_only: bool = False) -> Tuple[str, str]:
    '''Default value for `indicator_fn` parameter of
    `rpa_logger.logger.Logger`.

    Args:
        status: Status of the task to be logged.
        ascii_only: If true, use ascii only characters.

    Returns:
        Tuple of color and character to use as the status indicator.
    '''
    if status == SUCCESS:
        return ('green', '✓' if not ascii_only else 'Y',)
    if status == IGNORED:
        return ('magenta', '✓' if not ascii_only else 'I',)
    elif status == FAILURE:
        return ('red', '✗' if not ascii_only else 'X',)
    elif status == ERROR:
        return ('yellow', '!',)
    elif status == SKIPPED:
        return ('blue', '–',)
    else:
        return ('grey', '?',)


def multiple_active_text(num_active: int) -> str:
    '''Default value for `multiple_fn` parameter of `rpa_logger.logger.Logger`.

    Args:
        num_active: Number of currently active tasks.

    Returns:
        String to print when multiple tasks are in progress.
    '''
    return f'{num_active} tasks in progress'


class Logger:
    '''Interface for logging RPA tasks.

    Args:
        animations: If true, progress indicator is displayed.
        colors: If true, ANSI escape codes are used when logging to console.
        ascii_only: If true, use ascii only spinner and status indicators.
        target: File to print output to. Defaults to stdout.
        multiple_fn: Function used to determine progress message when multiple
            tasks are in progress. Defaults to
            `rpa_logger.logger.multiple_active_text`.
        indicator_fn: Function used to determine the color and character for
            the status indicator. Defaults to
            `rpa_logger.logger.get_indicator`.
    '''

    def __init__(
            self,
            animations: bool = True,
            colors: bool = True,
            ascii_only: bool = False,
            target: TextIO = None,
            multiple_fn: Callable[[int], str] = None,
            indicator_fn: Callable[[str, bool], Tuple[str, str]] = None):
        self._animations = animations
        self._colors = colors
        self._ascii_only = ascii_only
        self._target = target or stdout

        self._get_multiple_active_str = multiple_fn or multiple_active_text
        self._get_progress_indicator = indicator_fn or get_indicator

        self._active_tasks = dict()
        self._results = []

        self._spinner_thread = None
        self._spinner_stop_event = Event()

    def bold(self, text: str) -> str:
        '''Bold given text with ANSI escape codes.

        Args:
            text: Text to be formatted.

        Returns:
            String with formatted text.
        '''
        if not self._colors:
            return text
        return f'\033[1m{text}\033[22m'

    def color(self, text: str, color: str) -> str:
        '''Color given text with ANSI escape codes.

        Args:
            text: Text to be formatted.
            color: Color to format text with. See
                `rpa_logger.utils.terminal.COLORS` for available values.

        Returns:
            String with formatted text.
        '''
        if not self._colors or color not in COLORS:
            return text
        return f'\033[{COLORS[color]}m{text}\033[39m'

    def _print(self, *args, **kwargs):
        return print(*args, file=self._target, **kwargs)

    def error(self, text: str) -> None:
        '''Print error message.

        Args:
            text: Error message text.
        '''
        error_text = self.bold(self.color('ERROR:', 'red'))
        self._print(f'{error_text} {text}')

    def title(self, title: str = None, description: str = None) -> None:
        '''Print title and description of the RPA process.

        Args:
            title: Title to print in bold.
            description: Description to print under the title.
        '''
        title_text = f'{self.bold(title)}\n' if title else ''
        self._print(f'{title_text}{description or ""}\n')

    def _print_active(self):
        if not self._animations:
            return

        num_active = len(self._active_tasks)
        if not num_active:
            return
        elif num_active > 1:
            text = self._get_multiple_active_str(num_active)
        else:
            text = list(self._active_tasks.values())[0]

        clear_current_row(self._target)
        self.stop_progress_animation()

        self._spinner_thread = Thread(
            target=print_spinner_and_text,
            args=[
                text,
                self._spinner_stop_event,
                self._target,
                self._ascii_only])
        self._spinner_stop_event.clear()
        self._spinner_thread.start()

    def start_task(self, text: str, key: Hashable = None) -> Hashable:
        '''Create a new active task and print progress indicator.

        Args:
            text: Name or description of the task.
            key: Key to identify the task with. If not provided, new uuid4
                will be used.

        Return:
            Key to control to the created task with.
        '''
        if not key:
            key = uuid4()

        self._active_tasks[key] = text
        self._print_active()
        return key

    def stop_progress_animation(self) -> None:
        '''Stop possible active progress indicators.
        Should be used, for example, if the application is interrupted while
        there are active progress indicators.
        '''
        self._spinner_stop_event.set()
        if self._spinner_thread:
            self._spinner_thread.join()
            self._spinner_thread = None

    def _get_indicator_text(self, status):
        color, symbol = self._get_progress_indicator(status, self._ascii_only)
        return self.bold(self.color(symbol, color))

    def finish_task(
            self,
            status: str,
            text: str = None,
            key: Hashable = None) -> None:
        '''Finish active or new task and print its status.

        Calling this method is required to stop the progress spinner of a
        previously started task.

        Args:
            status: Status string used to determine the status indicator.
            text: Text to describe the task with. Defaults to the text used
                when the task was created if `key` is given.
            key: Key of the previously created task to be finished.
        '''
        self.stop_progress_animation()

        if key:
            start_text = self._active_tasks.pop(key, None)
            text = text or start_text

        if not text:
            raise RuntimeError(
                f'No text provided or found for given key ({key}).')

        self._results.append(status)

        indicator_text = self._get_indicator_text(status)
        indented_text = indent(text, '  ').strip()

        self._print(f'{indicator_text} {indented_text}\n')
        self._print_active()

    def log_task(self, status: str, text: str) -> None:
        '''Alias for `rpa_logger.logger.Logger.finish_task`.
        This method can be used when the task to be logged was not previously
        started.
        '''
        return self.finish_task(status, text)

    def summary(self) -> int:
        '''Print summary of the logged tasks.

        Returns:
            Number of failed (status is either `FAILURE` or `ERROR`) tasks.
        '''
        summary = Counter(self._results)

        text = self.bold('Summary:')
        for status in summary:
            indicator = self._get_indicator_text(status)
            text += f'\n{indicator} {status.title()}: {summary.get(status)}'

        self._print(text)

        return summary.get(FAILURE, 0) + summary.get(ERROR, 0)
