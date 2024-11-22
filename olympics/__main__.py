"""CLI public options."""

import argparse
from . import cli

parser = argparse.ArgumentParser(
    prog='olympics',
    description='Display various information about Olympics results',
)
parser.add_argument(
    'command',
    help='command to launch',
    choices=('countries', 'collective', 'individual'),
)
parser.add_argument(
    '--top',
    help='number of top elements to display',
    type=int,
    default=10,
)
parser.add_argument(
    '--chart',
    help='Display the results as a graph',
    action='store_true'
)

def main(argv=None):
    args = parser.parse_args(argv)
    if (top := args.top) <= 0:
        raise argparse.ArgumentTypeError(f'{top} is not a positive number')
    
    if args.chart:  # Affichage graphique
        match args.command:
            case 'countries':
                cli.plot_top_countries(top)
            case 'collective':
                cli.plot_top_collective(top)
            case 'individual':
                cli.plot_top_individual(top)
    else:  # Affichage console
        match args.command:
            case 'countries':
                cli.top_countries(top)
            case 'collective':
                cli.top_collective(top)
            case 'individual':
                cli.top_individual(top)

if __name__ == '__main__':  # pragma: no cover
    main()
