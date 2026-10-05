import sys

from scanner import Scanner


class Lox:
    had_error = False

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
        with open(path, "r") as file:
            source = file.read()

        Lox.run(source)

        if Lox.had_error:
            sys.exit(65)

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

            Lox.run(line)

            Lox.had_error = False

    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for error in scanner.errors:
            print(error)
        # --- start AI code ---
        if scanner.errors:
            Lox.had_error = True
        # -- end AI code ---
        for token in tokens:
            print(token)


if __name__ == "__main__":
    Lox.main()