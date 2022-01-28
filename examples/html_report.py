from io import StringIO
from time import sleep
from uuid import uuid4

from rpa_logger import Logger
from rpa_logger.report import generate_report

l = Logger()

l.title(
    'Example HTML report',
    'Example suite with dummy tasks to demonstrate HTML report feature of <b>rpa_logger</b>.')

key = l.start_task('Task with output')
sleep(1)

l.log_output(key, '# stdin stream can be used, for example, to log executed commands:', stream='stdin')
l.log_output(key, '+ simulalated-command', stream='stdin')
sleep(1)

l.log_output(key, 'Task output in stdout.')
l.log_output(key, 'Task output in stderr.', stream='stderr')
l.finish_task('SUCCESS', key=key)

key = l.start_task('Task with metadata')
task_id = str(uuid4())
l.log_metadata('id', task_id, key)
l.log_output(key, f'+ process-task --id={task_id}', stream='stdin')
sleep(1)

l.log_output(key, 'SUCCESS')
l.finish_task('SUCCESS', key=key)
l.finish_suite()

l.log_task('SKIPPED', 'Task with name\nspanning multiple lines\nand skipped status')

l2 = l.start_suite('Dummy child suite')

for status in ['SUCCESS', 'IGNORED', 'FAILURE', 'ERROR', 'SKIPPED', 'UNKNOWN']:
    l2.log_task(status, f'Demonstrate {status.lower()} status')

l2.finish_suite()
l.finish_task(l2.suite.status, key=l2.suite.key)

generate_report(l.suite)
