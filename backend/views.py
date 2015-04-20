import math

from django.core      import exceptions
from django.shortcuts import render, get_object_or_404
from django.http      import HttpResponse, HttpResponseRedirect

from walktalk import utils
from walktalk import errors

from backend  import models
from backend  import forms

def home(request):
    return HttpResponseRedirect("/login")

# @utils.only_post
def login(request):
    if request.method == "GET":
        return render(request, "login.html", {
            "login_form": forms.LoginForm()
        })

    loginform = forms.LoginForm(request.POST)

    if loginform.is_valid():
        request.session["authorized"] = True
        request.session["user_object"] = loginform.cleaned_data["user_object"]
        return HttpResponse(loginform.cleaned_data["user_object"].asJSON())

    custom_error = errors.convert_errors(loginform.errors, 401)
    return HttpResponse(utils.jsonify(custom_error),
                        status=custom_error["code"])

# @utils.only_post
def register(request):
    if request.method == "GET":
        return render(request, "register.html", {
            "register_form": forms.RegisterForm()
        })

    reqform = forms.RegisterForm(request.POST)
    if reqform.is_valid():
        return HttpResponse(reqform.cleaned_data["user_object"].asJSON())

    custom_error = errors.convert_errors(reqform.errors, reqform.error_code)
    return HttpResponse(utils.jsonify(custom_error),
                        status=reqform.error_code)

@utils.authorized
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

    return HttpResponse("No.", status=403)
    # custom_error = errors.convert_errors(schedform.errors, schedform.error_code)
    # return HttpResponse(utils.jsonify(custom_error),
    #                     status=schedform.error_code)

@utils.only_get
@utils.authorized
def nearby(request):
    if request.method == "GET":
        user = request.session["user_object"]
        loc  = get_object_or_404(models.Location, user=user)
        print(loc)

        # Naive user search
        all_users = models.User.objects.all()

        dist = lambda x, y: math.sqrt(
            (x.latitude  - y.latitude) ** 2,
            (x.longitude - y.longitude) ** 2)

        potential = {}
        for i in all_users:
            temp_location = models.Location.objects.filter(user=i)
            if not temp_location:
                continue

            d = dist(i, user)
            if d < 5: # < pref.radius:
                potential[i.username] = d

        return HttpResponse(utils.jsonify({
            "nearby_users": potential
        }))

    return HttpResponse("No.", status=403)
