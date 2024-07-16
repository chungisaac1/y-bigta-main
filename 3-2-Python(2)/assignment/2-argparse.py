import argparse
import logging


def create_parser() -> argparse.ArgumentParser:
    # 구현하세요!
    pass


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    start: int = args.start
    end: int = args.end
    verbose: bool = args.verbose

    print(start, end, verbose)

