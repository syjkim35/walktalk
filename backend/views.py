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
    else:
        return HttpResponse(utils.jsonify(loginform.errors),
                            status=loginform.errors["code"])

def register(request):
    if request.method == "GET":
        return HttpResponse("Bad request.", 405)    # Method not allowed


