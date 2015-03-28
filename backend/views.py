from django.core      import exceptions
from django.shortcuts import render
from django.http      import HttpResponse, HttpResponseRedirect

from walktalk import utils
from walktalk import errors

from backend  import models
from backend  import forms

def only_post(fn):
    def wrapper(request, *args):
        if request.method != "POST":
            return HttpResponse("Bad request: " + str(request.method),
                                status=405)

        return fn(request, *args)

    return wrapper

def authorized(fn):
    def wrapper(request, *args):
        if "authorized" not in request.session:
            return HttpResponse(utils.jsonify(
                errors.make_error(errors.get_error("auth"), 403, None)))

        return fn(request, *args)

    return wrapper

def home(request):
    return HttpResponseRedirect("/login")

@only_post
def login(request):
    loginform = forms.LoginForm(request.POST)

    if loginform.is_valid():
        request.session["authorized"] = True
        request.session["user_object"] = loginform.cleaned_data["user_object"]
        return HttpResponse(loginform.cleaned_data["user_object"].asJSON())

    custom_error = errors.convert_errors(loginform.errors, 401)
    return HttpResponse(utils.jsonify(custom_error),
                        status=custom_error["code"])

@only_post
def register(request):
    reqform = forms.RegisterForm(request.POST)
    if reqform.is_valid():
        return HttpResponse(reqform.cleaned_data["user_object"].asJSON())

    custom_error = errors.convert_errors(reqform.errors, reqform.error_code)
    return HttpResponse(utils.jsonify(custom_error),
                        status=reqform.error_code)

# @authorized
def schedule(request):
    if request.method == "GET":
        sched = models.Schedule.objects.filter(
            user=models.User.objects.get(pk=1)
            #request.session["user_object"]
        ).all()

        # This user still hasn't created a schedule.
        if len(sched) == 0:
            pass

        elif len(sched) != 1:
            pass

        return HttpResponse(sched[0].asJSON())

    elif request.method == "POST":
        # Verify that all of the weekdays are there, filling out the missing
        # ones with zeroes.
        weekdays = { "user": request.session["user_object"] }

        for item in utils.WEEKDAYS:
            weekdays[item] = request.POST.get(item, utils.ZEROES)

        sched = models.Schedule.objects.create(**weekdays)
        return HttpResponse(utils.jsonify(sched.asJSON()))

    # schedform = forms.ScheduleForm(request.POST)
    # if schedform.is_valid():
    #     return HttpResponse(models.Schedule.asJSON(
    #         schedform.cleaned_data["schedule"]))

    custom_error = errors.convert_errors(schedform.errors, schedform.error_code)
    return HttpResponse(utils.jsonify(custom_error),
                        status=schedform.error_code)
