import argparse
import logging


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--start", help="index to start scraping, 0 by default", type=int, default=0)
    parser.add_argument("-e", "--end", help="index to end scraping", type=int, required=True)
    parser.add_argument("-v", "--verbose", help="increases log verbosity", action="store_true")

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    start: int = args.start
    end: int = args.end
    verbose: bool = args.verbose

    print(start, end, verbose)

