from argparse import ArgumentParser, Namespace


def get_argparser(parser: ArgumentParser = None) -> ArgumentParser:
    if not parser:
        parser = ArgumentParser()

    parser.add_argument(
        '--ascii-only',
        action='store_true',
        help='Only use ascii characters in the indicators.')
    parser.add_argument(
        '--no-animation',
        dest='animation',
        action='store_false',
        help='Disable progress animations in console output.')
    parser.add_argument(
        '--no-colors',
        dest='colors',
        action='store_false',
        help='Disable colors in console output.')
    parser.add_argument(
        '--print-output-immediately',
        action='store_true',
        help=(
            'Print task output immediately as it is logged instead of '
            'printing it when the task is completed. If enabled, start of '
            'task is also printed.'))

    return parser


def get_rpa_logger_parameters(args: Namespace) -> dict:
    return dict(
        animations=args.animation,
        colors=args.colors,
        ascii_only=args.ascii_only,
        print_output_immediately=args.print_output_immediately,
    )
