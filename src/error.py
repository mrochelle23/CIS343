class Error:
    had_error = False

    @staticmethod
    def error(message):
        print(f"Error: {message}")
        Error.had_error = True