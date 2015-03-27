from django.core      import exceptions
from django.shortcuts import render
from django.http      import HttpResponse

from walktalk import utils
from walktalk import errors

from backend  import models
from backend  import forms

def login(request):
    if request.method != "POST":
        return HttpResponse("Bad request: " + request.method, 405)

    loginform = forms.LoginForm(request.POST)

    if loginform.is_valid():
        return HttpResponse(loginform.cleaned_data["user_object"].asJSON())

    custom_error = errors.convert_errors(loginform.errors, 401)
    return HttpResponse(utils.jsonify(custom_error),
                        status=custom_error["code"])

def register(request):
    if request.method == "GET":
        return HttpResponse("Bad request.", 405)    # Method not allowed

    reqform = forms.RegisterForm(request.POST)
    if reqform.is_valid():
        return HttpResponse(reqform.cleaned_data["user_object"].asJSON())

    custom_error = errors.convert_errors(reqform.errors, reqform.error_code)
    return HttpResponse(utils.jsonify(custom_error),
                        status=reqform.error_code)
