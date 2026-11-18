import sys

try:
    from scanner import Scanner
    from parser import Parser
    from ast_printer import AstPrinter
    from interpreter import Interpreter
except ImportError:
    from .scanner import Scanner
    from .parser import Parser
    from .ast_printer import AstPrinter
    from .interpreter import Interpreter


class Lox:
    had_error = False
    had_runtime_error = False
    interpreter = Interpreter()

    @staticmethod
    def main():
        if len(sys.argv) > 2:
            print("Usage: python src/lox.py [script]")
            sys.exit(1)

        if len(sys.argv) == 2:
            Lox.run_file(sys.argv[1])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(path):
        try:
            with open(path, "r") as file:
                source = file.read()
        except OSError as error:
            print(f"Could not read file '{path}': {error}")
            sys.exit(74)

        Lox.run(source)

        if Lox.had_error:
            sys.exit(65)
        if Lox.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("nova> ")
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()
                continue

            Lox.had_error = False
            Lox.had_runtime_error = False
            Lox.run(line)

    # --- start AI code ---
    @staticmethod
    def run(source):
        if not source.strip():
            return
    # --- end AI code ---
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        if scanner.errors:
            for error in scanner.errors:
                print(error)
            Lox.had_error = True
            return

        parser = Parser(tokens)
        statements = parser.parse()

        if parser.errors:
            for error in parser.errors:
                print(error)
            Lox.had_error = True
            return

        Lox.interpreter.errors = []
        Lox.interpreter.interpret(statements)

        if Lox.interpreter.errors:
            for error in Lox.interpreter.errors:
                print(error)
            Lox.had_runtime_error = True


if __name__ == "__main__":
    Lox.main()
