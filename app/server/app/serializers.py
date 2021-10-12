from typing import Optional, Dict

from rest_framework import serializers

from app.models import SharedFile
from module.validator.user_validator import UserValidator
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class SharedFileSerializer(serializers.Serializer):
    user_static_id = serializers.CharField(
        max_length=40,
        validators=[UserValidator.validate_static_id]
    )
    shared_id = serializers.CharField(max_length=54)
    file_root = serializers.CharField()
    start_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    def create(self) -> Dict:
        r: Dict[Optional] = dict(self.data)
        r['user_static_id'] = self.data['user_static_id'].split()[2][1:-1]
        r['start_date'] = datetime.strptime(self.data['start_date'], DATETIME_FORMAT)
        return r

    def build(self) -> SharedFile:
        self.is_valid()
        return SharedFile(**self.validated_data)
