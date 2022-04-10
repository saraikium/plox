from ..token import Token, TokenType


class Scanner:
    source: str = ""
    tokens: list[Token] = []
    current: int = 0
    start: int = 0
    line: int = 1

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []

    def advance(self) -> str:

        char = self.source[self.current]
        self.current += 1
        return char

    def add_token(self, type: TokenType, literal: object = None):
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

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

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_tokens(self) -> list[Token]:
        while self.is_at_end() is False:
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
