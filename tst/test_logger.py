from io import StringIO
from unittest import TestCase

from rpa_logger import Logger
from rpa_logger.task import ERROR, STATUSES, SUCCESS

class LoggerTest(TestCase):
    def test_cannot_finish_without_text_or_key(self):
        logger = Logger(target=StringIO())
        with self.assertRaises(RuntimeError):
            logger.finish_task(SUCCESS)

        with self.assertRaises(KeyError):
            logger.finish_task(SUCCESS, key='missing')

        logger.start_task('Test task', key='test-key')
        logger.finish_task(SUCCESS, key='test-key')

    def test_prints_task_output(self):
        target = StringIO()
        logger = Logger(target=target)

        key = logger.start_task('Test task')

        row1 = 'Test text row 1'
        logger.log_output(key, row1)
        row2 = 'Test text row 2'
        logger.log_output(key, row2, 'stderr')

        logger.finish_task(SUCCESS, key=key)
        logger.finish_suite()

        output = target.getvalue()
        self.assertIn(f'\n  {row1}\n', output)
        self.assertIn(f'\n  {row2}\n', output)

    def test_does_not_print_metadata(self):
        target = StringIO()
        logger = Logger(target=target)
        logger.log_metadata('meta_key', 'meta_value')

        self.assertEqual(logger.suite.metadata['meta_key'], 'meta_value')

        output = target.getvalue()
        self.assertNotIn('meta_key', output)
        self.assertNotIn('meta_value', output)

    def test_summary_returns_number_of_failed_tasks(self):
        target = StringIO()
        logger = Logger(target=target)

        for status in STATUSES:
            logger.log_task(status, f'Simulate {status.lower()}')

        logger.finish_suite()

        self.assertEqual(logger.summary(), 2)
        self.assertEqual(logger.suite.status, ERROR)

    def test_finish_suite_sets_ok_suite_status_if_no_failed_tasks(self):
        target = StringIO()
        logger = Logger(target=target)

        logger.log_task(SUCCESS, f'Simulate success')

        logger.finish_suite()

        self.assertEqual(logger.summary(), 0)
        self.assertEqual(logger.suite.status, SUCCESS)

    def test_custom_status_functions(self):
        get_indicator = lambda status, _: ('green', 'O',) if status == 'OK' else ('red', 'X')
        is_status_ok = lambda status: status == 'OK'

        for statuses, num_failed, suite_status in [
            (['OK', 'OK'], 0, 'OK'),
            (['OK', 'NOK', 'ERROR'], 2, 'NOK'),
        ]:
            with self.subTest(statuses=statuses):
                target = StringIO()
                logger = Logger(target=target, indicator_fn=get_indicator, status_ok_fn=is_status_ok)

                for status in statuses:
                    logger.log_task(status, f'Simulate {status.lower()}')

                logger.finish_suite('OK', 'NOK')

                self.assertEqual(logger.summary(), num_failed)
                self.assertEqual(logger.suite.status, suite_status)
