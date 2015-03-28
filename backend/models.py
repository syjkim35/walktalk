import re

from django.db  import models
from walktalk   import utils

class BitstringField(models.Field, metaclass=models.SubfieldBase):
    def __init__(self, *args, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = len(utils.ZEROES)
        kwargs["default"] = utils.ZEROES

        self.bitstring = []
        self.length = kwargs["max_length"]
        super(BitstringField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(BitstringField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return "bit"

    def to_python(self, value):
        if isinstance(value, list):
            self.bitstring = value

        matches = re.match(r"(\d)::bit\((\d)\)", value)
        if value is None or not matches:
            self.bitstring = [0 for i in range(self.length)]

        else:
            print(matches.groups())
            bits = [int(x) for x in bin(str(matches.group(1)))]

            # pad with zeroes on the left
            self.bitstring = [
                0 for i in range(matches.group(2) - len(bits))
            ] + bits

        return self.toString()

    def get_prep_value(self, value):
        if not value:
            return '0'

        as_str = ''.join([str(x) for x in value])
        return "%d::bit(%d)" % (int(as_str, 2), len(as_str))

    def __getitem__(self, index):
        return self.bitstring[index]

    def toString(self):
        return ''.join([str(x) for x in self.bitstring])

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
            "email":    self.email,
            "age":      self.age,
            "sex":      self.sex,
        })

class Schedule(models.Model):
    user        = models.ForeignKey(User)
    monday      = BitstringField()
    tuesday     = BitstringField()
    wednesday   = BitstringField()
    thursday    = BitstringField()
    friday      = BitstringField()
    saturday    = BitstringField()
    sunday      = BitstringField()

    def asJSON(self):
        return utils.jsonify({
            "username":     self.user.username,
            "tuesday":      self.tuesday,
            "wednesday":    self.wednesday,
            "thursday":     self.thursday,
            "friday":       self.friday,
            "saturday":     self.saturday,
            "sunday":       self.sunday
        })
