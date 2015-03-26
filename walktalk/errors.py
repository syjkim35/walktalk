ERRORS = {
    "login": "The username/password that you entered is invalid."
}

def get_error(key):
    return ERRORS.get(key, "An error occurred")
