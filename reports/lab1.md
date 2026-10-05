# Lab 1: Scanning

## 1. Language Design

### Language Name

Nova

### Design Choices

Nova is a small programming language based on the lexical structure of Lox. The language uses familiar programming-language syntax so that variables, expressions, control-flow keywords, and operators can be easily recognized by the scanner.

Nova supports identifiers, numeric literals, string literals, keywords, operators, punctuation, and single-line comments.

The scanner recognizes the following keywords:

* `and`
* `or`
* `if`
* `else`
* `while`
* `for`
* `true`
* `false`
* `nil`
* `var`
* `print`
* `return`

Identifiers may contain letters, digits, and underscores, but must begin with a letter or underscore.

Nova supports integer and decimal numeric literals. Numeric values are stored as floating-point values by the scanner.

Strings are enclosed in double quotation marks. The scanner also allows strings to span multiple lines.

### Differences from Lox

Nova is based on the lexical structure presented in Lox, but the language was designed specifically for this project. Nova uses the keyword set listed above and supports `//` single-line comments.

Block comments using `/* ... */` are not supported. They are scanned as regular operators and identifiers rather than being treated as comments.

Parsing and execution are outside the scope of this lab. This project only implements lexical scanning.

## 2. Lexical Grammar

### Numbers

A number consists of one or more digits, optionally followed by a decimal point and one or more additional digits.

Regular expression:

```text
[0-9]+(\.[0-9]+)?
```

Examples:

```text
0
1
12345
3.14
100.5
0.25
```

The scanner converts numeric literals to floating-point values.

### Strings

A string begins and ends with a double quotation mark.

The scanner accepts any characters until the next double quotation mark, including newline characters. Therefore, Nova supports multiline strings.

A simplified regular expression for the supported form is:

```text
"[^"]*"
```

An unterminated string produces a lexical error.

Examples:

```text
"hello"
"Hello, world!"
""
"This is
a multiline
string"
```

### Identifiers

Identifiers begin with a letter or underscore and may be followed by letters, digits, or underscores.

Regular expression:

```text
[A-Za-z_][A-Za-z0-9_]*
```

Examples:

```text
variable
_variable
variable123
android
printer
```

If an identifier matches one of Nova's reserved keywords, it is returned as the corresponding keyword token instead of an identifier token.

### Keywords

Nova recognizes the following reserved keywords:

```text
and
or
if
else
while
for
true
false
nil
var
print
return
```

For example, `if` is scanned as an `IF` token, while `iffy` is scanned as an `IDENTIFIER` token.

### Operators

Nova supports the following operators:

```text
!
!=
=
==
<
<=
>
>=
+
-
*
/
```

The scanner uses lookahead when necessary to distinguish single-character operators from two-character operators. For example, `=` produces an `EQUAL` token while `==` produces an `EQUAL_EQUAL` token.

### Comments

Nova supports single-line comments beginning with `//`.

Everything from `//` to the end of the line is ignored by the scanner.

Example:

```text
var x = 10; // this is a comment
```

Block comments using `/* ... */` are not supported.

### Whitespace

Spaces, tabs, and carriage returns are ignored.

Newline characters are also ignored as tokens, but the scanner increments its line counter whenever it encounters a newline. This allows lexical errors to report the appropriate source line.

## 3. Implementation

### Token Class

The `Token` class stores four pieces of information:

* Token type
* Lexeme
* Literal value
* Line number

Each token can be printed in the following format:

```text
TOKEN_TYPE lexeme literal
```

For example:

```text
NUMBER 123 123.0
IDENTIFIER variable None
STRING "hello" hello
```

### Scanner

The `Scanner` class processes the source code one character at a time.

The scanner maintains:

* `start` — the beginning of the current lexeme
* `current` — the current position in the source
* `line` — the current source-code line
* `tokens` — the list of generated tokens
* `errors` — the list of lexical errors

The scanner recognizes single-character tokens, two-character operators, comments, whitespace, strings, numbers, identifiers, and keywords.

When an unexpected character is encountered, the scanner records an error and continues scanning. This allows additional tokens and errors to be detected rather than terminating the entire scan.

Unterminated strings are also reported as lexical errors. The scanner records the line where the string began, even if the scanner reaches a later line before determining that the string is unterminated.

### Entry Point

The program is started through `src/lox.py`.

The entry point supports two modes:

1. Source-file mode
2. Interactive mode

The entry point creates a `Scanner`, scans the source, prints any scanner errors, and then prints the generated tokens.

## 4. Setup and Usage

### Source File Mode

A Nova source file can be scanned by passing its path to `lox.py`.

Example:

```bash
python src/lox.py test/lab1/all_tokens.lox
```

When a lexical error occurs in source-file mode, the program exits with status code `65`.

For example:

```bash
python src/lox.py test/lab1/errors.lox
echo $?
```

produces an exit status of:

```text
65
```

### Interactive Mode

Running `lox.py` without a source-file argument starts the Nova prompt:

```bash
python src/lox.py
```

The prompt is:

```text
nova>
```

Each line is scanned independently. After an error, the prompt remains available so additional input can be processed.

## 5. Testing

### Test 1: All Tokens

**Purpose:**

Verify that the scanner recognizes every supported token type.

**Input:**

`test/lab1/all_tokens.lox`

