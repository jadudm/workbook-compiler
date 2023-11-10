from typing import Dict, Any
from wbc.parser.exceptions import ParseException
from wbc.parser.objects import (
    check_type,
    requires_keys
    )

class Contents:
    def __init__(self, value, properties: Dict[str, Any] = None):
        if isinstance(value, Contents):
            raise ParseException(f"Contents cannot contain Contents")
        self.value = value
        self.properties = properties

    def __str__(self):
        return self.value


def parse_contents(c):
    if c is None:
        return None
    requires = ["value"]
    for r in requires:
        if r not in c:
            raise ParseException(f"missing key {r} in cell")
    return Contents(c["value"])
