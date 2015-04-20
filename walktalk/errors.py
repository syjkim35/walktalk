ERRORS = {
    "auth":                         "User not authorized.",
    "login":                        "The username/password that you entered is invalid.",
    "register_username_exists":     "This username already exists.",
    "register_password_mismatch":   "The passwords do not match.",
}

def get_error(key):
    return ERRORS.get(key, "An error occurred")

def convert_errors(django_errors, error_code=404):
    if "__all__" in django_errors:
        field = None
        error = django_errors["__all__"][0]
    else:
        for i in django_errors:
            first_error = django_errors[i][0]
            break

        field = first_error
        error = django_errors[first_error]

    return make_error(error, error_code, field)

def make_error(error_str, error_code, field):
    return {
        "error": error_str,
        "code": error_code,
        "field": field
    }
