from django.test import TestCase
from django.test import RequestFactory

from backend.models import *
from backend        import views
from backend.forms  import LoginForm
from walktalk       import errors

MOCK_USER_DATA = {
    "username": "gk",
    "password": "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05"
}

class LoginTestCase(TestCase):
    def setUp(self):
        # http://www.xorbin.com/tools/sha256-hash-calculator
        # Hash of "testpassword"
        self.user = User.objects.create(
            username=MOCK_USER_DATA["username"],
            password=MOCK_USER_DATA["password"],
            email="george.k@berkeley.edu",
            age=25,
            sex='M',
        )

    def test_login_works(self):
        login = LoginForm(MOCK_USER_DATA)

        self.assertTrue(login.is_valid())
        self.assertTrue("user_object" in login.cleaned_data)
        self.assertTrue(isinstance(login.cleaned_data["user_object"], User))
        self.assertTrue(login.cleaned_data["user_object"].sex in [
            x[0] for x in User.SEX_CHOICES])
        print(login.cleaned_data["user_object"].asJSON())

    def test_login_badpassword(self):
        login = LoginForm({
            "username": MOCK_USER_DATA["username"],
            "password": "bad password"
        })

        self.assertEqual(login.is_valid(), False)
        self.assertTrue(errors.get_error("login") in login.errors.get("__all__"))

    def test_login_badusername(self):
        login = LoginForm({
            "username": "bad username",
            "password": MOCK_USER_DATA["password"]
        })

        self.assertEqual(login.is_valid(), False)
        self.assertTrue(errors.get_error("login") in login.errors.get("__all__"))

    def test_login_view(self):
        client = RequestFactory()
        response = client.post("/login", MOCK_USER_DATA)
        self.assertEqual(views.login(response).content,
                         self.user.asJSON().encode())
