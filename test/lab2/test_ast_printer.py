
import unittest

from src.expr import Binary, Unary, Grouping, Literal
from src.token import Token
from src.ast_printer import AstPrinter


def make_operator(lexeme):
    return Token("OPERATOR", lexeme, None, 1)


class AstPrinterTests(unittest.TestCase):
    def setUp(self):
        self.printer = AstPrinter()

    def test_nested_ast(self):
        expression = Binary(
            Unary(
                make_operator("-"),
                Literal(123)
            ),
            make_operator("*"),
            Grouping(Literal(45.67))
        )

        expected = "(* (- 123) (group 45.67))"
        self.assertEqual(self.printer.print_expr(expression), expected)

    def test_all_operators(self):
        binary_operators = [
            "or", "and", "==", "!=", ">", ">=",
            "<", "<=", "+", "-", "*", "/"
        ]

        for operator in binary_operators:
            with self.subTest(operator=operator):
                expression = Binary(
                    Literal(1),
                    make_operator(operator),
                    Literal(2)
                )

                expected = f"({operator} 1 2)"
                self.assertEqual(
                    self.printer.print_expr(expression),
                    expected
                )

        for operator in ["!", "-"]:
            with self.subTest(unary_operator=operator):
                expression = Unary(
                    make_operator(operator),
                    Literal(1)
                )

                expected = f"({operator} 1)"
                self.assertEqual(
                    self.printer.print_expr(expression),
                    expected
                )

    def test_literal_types_and_grouping(self):
        examples = [
            (Literal(42), "42"),
            (Literal(3.14), "3.14"),
            (Literal("Nova"), "Nova"),
            (Literal(True), "true"),
            (Literal(False), "false"),
            (Literal(None), "nil"),
            (Grouping(Literal("Nova")), "(group Nova)")
        ]

        for expression, expected in examples:
            with self.subTest(expected=expected):
                self.assertEqual(
                    self.printer.print_expr(expression),
                    expected
                )


if __name__ == "__main__":
    unittest.main()
