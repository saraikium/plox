import sys


class Lox(object):
    def run_file(self, file_path: str)->None:
        with open(file_path) as code:
            self.run(code.read())

    def run_prompt(self ) -> None:

       while True:
           print("> ", end="")
           code_str = input()
           if code_str is None:
               break
           self.run(code_str)



    def run(self, code_str:str) -> None:
        scanner = new scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        print(code_str)


    def main(self) -> None:
        args_len = len(sys.argv)
        if args_len > 2:
            print("Usage: plox [script]")
        elif args_len == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()




if __name__ == "__main__":
    lox = Lox()
    lox.main()
