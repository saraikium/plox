import sys
from src import Lox


def main() -> None:
    # Instantiate a new Lox Object
    lox = Lox()
    # Read command line arguments
    args = sys.argv
    args_len = len(args)

    if args_len > 2:
        print("Usage: plox script")
        sys.exit(64)

    # If file name is provided, run code from the file
    elif args_len == 2:
        lox.run_file(args[1])

    # If no filename is provided run the interactive prompt
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
