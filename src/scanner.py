from token import Token


class Scanner:
    # Nova language token types
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"

    COMMA = "COMMA"
    DOT = "DOT"
    SEMICOLON = "SEMICOLON"

    MINUS = "MINUS"
    PLUS = "PLUS"
    SLASH = "SLASH"
    STAR = "STAR"

    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"

    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"

    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    AND = "AND"
    OR = "OR"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NIL = "NIL"
    VAR = "VAR"
    PRINT = "PRINT"
    RETURN = "RETURN"

    EOF = "EOF"

    keywords = {
        "and": AND,
        "or": OR,
        "if": IF,
        "else": ELSE,
        "while": WHILE,
        "for": FOR,
        "true": TRUE,
        "false": FALSE,
        "nil": NIL,
        "var": VAR,
        "print": PRINT,
        "return": RETURN,
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

        self.errors = []

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(
            Token(self.EOF, "", None, self.line)
        )

        return self.tokens

    def scan_token(self):
        c = self.advance()

        single_char_tokens = {
            "(": self.LEFT_PAREN,
            ")": self.RIGHT_PAREN,
            "{": self.LEFT_BRACE,
            "}": self.RIGHT_BRACE,
            ",": self.COMMA,
            ".": self.DOT,
            ";": self.SEMICOLON,
            "-": self.MINUS,
            "+": self.PLUS,
            "*": self.STAR,
        }

        if c in single_char_tokens:
            self.add_token(single_char_tokens[c])
            return

        if c == "!":
            self.add_token(
                self.BANG_EQUAL if self.match("=") else self.BANG
            )
            return

        if c == "=":
            self.add_token(
                self.EQUAL_EQUAL if self.match("=") else self.EQUAL
            )
            return

        if c == "<":
            self.add_token(
                self.LESS_EQUAL if self.match("=") else self.LESS
            )
            return

        if c == ">":
            self.add_token(
                self.GREATER_EQUAL if self.match("=") else self.GREATER
            )
            return

        if c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(self.SLASH)
            return

        if c in (" ", "\r", "\t"):
            return

        if c == "\n":
            self.line += 1
            return

        if c == '"':
            self.string()
            return

        if self.is_digit(c):
            self.number()
            return

        if self.is_alpha(c):
            self.identifier()
            return

        self.error(
            f"Unexpected character '{c}'."
        )

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]

        token_type = self.keywords.get(
            text,
            self.IDENTIFIER
        )

        self.add_token(token_type)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        value = self.source[self.start:self.current]

        self.add_token(
            self.NUMBER,
            float(value)
        )

    def string(self):
        string_line = self.line

        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.errors.append(
                f"[line {string_line}] Error: Unterminated string."
            )
            return

        self.advance()

        value = self.source[
            self.start + 1:self.current - 1
        ]

        self.add_token(
            self.STRING,
            value
        )

    def is_digit(self, c):
        return c >= "0" and c <= "9"

    def is_alpha(self, c):
        return (
            (c >= "a" and c <= "z")
            or (c >= "A" and c <= "Z")
            or c == "_"
        )

    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected):
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def is_at_end(self):
        return self.current >= len(self.source)

    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]

        self.tokens.append(
            Token(
                token_type,
                text,
                literal,
                self.line
            )
        )

    def error(self, message):
        self.errors.append(
            f"[line {self.line}] Error: {message}"
        )