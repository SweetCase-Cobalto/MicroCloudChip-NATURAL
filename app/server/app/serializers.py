from rest_framework import serializers

from app.models import SharedFile
from module.validator.user_validator import UserValidator
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class SharedFileSerializer(serializers.Serializer):
    user_static_id = serializers.CharField(
        max_length=40,
        validators=[UserValidator.validate_static_id]
    )
    shared_id = serializers.CharField(max_length=54)
    file_root = serializers.CharField()
    start_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    def change_start_date_to_datetime(self, start_date: str) -> datetime:
        return datetime.strptime(start_date, DATETIME_FORMAT)

    def build(self) -> SharedFile:
        self.is_valid()
        return SharedFile(**self.validated_data)