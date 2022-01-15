from io import StringIO
from unittest import TestCase

from rpa_logger.example import main

class ExampleTest(TestCase):
    def test_args_limit_output_features(self):
        for argv, in_checks, not_in_checks in [
            (['--no-color'], ['\r'], ['\033[1m', '\033[33m']),
            (['--no-animation'], ['\033[1m', '\033[33m'], ['\r']),
            (['--ascii-only'], ['\033[1m', '\033[33m', '\r'], ['✓','✗']),
            ([], ['\033[1m', '\033[33m', '\r', '✓','✗'], []),
        ]:
            with self.subTest(argv=argv):
                output_file = StringIO()
                main([*argv, '--slowness', '0'], file=output_file)
                output = output_file.getvalue()

                for in_check in in_checks:
                    self.assertIn(in_check, output)

                for not_in_check in not_in_checks:
                    self.assertNotIn(not_in_check, output)
