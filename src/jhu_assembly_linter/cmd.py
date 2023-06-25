from .linter import Linter


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        help='File to lint',
    )

    args = parser.parse_args()

    linter = Linter(args.file)
    linter.lint()

    for f in linter.findings:
        print(f)
