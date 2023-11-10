class ParseException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"parse exception: {self.message}"


class RenderException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"render exception: {self.message}"
