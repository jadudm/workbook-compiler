from wbc.parser.range import (Range, parse_range)
from wbc.parser.objects import (
    check_type,
    requires_keys
    )



class Sheet:
    def __init__(self, name: str, ranges: list[Range]):
        self.name = name
        self.ranges = ranges

    def __str__(self):
        return f"sheet: {self.name} ranges: {len(self.ranges)}"

    def __repr__(self):
        return self.__str__()


def parse_sheet(sh):
    requires_keys(sh, ["type", "name", "ranges"])
    check_type(sh, "sheet")
    return Sheet(sh["name"], [parse_range(r) for r in sh["ranges"]])