**Expected:**

The scanner should produce a token for every supported token type and finish with an `EOF` token.

**Actual:**

The scanner produced tokens for all supported token types, including:

```text
LEFT_PAREN
RIGHT_PAREN
LEFT_BRACE
RIGHT_BRACE
COMMA
DOT
SEMICOLON
PLUS
MINUS
STAR
SLASH
BANG
BANG_EQUAL
EQUAL
EQUAL_EQUAL
LESS
LESS_EQUAL
GREATER
GREATER_EQUAL
AND
OR
IF
ELSE
WHILE
FOR
TRUE
FALSE
NIL
VAR
PRINT
RETURN
IDENTIFIER
NUMBER
STRING
EOF
```

**Result:**

Passed.

### Test 2: Numbers

**Purpose:**

Verify that integer and decimal numeric literals are recognized correctly.

**Input:**

`test/lab1/numbers.lox`

**Expected:**

Each numeric value should produce a `NUMBER` token with the appropriate floating-point literal value.

**Actual:**

The scanner correctly recognized values including:

```text
0
1
10
12345
3.14
100.5
0.25
999.999
```

**Result:**

Passed.

### Test 3: Identifiers and Keywords

**Purpose:**

Verify that keywords are distinguished from identifiers with similar names.

**Input:**

`test/lab1/identifiers.lox`

**Expected:**

Reserved words should produce keyword tokens, while similar but non-reserved words should produce `IDENTIFIER` tokens.

**Actual:**

Examples included:

```text
and      -> AND
android  -> IDENTIFIER
if       -> IF
iffy     -> IDENTIFIER
var      -> VAR
variable -> IDENTIFIER
print    -> PRINT
printer  -> IDENTIFIER
true     -> TRUE
truth    -> IDENTIFIER
```

**Result:**

Passed.

### Test 4: Comments

**Purpose:**

Verify that single-line comments are ignored.

**Input:**

`test/lab1/comments.lox`

**Expected:**

Text following `//` should not produce tokens.

**Actual:**

The scanner ignored the `//` comments and correctly scanned the code surrounding them.

A `/* ... */` example was also included. Since block comments are not part of Nova's lexical grammar, those characters were scanned as normal tokens.

**Result:**

Passed for the supported `//` comment syntax.

### Test 5: Strings

**Purpose:**

Verify that strings are scanned correctly, including empty strings and strings containing spaces.

**Input:**

`test/lab1/strings.lox`

**Expected:**

Each quoted value should produce a `STRING` token with the quotation marks excluded from the literal value.

**Actual:**

The scanner correctly recognized:

```text
"hello"
"Hello, world!"
"Nova"
"123"
""
"spaces inside a string"
```

**Result:**

Passed.

### Test 6: Lexical Errors

**Purpose:**

Verify that unexpected characters are reported as lexical errors and that scanning continues afterward.

**Input:**

`test/lab1/errors.lox`

**Expected:**

The scanner should report an error for unsupported characters while continuing to scan the remainder of the source file.

**Actual:**

The scanner reported:

```text
[line 1] Error: Unexpected character '@'.
[line 2] Error: Unexpected character '#'.
[line 3] Error: Unexpected character '&'.
```

It then successfully produced the remaining tokens.

The source-file process exited with status code `65`.

**Result:**

Passed.

### Test 7: Unterminated String

**Purpose:**

Verify that an unterminated string is detected and that the error is associated with the line where the string began.

**Input:**

`test/lab1/unterminated_string.lox`

**Expected:**

The scanner should report an unterminated-string error on line 1.

**Actual:**

```text
[line 1] Error: Unterminated string.
PRINT print None
EOF  None
```

The scanner correctly reported line 1 even though it reached the end of the source after the line-ending newline.

**Result:**

Passed.

### Test 8: Interactive Recovery

**Purpose:**

Verify that the interactive interpreter remains usable after a lexical error.

**Input:**

The following commands were entered interactively:

```text
var x = 10;
@
print x;
```

**Expected:**

The first command should produce valid tokens. The invalid `@` should produce an error without terminating the interpreter. The third command should then be processed normally.

**Actual:**

The interpreter produced the expected tokens for `var x = 10;`, reported:

```text
[line 1] Error: Unexpected character '@'.
```

and then successfully scanned:

```text
print x;
```

The interpreter remained at the `nova>` prompt after the error and exited normally with `Ctrl-D`.

**Result:**

Passed.

## 6. Known Limitations

Nova currently implements lexical scanning only. It does not parse or execute programs.

The scanner does not support block comments using `/* ... */`. Only `//` single-line comments are supported.

String escape sequences are not implemented as a separate lexical feature. Strings are scanned until the next double quotation mark.

## 7. Conclusion

The Nova scanner successfully implements the required lexical scanning functionality. It recognizes identifiers, keywords, numeric and string literals, operators, punctuation, comments, and end-of-file. It also reports unexpected characters and unterminated strings while continuing to scan when possible.

Testing was performed in both source-file and interactive modes. The source-file tests successfully produced the expected tokens and error behavior, including the required exit status of `65` for lexical errors. Interactive testing also demonstrated that the interpreter can recover from an invalid character and continue processing subsequent input.

The completed scanner provides the lexical-analysis foundation for future parsing and execution stages of the Nova interpreter.

