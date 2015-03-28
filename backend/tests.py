from django.test import TestCase
from django.test import RequestFactory

from backend.models import *
from backend        import views
from backend.forms  import *
from walktalk       import errors

MOCK_USER_DATA = {
    "username": "gk",
    "password": "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05"
}

def add_dicts(d1, d2):
    return dict([
        (k, v) for k, v in d1.items()
    ] + [
        (k, v) for k, v in d2.items()
    ])

def add_all_dicts(*dicts):
    final = {}
    for i in dicts:
        final = add_dicts(final, i)
    return final

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

    def test_login_view_ok(self):
        client = RequestFactory()
        response = client.post("/login", MOCK_USER_DATA)
        self.assertEqual(views.login(response).content,
                         self.user.asJSON().encode())

    def test_login_view_notok(self):
        client = RequestFactory()
        response = client.post("/login", {
            "username": MOCK_USER_DATA["username"],
            "password": "bad password"
        })

        self.assertNotEqual(views.login(response).content,
                            self.user.asJSON().encode())
        self.assertEqual(views.login(response).content,
                         utils.jsonify(errors.make_error(
                            errors.get_error("login"),
                            401,
                            None)).encode())

MOCK_REGISTER_DATA = add_dicts({
    "password_confirm": MOCK_USER_DATA["password"],
    "sex": 'M',
    "age": 42,
    "email": "george.k@berkeley.edu",
}, MOCK_USER_DATA)

class RegisterTestCase(TestCase):
    def test_register_works(self):
        reg = RegisterForm(MOCK_REGISTER_DATA)

        self.assertTrue(reg.is_valid())
        self.assertTrue(isinstance(reg.cleaned_data["user_object"], User))

    def test_reg_passmatch(self):
        tmp = dict(MOCK_REGISTER_DATA)
        tmp["username"] += "_new"
        tmp["password_confirm"] = "bad match"
        reg = RegisterForm(tmp)

        self.assertEqual(reg.is_valid(), False)
        self.assertTrue(errors.get_error(
            "register_password_mismatch") in reg.errors.get("password"))
        self.assertTrue(errors.get_error(
            "register_password_mismatch") in reg.errors.get("password_confirm"))

    def test_reg_userexists(self):
        # First, register a user.
        self.test_register_works()

        # Then, try to register a user with the same name.
        reg = RegisterForm(MOCK_REGISTER_DATA)

        self.assertEqual(reg.is_valid(), False)
        self.assertTrue(errors.get_error(
            "register_username_exists") in reg.errors.get("username"))

    def test_reg_view_ok(self):
        tmp = dict(MOCK_REGISTER_DATA)
        tmp["username"] += "_tmp"

        client = RequestFactory()
        response = client.post("/register", tmp)
        self.assertEqual(views.register(response).content,
                         User.objects.get(
                            username=tmp["username"]
                         ).asJSON().encode())
