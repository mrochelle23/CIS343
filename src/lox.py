import sys

from error import Error


class Lox:

    def run(self, source):
        # Scanner will be implemented later.
        print(source)
        Error.error("Scanner Not Implemented")

    def run_file(self, filename):
        try:
            with open(filename, "r") as file:
                source = file.read()

            self.run(source)

        except FileNotFoundError:
            Error.error(f"Could not open file '{filename}'.")

    def run_prompt(self):
        while True:
            try:
                line = input("> ")

                self.run(line)

                # Errors in one REPL input should not
                # prevent the next input from running.
                Error.had_error = False

            except KeyboardInterrupt:
                print()
                break

            except EOFError:
                print()
                break


def main():
    lox = Lox()

    if len(sys.argv) > 2:
        print("Usage: python src/lox.py [script]")
        sys.exit(1)

    if len(sys.argv) == 2:
        lox.run_file(sys.argv[1])

        if Error.had_error:
            sys.exit(1)

    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()