import json


def load_json_file(path, hook=None):
    try:
        with open(path, 'rt') as handle:
            return json.load(handle, object_hook=hook)
    except json.JSONDecodeError:
        return {}
