'''Tools for presenting `rpa_logger.task.TaskSuite` as a HTML report.
'''

from textwrap import indent
from typing import Callable, List, Tuple

try:
    from jinja2 import Environment, PackageLoader
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

from .defaults import get_indicator
from .task import TaskSuite
from ._version import __version__


GetIndicatorT = Callable[[str, bool], Tuple[str, str]]


def _get_status_to_color_fn(
        get_indicator_fn: GetIndicatorT) -> Callable[[str], str]:
    def _status_to_color(status: str) -> str:
        color, _ = get_indicator_fn(status)
        return color

    return _status_to_color


def _get_status_to_html_fn(
        get_indicator_fn: GetIndicatorT) -> Callable[[str], str]:
    def _status_to_html(status: str) -> str:
        color, symbol = get_indicator_fn(status)
        return f'<span class="status {color}">{symbol}</span>'

    return _status_to_html


def _ensure_html_extension(filename: str) -> str:
    if filename.endswith('.html') or filename.endswith('.htm'):
        return filename
    return f'{filename}.html'


def _child_suites(suite: TaskSuite) -> List[TaskSuite]:
    child_suites = [task for task in suite.tasks if task.type == 'SUITE']
    for child_suite in [*child_suites]:
        child_suites.extend(_child_suites(child_suite))

    return child_suites


def _sorted_child_suites(suite: TaskSuite) -> List[TaskSuite]:
    child_suites = _child_suites(suite)
    child_suites.sort(key=lambda i: i.started)
    return child_suites


def generate_report(
        suite: TaskSuite,
        filename: str = 'rpa_report',
        output_timestamps: bool = True,
        indicator_fn: GetIndicatorT = None):
    '''Generate HTML report for `rpa_logger.task.TaskSuite` into specifed file.

    Args:
        suite: `rpa_logger.task.TaskSuite` to generate report for.
        filename: Target path for the HTML report. If `filename` does not have
            HTML file extension, it is added automatically.
        output_timestamps: If true, timestamps are included in the output log.
        indicator_fn: Function used to determine the color and character for
            the status indicator. Defaults to
            `rpa_logger.defaults.get_indicator`.
    '''
    if not JINJA2_AVAILABLE:
        raise RuntimeError(
            'Generating HTML report requires jinja2 to be installed.')

    env = Environment(loader=PackageLoader('rpa_logger'))
    get_indicator_fn = indicator_fn or get_indicator
    env.filters['status_to_color'] = _get_status_to_color_fn(get_indicator_fn)
    env.filters['status_to_html'] = _get_status_to_html_fn(get_indicator_fn)
    env.filters['indent_name'] = lambda name: indent(name or '', '  ').strip()

    template = env.get_template('report.html.j2')
    stream = template.stream(
        suite=suite,
        child_suites=_sorted_child_suites(suite),
        output_timestamps=output_timestamps,
        version=__version__)

    filename = _ensure_html_extension(filename)
    with open(filename, 'w') as f:
        stream.dump(f)
