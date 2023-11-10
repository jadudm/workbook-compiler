from .exceptions import ParseException

def check_type(o, type):
    if "type" not in o:
        raise ParseException(f"Object does not contain key `type`")
    if o['type'] != type:
        raise ParseException(f"Object is not of type `{type}`")
    return True
    
def requires_keys(o, keys):
    for r in keys:
        if r not in o:
            raise ParseException(f"missing key {r} in sheet")
    return True

def allowed_keys(o, keys):
    for k in o.keys():
        if k not in keys:
            raise ParseException(f"key {k} not allowed in object {o}")