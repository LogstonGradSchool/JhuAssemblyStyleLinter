from .linter import Linter


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        help='File to lint',
    )

    args = parser.parse_args()

    l = Linter(args.file)
    l.lint()

    for f in l.findings():
        print(f)
