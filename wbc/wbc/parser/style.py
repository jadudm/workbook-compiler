from colour import Color
from wbc.parser.util import check_type, requires_keys
from wbc.constants import STYLES


class Side():
    # https://pypi.org/project/colour/
    def __init__(self, style:str=None, color=Color("black")):
        self.style = style
        self.color = color

class Border():
    def __init__(self, 
                 left:Side=None, 
                 right:Side=None, 
                 top:Side=None,
                 bottom:Side=None, 
                outline:Side=None):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.outline = outline

class Font():
    def __init__(self, face=None, bold:bool=False, size:int=12, color:Color=Color("black")):
        self.face = face
        self.bold = bold
        self.color = color

class NamedStyle():
    def __init__(self, name, font:Font=None, border:Border=None):
        self.name = name
        self.font = font
        self.border = None

def parse_font(f):
    if f is None:
        return None
    requires_keys(f, ["type"])
    check_type(f, "font")
    return Font(face = f.get("face", None),
                bold = f.get("bold", False),
                size = f.get("size", 12),
                color = Color(f.get("color", "black"))
                )

def parse_side(s):
    if s is None:
        return None
    requires_keys(s, ["type"])
    check_type(s, "side")
    return Side(style=s.get("style", None),
                color=Color(s.get("color", "black"))
                )

def parse_border(b):
    if b is None:
        return None
    requires_keys(b, ["type"])
    check_type(b, "border")
    return Border(left=parse_side(b.get("left", None)),
                  right=parse_side(b.get("right", None)),
                  top=parse_side(b.get("top", None)),
                  bottom=parse_side(b.get("bottom", None)),
                  outline=parse_side(b.get("outline", None))
    )


def parse_named_style(ns):
    requires_keys(ns, ["type", "name"])
    check_type(ns, "named_style")
    return NamedStyle(ns.get("name"), 
                      font=parse_font(ns.get("font", None)),
                      border=parse_border(ns.get("border", None))
                      )
