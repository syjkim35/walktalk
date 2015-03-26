from django.core      import exceptions
from django.shortcuts import render
from django.http      import HttpResponse

from backend import models
from walktalk import utils
from walktalk import errors

def login(request):
    if request.method == "POST":
        loginform = forms.LoginForm(request.GET)

        if loginform.is_valid():
            return HttpResponse(loginform.user_object.asJSON())
        else:
            return HttpResponse(utils.jsonify(loginform.errors),
                                status=loginform.errors["code"])

    return HttpResponse("Bad request.", 400)
