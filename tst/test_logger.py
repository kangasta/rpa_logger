from io import StringIO
from unittest import TestCase

from rpa_logger import Logger
from rpa_logger.task import SUCCESS

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
