from dataclasses import asdict
import json
from unittest import TestCase
from uuid import uuid4

from rpa_logger.task import ERROR, FAILURE, SKIPPED, SUCCESS, TaskSuite

class TaskTest(TestCase):
    def test_active_tasks(self):
        suite = TaskSuite('Test suite')
        key1 = suite.create_task('1st test task')
        key2 = suite.create_task('2nd test task')
        key3 = suite.create_task('3rd test task')

        self.assertEqual(len(suite.tasks), 3)
        self.assertEqual(len(suite.active_tasks), 3)

        suite.finish_task(key2, SUCCESS)
        suite.finish_task(key3, ERROR)

        self.assertEqual(len(suite.tasks), 3)
        self.assertEqual(len(suite.active_tasks), 1)

    def test_log_output_to_task(self):
        suite = TaskSuite('Test suite')
        key1 = suite.create_task('1st test task')
        output1 = 'Test stdout'
        suite.log_output(key1, output1)

        self.assertEqual(len(suite.tasks[0].output), 1)
        self.assertEqual(suite.tasks[0].output[0].text, output1)
        self.assertEqual(suite.tasks[0].output[0].stream, 'stdout')

        output2 = 'Test stderr'
        suite.log_output(key1, output2, 'stderr')

        self.assertEqual(len(suite.tasks[0].output), 2)
        self.assertEqual(suite.tasks[0].output[1].text, output2)
        self.assertEqual(suite.tasks[0].output[1].stream, 'stderr')

    def test_update_undefined_key(self):
        suite = TaskSuite('Test suite')
        with self.assertRaises(KeyError):
            suite.log_output(uuid4(), 'Test output')

        with self.assertRaises(KeyError):
            suite.log_metadata('meta_key', 'meta_value', uuid4())

    def test_log_metadata(self):
        suite = TaskSuite('Test suite')
        self.assertEqual(len(suite.metadata), 0)

        suite.log_metadata('meta_key', 'meta_value')
        self.assertEqual(len(suite.metadata), 1)

        key = suite.log_task('Test task', SUCCESS)
        self.assertEqual(len(suite.tasks[0].metadata), 0)

        suite.log_metadata('meta_key', 'meta_value', key)
        self.assertEqual(len(suite.tasks[0].metadata), 1)

    def test_task_status_counter(self):
        suite = TaskSuite('Test suite')
        for i in [SUCCESS, SUCCESS, ERROR, SKIPPED]:
            suite.log_task(i, 'Test task')

        counter = suite.task_status_counter
        self.assertEqual(counter[SUCCESS], 2)
        self.assertEqual(counter[ERROR], 1)
        self.assertEqual(counter[SKIPPED], 1)
        self.assertEqual(counter[FAILURE], 0)

    def test_custom_task_key(self):
        suite = TaskSuite('Test suite')
        self.assertIsNone(suite.get_task('asd'))

        suite.create_task('Test task', key='asd')
        self.assertIsNotNone(suite.get_task('asd'))
        suite.finish_task('asd', SUCCESS)

    def test_suite_json_serialization(self):
        suite = TaskSuite('Test suite')
        key = suite.create_task('Started task')
        output = 'Loading content'
        suite.log_output(key, output)
        suite.log_task(SUCCESS, 'Success task')
        suite.log_metadata('meta_key', 'meta_value')

        suite_dict = asdict(suite)
        self.assertEqual(suite_dict['type'], 'SUITE')
        self.assertEqual(len(suite_dict['tasks']), 2)
        self.assertEqual(suite_dict['tasks'][0]['type'], 'TASK')
        self.assertEqual(suite_dict['tasks'][0]['output'][0]['text'], output)

        json.dumps(suite_dict)
