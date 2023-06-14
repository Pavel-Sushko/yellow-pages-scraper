import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Yellow Pages Scraper')

    parser.add_argument('-s', '--search', type=str,
                        required=True, help='Search term')

    parser.add_argument('-o', '--output', type=str,
                        default='data/contacts', help='Output file name')

    parser.add_argument('-f', '--format', type=list or str, default=[
                        'json', 'csv'], nargs='+', choices=['json', 'csv'], help='Output format')

    parser.add_argument('-w', '--website', action='store_true',
                        help='Filter out listings with websites')

    return parser.parse_args()
