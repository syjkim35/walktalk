from django         import forms
from django.core    import exceptions

from backend  import models
from walktalk import errors

class RegisterForm(forms.Form):
    username            = forms.CharField(label='Username', max_length=64)
    password            = forms.CharField(label='Password', max_length=256)
    password_confirm    = forms.CharField(label='Confirm Password', max_length=256)
    email               = forms.CharField(label='Email Address', max_length=128)
    age                 = forms.IntegerField(label='Age')
    sex                 = forms.ChoiceField(label='Sex',
                                            choices=models.User.SEX_CHOICES)

    def clean_username(self):
        if models.User.objects.filter(
            username=self.cleaned_data["username"]
        ).count() != 0:
            self.error_code = 409    # Conflict
            raise forms.ValidationError(
                errors.get_error("register_username_exists"))

        return self.cleaned_data["username"]

    def clean(self):
        cleaned_data = super(forms.Form, self).clean()
        self.error_code = 200

        if cleaned_data["password"] != cleaned_data["password_confirm"]:
            self.add_error("password", forms.ValidationError(
                errors.get_error("register_password_mismatch")))
            self.add_error("password_confirm", forms.ValidationError(
                errors.get_error("register_password_mismatch")))
            self.error_code = 409   # Conflict

        else:
            tmp = dict(cleaned_data)
            tmp.pop("password_confirm")
            cleaned_data["user_object"] = models.User.objects.create(**tmp)

        return cleaned_data

class LoginForm(forms.Form):
    username            = forms.CharField(label='Username', max_length=64)
    password            = forms.CharField(label='Password', max_length=256)

    def clean(self):
        cleaned_data = super(forms.Form, self).clean()

        try:
            user = models.User.objects.get(
                username=cleaned_data.get("username"),
                password=cleaned_data.get("password"))
            cleaned_data["user_object"] = user

        except models.User.DoesNotExist:
            raise forms.ValidationError(errors.get_error("login"))

        return cleaned_data
