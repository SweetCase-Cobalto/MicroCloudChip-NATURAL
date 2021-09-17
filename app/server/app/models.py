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
