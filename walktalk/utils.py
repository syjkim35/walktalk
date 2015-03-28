import json

ZEROES = '0' * ((24 * 60) // 30)     # time chunks
WEEKDAYS = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
]

def jsonify(data):
    return json.dumps(data)

def is_int(value):
    try:
        int(value)
        return True

    except ValueError:
        return False
