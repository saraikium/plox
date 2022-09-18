import sys
from src.token import Token
from src.scanner import Scanner


class Lox(object):
    had_error = False

    def run_file(self, file_path: str) -> None:
        with open(file_path) as code:
            self.run(code.read())
        if self.had_error:
            sys.exit(65)

    def run_prompt(self) -> None:
        while True:
            print("> ", end="")
            code_str = input()
            if code_str is None:
                break
            self.run(code_str)
            self.had_error = False

    def run(self, code_str: str) -> None:
        scanner = Scanner(code_str)
        tokens: list[Token] = scanner.scan_tokens()

        # print the tokens
        for token in tokens:
            print(token)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[Line {line} ] Error {where} : {message}")
        Lox.had_error = True

    def main(self) -> None:
        print(sys.argv)
        args_len = len(sys.argv)
        if args_len > 2:
            print("Usage: plox [script]")
        elif args_len == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()


def main() -> None:
    # Instantiate a new Lox Object
    lox = Lox()

    args = sys.argv
    args_len = len(args)

    if args_len > 2:
        print("Usage: plox script")
        sys.exit(64)

    elif args_len == 2:
        lox.run_file(args[1])

    else:
        lox.run_prompt()

    pass


if __name__ == "__main__":
    main()
