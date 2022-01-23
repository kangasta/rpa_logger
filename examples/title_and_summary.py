from rpa_logger import Logger

l = Logger()
l.title(
    'Demonstrate title and summary usage',
    'Print title, log tasks with different statuses, and print summary')

for status in ['SUCCESS', 'IGNORED', 'FAILURE', 'ERROR', 'SKIPPED', 'UNKNOWN']:
    l.log_task(status, f'Demonstrate {status.lower()} status')

l.finish_suite()

# Summary returns number of non-ok tasks. Use that as exit code.
code = l.summary()
exit(code)
