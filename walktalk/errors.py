ERRORS = {
    "login":                        "The username/password that you entered is invalid.",
    "register_username_exists":     "This username already exists.",
    "register_password_mismatch":   "The passwords do not match.",
}

def get_error(key):
    return ERRORS.get(key, "An error occurred")

def convert_errors(django_errors, error_code=404):
    custom_error = {}
    custom_error["code"] = error_code

    if "__all__" in django_errors:
        custom_error["field"] = None
        custom_error["error"] = django_errors["__all__"][0]
    else:
        first_error = django_errors.keys()[0]
        custom_error["field"] = first_error
        custom_error["error"] = django_errors[first_error]

    return custom_error

def make_error(error_str, error_code, field):
    return {
        "error": error_str,
        "code": error_code,
        "field": field
    }
