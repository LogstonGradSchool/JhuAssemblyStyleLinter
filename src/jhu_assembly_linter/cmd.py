from .linter import Linter


def main():
    import argparse

    parser = argparse.ArgumentParser('A Linter for JHU course EN.605.204')
    parser.add_argument(
        'file',
        help='File to lint',
    )

    args = parser.parse_args()

    linter = Linter(args.file)
    linter.lint()

    for f in linter.findings:
        print(f)


def multi(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser('A Linter for JHU course EN.605.204')
    parser.add_argument(
        'files',
        nargs='*',
        help='Filenames to lint',
    )
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.files:
        linter = Linter(filename)
        linter.lint()

        if linter.findings:
            print(f'--- {filename}')
            for f in linter.findings:
                print(f)

            return_code = 1

    return return_code
