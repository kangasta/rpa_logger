from time import sleep
from rpa_logger import Logger
from rpa_logger.utils.args import get_argparser, get_rpa_logger_parameters

args = get_argparser().parse_args()
l = Logger(**get_rpa_logger_parameters(args))

key = l.start_task('Log task output')
sleep(1)

l.log_output(key, 'Tasks often produce output.')
sleep(1)

l.log_output(key, 'Output can be logged to tasks.')
sleep(1)

l.finish_task('SUCCESS', key=key)
l.finish_suite()
