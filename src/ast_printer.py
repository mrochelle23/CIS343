
try:
    from .expr import Binary, Unary, Grouping, Literal
except ImportError:
    from expr import Binary, Unary, Grouping, Literal


class AstPrinter:
    def print_expr(self, expression):
        return expression.accept(self)

    def visit_binary_expr(self, expr):
        return self.parenthesize(
            expr.operator.lexeme,
            expr.left,
            expr.right
        )

    def visit_unary_expr(self, expr):
        return self.parenthesize(
            expr.operator.lexeme,
            expr.right
        )

    def visit_grouping_expr(self, expr):
        return self.parenthesize(
            "group",
            expr.expression
        )

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        if expr.value is True:
            return "true"
        if expr.value is False:
            return "false"
        return str(expr.value)

    def parenthesize(self, name, *expressions):
        parts = [name]

        for expression in expressions:
            parts.append(self.print_expr(expression))

        return "(" + " ".join(parts) + ")"
# --- end AI code ---


if __name__ == "__main__":
    # --- start AI code ---
    from_token = None
    try:
        from .token import Token
    except ImportError:
        from token import Token

    expression = Binary(
        Unary(
            Token("MINUS", "-", None, 1),
            Literal(123)
        ),
        Token("STAR", "*", None, 1),
        Grouping(Literal(45.67))
    )

    print(AstPrinter().print_expr(expression))
