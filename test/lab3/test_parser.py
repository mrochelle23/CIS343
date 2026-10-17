
# --- start AI code ---
import unittest

from src.scanner import Scanner
from src.parser import Parser
from src.ast_printer import AstPrinter


class TestParser(unittest.TestCase):
    def parse_expression(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        self.assertEqual(
            scanner.errors, [],
            f"Scanner errors for {source!r}: {scanner.errors}"
        )

        parser = Parser(tokens)
        expression = parser.parse()

        self.assertEqual(
            parser.errors, [],
            f"Parser errors for {source!r}: {parser.errors}"
        )
        self.assertIsNotNone(expression)

        return AstPrinter().print_expr(expression)

    def test_operator_precedence(self):
        self.assertEqual(
            self.parse_expression("1 + 2 * 3"),
            "(+ 1.0 (* 2.0 3.0))"
        )

    def test_grouping(self):
        self.assertEqual(
            self.parse_expression("(1 + 2) * 3"),
            "(* (group (+ 1.0 2.0)) 3.0)"
        )

    def test_left_associativity(self):
        self.assertEqual(
            self.parse_expression("1 - 2 - 3"),
            "(- (- 1.0 2.0) 3.0)"
        )

    def test_unary_operators(self):
        self.assertEqual(self.parse_expression("-5"), "(- 5.0)")
        self.assertEqual(self.parse_expression("!true"), "(! true)")

    def test_literal_types(self):
        self.assertEqual(self.parse_expression("true"), "true")
        self.assertEqual(self.parse_expression("false"), "false")
        self.assertEqual(self.parse_expression("nil"), "nil")
        self.assertEqual(self.parse_expression('"hello"'), "hello")
        self.assertEqual(self.parse_expression("42"), "42.0")

    def test_equality_and_comparison(self):
        self.assertEqual(
            self.parse_expression("1 < 2 == true"),
            "(== (< 1.0 2.0) true)"
        )

    def test_logical_operators(self):
        self.assertEqual(
            self.parse_expression("true or false and true"),
            "(or true (and false true))"
        )

    def test_missing_operand(self):
        parser = Parser(Scanner("1 +").scan_tokens())
        self.assertIsNone(parser.parse())
        self.assertTrue(parser.errors)

    def test_missing_right_parenthesis(self):
        parser = Parser(Scanner("(1 + 2").scan_tokens())
        self.assertIsNone(parser.parse())
        self.assertTrue(parser.errors)

    def test_unexpected_trailing_token(self):
        parser = Parser(Scanner("1 2").scan_tokens())
        self.assertIsNone(parser.parse())
        self.assertTrue(parser.errors)

    def test_unexpected_operator(self):
        parser = Parser(Scanner("* 2").scan_tokens())
        self.assertIsNone(parser.parse())
        self.assertTrue(parser.errors)


if __name__ == "__main__":
    unittest.main()
# --- end AI code ---
