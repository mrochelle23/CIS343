try:
    from expr import Binary, Unary, Grouping, Literal
except ImportError:
    from .expr import Binary, Unary, Grouping, Literal

class ParseError(Exception):
    """Represents a syntax error found while parsing Nova code."""
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    def parse(self):
        try:
            expression = self.expression()

            if not self.is_at_end():
                self.error(
                    self.peek(),
                    "Unexpected token after expression."
                )

            return expression if not self.errors else None

        except ParseError:
            return None

    # expression -> or
    def expression(self):
        return self.or_expression()

    # or -> and ( "or" and )*
    def or_expression(self):
        expr = self.and_expression()

        while self.match("OR"):
            operator = self.previous()
            right = self.and_expression()
            expr = self.make_binary(expr, operator, right)

        return expr

    # and -> equality ( "and" equality )*
    def and_expression(self):
        expr = self.equality()

        while self.match("AND"):
            operator = self.previous()
            right = self.equality()
            expr = self.make_binary(expr, operator, right)

        return expr

    # equality -> comparison ( ("!=" | "==") comparison )*
    def equality(self):
        expr = self.comparison()

        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expr = self.make_binary(expr, operator, right)

        return expr

    # comparison -> term ( (">" | ">=" | "<" | "<=") term )*
    def comparison(self):
        expr = self.term()

        while self.match(
            "GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"
        ):
            operator = self.previous()
            right = self.term()
            expr = self.make_binary(expr, operator, right)

        return expr

    # term -> factor ( ("-" | "+") factor )*
    def term(self):
        expr = self.factor()

        while self.match("MINUS", "PLUS"):
            operator = self.previous()
            right = self.factor()
            expr = self.make_binary(expr, operator, right)

        return expr

    # factor -> unary ( ("/" | "*") unary )*
    def factor(self):
        expr = self.unary()

        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expr = self.make_binary(expr, operator, right)

        return expr

    # unary -> ("!" | "-") unary | primary
    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()

            return Unary(operator, right)

        return self.primary()

    # primary -> literals | "(" expression ")"
    def primary(self):

        if self.match("FALSE"):
            return Literal(False)

        if self.match("TRUE"):
            return Literal(True)

        if self.match("NIL"):
            return Literal(None)

        if self.match("NUMBER", "STRING"):
            return Literal(self.previous().literal)

        if self.match("LEFT_PAREN"):
            expression = self.expression()
            self.consume(
                "RIGHT_PAREN",
                "Expected ')' after expression."
            )
            return Grouping(expression)

        self.error(self.peek(), "Expected an expression.")

    def make_binary(self, left, operator, right):
        return Binary(left, operator, right)

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        self.error(self.peek(), message)

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type):
        if self.is_at_end():
            return token_type == "EOF"

        return self.peek().token_type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        if token.token_type == "EOF":
            location = " at end"
        else:
            location = f" at '{token.lexeme}'"

        self.errors.append(
            f"[line {token.line}] Syntax error{location}: {message}"
        )
        raise ParseError()
