'''The default values used by the `rpa_logger` library.
'''

from typing import Tuple


STARTED = 'STARTED'
'''Status for started/in-progress tasks.'''
SUCCESS = 'SUCCESS'
'''Status for successfully finished tasks.'''
IGNORED = 'IGNORED'
'''Status for failed non-critical tasks which failure was ignored.'''
FAILURE = 'FAILURE'
'''Status for task that failed due to an expected error.'''
ERROR = 'ERROR'
'''Status for task that failed due to an unexpected error.'''
SKIPPED = 'SKIPPED'
'''Status for task that was not executed.'''
STATUSES = (STARTED, SUCCESS, IGNORED, FAILURE, ERROR, SKIPPED,)
'''Tuple of all default statuses.'''


def get_indicator(status: str, ascii_only: bool = False) -> Tuple[str, str]:
    '''Default value for `indicator_fn` parameter of
    `rpa_logger.logger.Logger`.

    Args:
        status: Status of the task to be logged.
        ascii_only: If true, use ascii only characters.

    Returns:
        Tuple of color and character to use as the status indicator.
    '''
    if status == SUCCESS:
        return ('green', '✓' if not ascii_only else 'Y',)
    if status == IGNORED:
        return ('magenta', '✓' if not ascii_only else 'I',)
    elif status == FAILURE:
        return ('red', '✗' if not ascii_only else 'X',)
    elif status == ERROR:
        return ('yellow', '!',)
    elif status == SKIPPED:
        return ('blue', '–',)
    elif status == STARTED:
        return ('white', '#',)
    else:
        return ('grey', '?',)


def multiple_active_text(num_active: int) -> str:
    '''Default value for `multiple_fn` parameter of `rpa_logger.logger.Logger`.

    Args:
        num_active: Number of currently active tasks.

    Returns:
        String to print when multiple tasks are in progress.
    '''
    return f'{num_active} tasks in progress'


def is_status_ok(status: str) -> bool:
    '''Default value for `status_ok_fn` parameter of
    `rpa_logger.logger.Logger`.

    Args:
        status: Status to determine OK status for.

    Returns:
        True if given status is OK, False otherwise.
    '''
    return status not in (FAILURE, ERROR,)
