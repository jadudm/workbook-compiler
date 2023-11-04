from parser.range import Range

class Sheet():
    def __init__(self, name: str, ranges: list[Range]):
        self.name = name
        self.ranges = ranges
    
    def __str__(self):
        return f"sheet: {self.name} ranges: {len(self.ranges)}"
    
    def __repr__(self):
        return self.__str__()