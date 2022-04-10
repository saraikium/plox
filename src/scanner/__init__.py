from ..token import Token, TokenType
from ..main import Lox


class Scanner:
    source: str = ""
    tokens: list[Token] = []
    current: int = 0
    start: int = 0
    line: int = 1

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_tokens(self) -> list[Token]:
        while self.is_at_end() is False:
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def advance(self) -> str:

        char = self.source[self.current]
        self.current += 1
        return char

    def add_token(self, type: TokenType, literal: object = None):
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match_next(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def scan_token(self) -> None:
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)

            case ")":
                self.add_token(TokenType.RIGHT_PAREN)

            case "{":
                self.add_token(TokenType.LEFT_BRACE)

            case "}":
                self.add_token(TokenType.RIGHT_BRACE)

            case ",":
                self.add_token(TokenType.COMMA)

            case ".":
                self.add_token(TokenType.DOT)

            case "-":
                self.add_token(TokenType.MINU)

            case "+":
                self.add_token(TokenType.PLUS)

            case ";":
                self.add_token(TokenType.SEMI_COLON)

            case "*":
                self.add_token(TokenType.STAR)

            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match_next("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match_next("=") else TokenType.EQUAL
                )

            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match_next("=") else TokenType.LESS
                )

            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL
                    if self.match_next("=")
                    else TokenType.GREATER
                )

            case "/":
                if self.match_next("/"):
                    while self.peek() != "\n" and self.is_at_end() == False:
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)

            case " ":
                pass

            case "\r":
                pass

            case "\t":
                pass

            case "\n":
                self.line += 1

            case _:
                Lox.error(self.line, "Unexpected character.")
