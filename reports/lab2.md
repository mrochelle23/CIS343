# Lab 2: AST Printer

## 1. Overview

The purpose of this lab was to implement an Abstract Syntax Tree (AST) representation and an AST printer for the Nova programming language. The AST represents expressions as objects, and the printer displays the structure of an expression using parentheses.

## 2. Expression Grammar

The expression grammar defines the types of expressions supported by the printer.

```text
expression → or
or → and ( "or" and )*
and → equality ( "and" equality )*
equality → comparison ( ( "!=" | "==" ) comparison )*
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )*
term → factor ( ( "-" | "+" ) factor )*
factor → unary ( ( "/" | "*" ) unary )*
unary → ( "!" | "-" ) unary
      | primary
primary → NUMBER
        | STRING
        | "true"
        | "false"
        | "nil"
        | "(" expression ")"
```

This grammar describes literals, grouping, unary expressions, and binary expressions. The grammar includes operator precedence, with unary expressions taking precedence over multiplication and division, followed by addition and subtraction, comparisons, equality, logical AND, and logical OR.

## 3. Design

The implementation uses four expression classes:

- **Binary:** Stores the left expression, operator, and right expression.
- **Unary:** Stores the operator and right expression.
- **Grouping:** Stores the expression inside parentheses.
- **Literal:** Stores a literal value.

The `AstPrinter` uses visitor methods to print each expression type. Its `parenthesize` method places an operator or grouping label before its child expressions.

Literal values are printed as text. Boolean values are printed as `true` or `false`, and `None` is printed as `nil`.

## 4. Setup and Execution

Run the AST printer from the project root:

```bash
python -m src.ast_printer
```

Expected output:

```text
(* (- 123) (group 45.67))
```

Run the Lab 2 unit tests:

```bash
python -m unittest discover -s test/lab2 -v
```

## 5. Tests

### Test 1: Nested AST

**Purpose:** Verify that nested unary, binary, and grouping expressions are printed with the correct structure.

**Expected output:**

```text
(* (- 123) (group 45.67))
```

**Actual output:** Confirmed by running `python -m src.ast_printer`.

**Result:** Pass.

### Test 2: Operators

**Purpose:** Verify that supported binary operators (`or`, `and`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `+`, `-`, `*`, `/`) and unary operators (`!`, `-`) are printed correctly.

**Result:** Pass.

### Test 3: Literal Types and Grouping

**Purpose:** Verify printing of integer and floating-point numbers, strings, Boolean values, `nil`, and grouping expressions.

**Result:** Pass.

## 6. Test Results

The following command was executed:

```bash
python -m unittest discover -s test/lab2 -v
```

All three unit tests passed:

- `test_all_operators`
- `test_literal_types_and_grouping`
- `test_nested_ast`

The final test summary was:

```text
Ran 3 tests in 0.000s

OK
```

## 7. Limitations

The AST printer represents and prints expressions that are constructed directly in Python. It does not parse Nova source code into an AST. The tests verify the expression classes and printer behavior for the cases included in the test suite.