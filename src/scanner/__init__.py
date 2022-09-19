from decimal import Decimal
from src.token import Token, TokenType
from src.main import Lox

keywords: dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    source: str = ""  # The source code
    tokens: list[Token] = []  # List of tokens generated from the source code
    keywords: dict[str, TokenType] = keywords  # Reserved keywords
    start: int = 0  # Starting index of lexeme
    current: int = 0  # Index of current character being scanned
    line: int = 1

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(
            Token(type=TokenType.EOF, lexeme="", literal=None, line=self.line)
        )
        return self.tokens

    def advance(self) -> str:
        """
        Get the next character in the sequence. Increment the current index.
        """
        char = self.source[self.current]
        self.current += 1
        return char

    def add_token(self, type: TokenType, literal: object = None):
        lexeme_text: str = self.source[self.start : self.current]
        self.tokens.append(Token(type, lexeme_text, literal, self.line))

    def match_next(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek_ahead(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def string(self) -> None:
        while self.peek_ahead() != '"' and self.is_at_end() is False:
            if self.peek_ahead() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            # Lox.error(self.line, "Unterminated string.")
            return

        # The closing '"'
        self.advance()

        str_value: str = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, str_value)

    def is_digit(self, c: str) -> bool:
        # This might not work in python. Circle back if this doesn't work.
        return c.isnumeric()

    # This method peeks two characters ahead
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_alpha(self, char: str) -> bool:
        return char.isalpha()

    def is_alphanumeric(self, char: str):
        return char.isalnum()

    def number(self) -> None:
        while self.is_digit(self.peek_ahead()):
            self.advance()

        # Look for the decimal part
        if self.peek_ahead() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek_ahead()):
                self.advance()

        self.add_token(
            TokenType.NUMBER, Decimal(self.source[self.start : self.current])
        )

    def identifier(self) -> None:
        while self.is_alphanumeric(self.peek_ahead()):
            self.advance()

        text: str = self.source[self.start : self.current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER

        self.add_token(token_type)

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
                self.add_token(TokenType.MINUS)

            case "+":
                self.add_token(TokenType.PLUS)

            case ";":
                self.add_token(TokenType.SEMI_COLON)

            case "*":
                self.add_token(TokenType.STAR)

            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL
                    if self.match_next("=")
                    else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL
                    if self.match_next("=")
                    else TokenType.EQUAL
                )

            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL
                    if self.match_next("=")
                    else TokenType.LESS
                )

            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL
                    if self.match_next("=")
                    else TokenType.GREATER
                )

            case "/":
                if self.match_next("/"):
                    while (
                        self.peek_ahead() != "\n" and self.is_at_end() is False
                    ):
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)

            # Ignore the whitespace characters
            case " " | "\r" | "\t":
                pass

            case "\n":
                self.line += 1

            case '"':
                self.string()

            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    raise SyntaxError(f"{self.line}: Unexpected character")
                    # Lox.Synr(line=self.line, message="Unexpected character.")
