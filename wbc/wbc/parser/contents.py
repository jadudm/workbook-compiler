from typing import Dict, Any
from wbc.parser.exceptions import ParseException
from wbc.parser.util import check_type, requires_keys


class Contents:
    def __init__(self, 
                 value,
                 style=None, 
                 wrap=False,
                 properties: Dict[str, Any] = None):
        if isinstance(value, Contents):
            raise ParseException(f"Contents cannot contain Contents")
        self.value = value
        self.style = style
        self.properties = properties
        self.wrap = wrap

    def __str__(self):
        return self.value
    
    def __reprt__(self):
        return self.__str__()


def parse_contents(c):
    if c == None:
        return None
    check_type(c, "contents")
    requires_keys(c, ["value"])
    return Contents(c["value"],
                    style=c.get("style", None),
                    wrap=c.get("wrap", False)
                    )
