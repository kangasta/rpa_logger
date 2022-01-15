from os import terminal_size
from unittest import TestCase
from unittest.mock import patch

from rpa_logger.utils.terminal import fit_to_width

TEXT = '\r- Get queued items'
FORMATTED_TEXT = '\r\033[1m- Get queued items\033[22m'

class TerminalUtilsTest(TestCase):
    @patch('rpa_logger.utils.terminal.get_terminal_size')
    def test_fit_to_width_no_truncate(self, get_width_mock):
        get_width_mock.return_value = terminal_size((18, 3))
        self.assertEqual(fit_to_width(TEXT), TEXT)
        self.assertEqual(fit_to_width(FORMATTED_TEXT), FORMATTED_TEXT)

    @patch('rpa_logger.utils.terminal.get_terminal_size')
    def test_fit_to_width_truncate(self, get_width_mock):
        get_width_mock.return_value = terminal_size((16, 3))
        self.assertEqual(
            fit_to_width(TEXT),
            f'{TEXT[:15]}…')
        self.assertEqual(
            fit_to_width(FORMATTED_TEXT),
            f'{FORMATTED_TEXT[:19]}\033[0m…')
