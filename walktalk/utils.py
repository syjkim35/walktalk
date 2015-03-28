import json

from django.http import HttpResponse
from walktalk    import errors

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

def only_post(fn):
    def wrapper(request, *args):
        if request.method != "POST":
            return HttpResponse("Bad request: " + str(request.method),
                                status=405)

        return fn(request, *args)

    return wrapper

def only_get(fn):
    def wrapper(request, *args):
        if request.method != "GET":
            return HttpResponse("Bad request: " + str(request.method),
                                status=405)

        return fn(request, *args)

    return wrapper

def authorized(fn):
    def wrapper(request, *args):
        if "authorized" not in request.session:
            return HttpResponse(jsonify(
                errors.make_error(errors.get_error("auth"), 403, None)))

        return fn(request, *args)

    return wrapper
