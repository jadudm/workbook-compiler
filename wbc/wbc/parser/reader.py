import json
from _jsonnet import evaluate_file


def read(file):
    sonnet = evaluate_file(file)
    as_obj = json.loads(sonnet)
    return as_obj
