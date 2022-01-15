from collections import Counter
from sys import stdout
from textwrap import indent
from threading import Event, Thread
from typing import Callable, Hashable, Tuple, TextIO
from uuid import uuid4

from .task import *
from .utils.terminal import clear_current_row, print_spinner_and_text, COLORS


def get_indicator(status: str, ascii_only: bool = False) -> Tuple[str, str]:
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
    return f'{num_active} tasks in progress'


class Logger:
    def __init__(
            self,
            animations: bool = True,
            colors: bool = True,
            ascii_only: bool = True,
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

    def bold(self, text: str):
        if not self._colors:
            return text
        return f'\033[1m{text}\033[22m'

    def color(self, text: str, color: str):
        if not self._colors or color not in COLORS:
            return text
        return f'\033[{COLORS[color]}m{text}\033[0m'

    def _print(self, *args, **kwargs):
        return print(*args, file=self._target, **kwargs)

    def error(self, text: str):
        error_text = self.bold(self.color('ERROR:', 'red'))
        self._print(f'{error_text} {text}')

    def title(self, name: str = None, description: str = None):
        name_text = f'{self.bold(name)}\n' if name else ''
        self._print(f'{name_text}{description or ""}\n')

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
        if not key:
            key = uuid4()

        self._active_tasks[key] = text
        self._print_active()
        return key

    def stop_progress_animation(self) -> None:
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
        return self.finish_task(status, text)

    def summary(self) -> int:
        summary = Counter(self._results)

        text = self.bold('Summary:')
        for status in summary:
            indicator = self._get_indicator_text(status)
            text += f'\n{indicator} {status.title()}: {summary.get(status)}'

        self._print(text)

        return summary.get(FAILURE, 0) + summary.get(ERROR, 0)
