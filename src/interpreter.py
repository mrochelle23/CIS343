try:
    from .token import Token
except ImportError:
    from token import Token


class LoxRuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token
        self.message = message


class Interpreter:
    def __init__(self):
        self.errors = []

    def interpret(self, statements):
        try:
            for statement in statements:
                if statement is not None:
                    self.execute(statement)
        except LoxRuntimeError as error:
            self.errors.append(
                f"[line {error.token.line}] Runtime error at '{error.token.lexeme}': {error.message}"
            )

    def execute(self, stmt):
        return stmt.accept(self)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        op = expr.operator.token_type

        if op == "BANG":
            return not self.is_truthy(right)
        if op == "MINUS":
            self.check_number_operand(expr.operator, right)
            return -float(right)

        return None

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        op = expr.operator.token_type

        if op == "OR":
            if self.is_truthy(left):
                return left
            return self.evaluate(expr.right)

        if op == "AND":
            if not self.is_truthy(left):
                return left
            return self.evaluate(expr.right)

        right = self.evaluate(expr.right)

        if op == "MINUS":
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        if op == "SLASH":
            self.check_number_operands(expr.operator, left, right)
            if float(right) == 0.0:
                raise LoxRuntimeError(expr.operator, "Division by zero.")
            return float(left) / float(right)
        if op == "STAR":
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        if op == "PLUS":
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise LoxRuntimeError(
                expr.operator,
                "Operands must be two numbers or two strings."
            )
        if op == "GREATER":
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        if op == "GREATER_EQUAL":
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if op == "LESS":
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if op == "LESS_EQUAL":
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        if op == "BANG_EQUAL":
            return not self.is_equal(left, right)
        if op == "EQUAL_EQUAL":
            return self.is_equal(left, right)

        return None

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        if type(a) is not type(b):
            return False
        return a == b

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float) and not isinstance(operand, bool):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if (
            isinstance(left, float) and not isinstance(left, bool)
            and isinstance(right, float) and not isinstance(right, bool)
        ):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def stringify(self, obj):
        if obj is None:
            return "nil"
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
