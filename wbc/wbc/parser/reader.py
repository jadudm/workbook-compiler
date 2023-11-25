import json
from _jsonnet import evaluate_file


def read_jsonnet(file):
    sonnet = evaluate_file(file)
    as_obj = json.loads(sonnet)
    return as_obj

def read_json(file):
    as_obj = json.loads(file)
    return as_obj
