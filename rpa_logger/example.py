from time import sleep
from typing import Sequence, TextIO

from rpa_logger import Logger
from rpa_logger.task import ERROR, FAILURE, IGNORED, SKIPPED, SUCCESS
from rpa_logger.utils.args import get_argparser, get_rpa_logger_parameters


def main(argv: Sequence[str] = None, file: TextIO = None):
    '''Print example output via rpa_logger

    This function/app provides an example for usage and output of rpa_logger.
    '''
    parser = get_argparser()
    parser.add_argument(
        '--slowness',
        type=int,
        nargs='?',
        default=1,
        help='Multiplier for sleep times.')
    args = parser.parse_args(argv)
    params = get_rpa_logger_parameters(args)

    logger = Logger(**params, target=file)

    title, raw_description = main.__doc__.split('\n', 1)
    logger.title(title, raw_description.strip())

    init_key = logger.start_task('Run single task and wait for it to finish.')
    sleep(2 * args.slowness)
    logger.finish_task(SUCCESS, key=init_key)

    key_1 = logger.start_task(
        'Run task and start another while it is running.')
    sleep(2 * args.slowness)

    text_2 = 'Run another task as promised.'
    key_2 = logger.start_task(text_2)
    sleep(1 * args.slowness)

    key_3 = logger.start_task(
        'Run short failing task while other two are running.')
    sleep(1 * args.slowness)
    logger.finish_task(FAILURE, key=key_3)

    sleep(1 * args.slowness)
    logger.finish_task(SUCCESS, key=key_1)

    sleep(2 * args.slowness)
    logger.finish_task(
        SUCCESS,
        'Text can be overridden when finishing task.\n'
        f'This task used text "{text_2}" on start.',
        key=key_2)

    logger.finish_task(
        SUCCESS,
        'Task can be finished without starting it, if progress indicator is'
        'not required.')

    logger.log_task(
        SUCCESS,
        'Alternatively, log_task method can be used to log short tasks.')

    logger.log_task(SKIPPED, 'Simulate SKIPPED task.')
    logger.log_task(IGNORED, 'Simulate IGNORED task.')
    logger.log_task(ERROR, 'Simulate ERROR task.')
    logger.log_task('UNKNOWN', 'Simulate UNKNOWN task.')
    logger.log_task('CUSTOM', 'Simulate CUSTOM task.')

    return logger.summary()


if __name__ == '__main__':
    code = main()
    exit(code)
