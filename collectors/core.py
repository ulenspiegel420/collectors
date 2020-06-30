import json


def load_json_file(path):
    try:
        with open(path, 'rt') as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return