import datetime
import random
import string
from django.db import models

from module.validator.user_validator import UserValidator


# Create your models here.
class User(models.Model):
    static_id = models.CharField(max_length=40, primary_key=True, validators=[UserValidator.validate_static_id])
    name = models.CharField(max_length=16, validators=[UserValidator.validate_name])
    pswd = models.CharField(max_length=128, validators=[UserValidator.validate_password])
    email = models.EmailField(max_length=256, validators=[UserValidator.validate_email])
    volume_type = models.CharField(max_length=32)
    is_admin = models.BooleanField(validators=[UserValidator.validate_is_admin])

    def to_dict(self):
        return {
            'static_id': self.static_id,
            'name': self.name,
            'pswd': self.pswd,
            'email': self.email,
            'volume_type': self.volume_type,
            'is_admin': self.is_admin
        }


class SharedFile(models.Model):
    user_static_id = models.ForeignKey(
        "User", on_delete=models.CASCADE,
        db_column="user_static_id",
        validators=[UserValidator.validate_static_id]
    )
    shared_id = models.CharField(max_length=54, primary_key=True, blank=True)
    file_root = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # random id 생성
        self.shared_id = \
            datetime.datetime.now().strftime("%Y%m%d") + \
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))

        super().save(*args, *kwargs)
