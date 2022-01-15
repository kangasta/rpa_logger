from io import StringIO
from unittest import TestCase

from rpa_logger import Logger
from rpa_logger.task import SUCCESS

class LoggerTest(TestCase):
    def test_cannot_finish_without_text_or_key(self):
        logger = Logger(target=StringIO())
        with self.assertRaises(RuntimeError):
            logger.finish_task(SUCCESS)

        with self.assertRaises(RuntimeError):
            logger.finish_task(SUCCESS, key='missing')

        logger.start_task('Test task', key='test-key')
        logger.finish_task(SUCCESS, key='test-key')
