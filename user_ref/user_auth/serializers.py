import re

from rest_framework import serializers

from .models import UserPhone


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhone
        fields = ['phone']

    def validate_phone(self, value):
        cleaned_value = re.sub(r'[^+\d]', '', value)

        if cleaned_value.startswith('8') or cleaned_value.startswith('8'):
            cleaned_value = '+7' + cleaned_value[1:]
        else:
            raise serializers.ValidationError(
                'Корректный номер телефона должен начинаться на +7, 7 или 8')

        if not re.fullmatch(r'\+7\d{10}', cleaned_value):
            raise serializers.ValidationError(
                'Введите корректный номер телефона в формате +7XXXXXXXXXX, 7XXXXXXXXXX или 8XXXXXXXXXX')

        return cleaned_value
