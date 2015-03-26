import json

def jsonify(data):
    return json.dumps(data)

def make_error(error_str, error_code, field):
    return {
        "error": error_str,
        "code": error_code,
        "field": field
    }
