from django         import forms
from django.core    import exceptions

from backend  import models
from walktalk import errors

class RegisterForm(forms.Form):
    username            = forms.CharField(label='Username', max_length=64)
    password            = forms.CharField(label='Password', max_length=256)
    password_comfirm    = forms.CharField(label='Confirm Password', max_length=256)
    email               = forms.CharField(label='Email Address', max_length=128)
    age                 = forms.IntegerField(label='Age')
    sex                 = forms.ChoiceField(label='Sex',
                                            choices=models.User.SEX_CHOICES)

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
