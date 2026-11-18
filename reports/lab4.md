# Lab 4: Statements

## 1. Overview

In this lab, the Nova interpreter was extended to parse and execute statements rather than standalone expressions. Specifically, support was added for expression statements and `print` statements, along with panic-mode error recovery in the parser so that syntax errors can be reported without halting parsing of subsequent statements.

## 2. Grammar

The language grammar was updated so that a program consists of zero or more statements followed by `EOF`:

```text
program → statement* EOF

statement → printStmt
          | exprStmt

printStmt → "print" expression ";"

exprStmt → expression ";"
```

Expression rules (`expression` through `primary`) remain unchanged from Lab 3.

## 3. Implementation

### Statement AST Nodes (`src/stmt.py`)

A new `Stmt` base class and two subclasses were added using the Visitor pattern:

- **`Expression`:** Wraps an expression to be evaluated for side effects, discarding its result.
- **`Print`:** Wraps an expression to be evaluated and printed to standard output.

### Parser Updates & Panic-Mode Recovery (`src/parser.py`)

- `parse()` loops until `EOF`, parsing a sequence of statements and returning a list of `Stmt` nodes.
- `statement()` dispatches to `print_statement()` when encountering a `PRINT` token, or falls back to `expression_statement()`. Both require a terminating semicolon (`;`).
- If a `ParseError` is raised while parsing a statement, `statement()` catches the exception, invokes `synchronize()`, and returns `None` so parsing can continue.
- `synchronize()` discards tokens until it reaches a statement boundary, either immediately after a semicolon (`;`) or before a statement-starting keyword (`VAR`, `FOR`, `IF`, `WHILE`, `PRINT`, `RETURN`).

### Interpreter (`src/interpreter.py` & `src/lox.py`)

- `Interpreter` evaluates expressions (`Literal`, `Grouping`, `Unary`, `Binary`) and executes statements (`Expression` and `Print`).
- Values are formatted via `stringify()`, displaying `None` as `nil`, booleans as `true`/`false`, and whole floating-point numbers without trailing `.0`.
- `Lox.run()` collects both lexical errors from the scanner and syntax errors from the parser before halting execution (exiting with status code `65` in file mode). Runtime errors are caught and reported with line numbers (exiting with status code `70` in file mode).

## 4. Setup and Execution

From the repository root, run a Nova source file using:

```bash
python3 src/lox.py path/to/file.lox
```

To start the interactive REPL prompt (`nova>`):

```bash
python3 src/lox.py
```

## 5. Test Cases and Outputs

### Test Case 1: Syntax Error & Panic-Mode Recovery (`test/lab4/test_errors.lox`)

**Input:**

```lox
"one"
true;
print 2 +
$4+2$;
```

**Command:**

```bash
python3 src/lox.py test/lab4/test_errors.lox
```

**Output:**

```text
[line 4] Error: Unexpected character '$'.
[line 4] Error: Unexpected character '$'.
[line 2] Syntax error at 'true': Expected ';' after expression.
```

*(Note: When `Lox.run` is configured to continue parsing after scanner errors, the parser reports `[line 2] Syntax error at 'true': Expected ';' after expression.`, synchronizes past `true;`, and recovers to parse the remaining tokens on lines 3-4.)*

### Test Case 2: Valid Statements (`test/lab4/test_valid.lox`)

**Input:**

```lox
print "one";
print true;
print 1 + 2;
print nil;
```

**Command:**

```bash
python3 src/lox.py test/lab4/test_valid.lox
```

**Output:**

```text
one
true
3
nil
```

## 6. Conclusion

The Nova interpreter now supports parsing and executing sequences of `print` and expression statements, and uses panic-mode error recovery to report syntax errors and continue parsing subsequent statements.
