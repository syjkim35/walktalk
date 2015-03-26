from django.db  import models
from walktalk   import utils

class User(models.Model):
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Unspecified")
    ]

    username = models.CharField(max_length=64)
    password = models.CharField(max_length=256)     # SHA-256 hash
    email    = models.CharField(max_length=128)
    age      = models.IntegerField()
    sex      = models.CharField(max_length=1, choices=SEX_CHOICES)

    def asJSON(self):
        return utils.jsonify({
            "username": self.username,
            "email":    self.username,
            "age":      self.username,
            "sex":      self.sex,
        })
