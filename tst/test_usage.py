from io import StringIO
from unittest import TestCase

from rpa_logger import Logger
from rpa_logger.defaults import ERROR, FAILURE, IGNORED, SKIPPED, SUCCESS
from rpa_logger.utils.args import get_argparser, get_rpa_logger_parameters


def target_main(argv, file):
    parser = get_argparser()
    args = parser.parse_args(argv)
    params = get_rpa_logger_parameters(args)

    logger = Logger(**params, target=file)

    logger.title('Test package usage')

    init_key = logger.start_task('Run single task and wait for it to finish.')
    logger.finish_task(SUCCESS, key=init_key)

    key_1 = logger.start_task(
        'Run task and start another while it is running.')

    text_2 = 'Run another task as promised.'
    key_2 = logger.start_task(text_2)

    key_3 = logger.start_task(
        'Run failing task while other two are running.')
    logger.finish_task(FAILURE, key=key_3)

    logger.finish_task(SUCCESS, key=key_1)

    logger.finish_task(SUCCESS, 'Override text.', key=key_2)

    logger.finish_task(SUCCESS, 'Finish task without starting it.')
    logger.log_task(SUCCESS, 'Use log_task method.')

    for status in [SKIPPED, IGNORED, ERROR, 'UNKNOWN', 'CUSTOM']:
        logger.log_task(status, f'Simulate {status} task.')

    return logger.summary()


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
                target_main(argv, file=output_file)
                output = output_file.getvalue()

                for in_check in in_checks:
                    self.assertIn(in_check, output)

                for not_in_check in not_in_checks:
                    self.assertNotIn(not_in_check, output)
