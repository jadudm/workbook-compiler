class ParseException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        print(f"Parse exception: {self.message}")