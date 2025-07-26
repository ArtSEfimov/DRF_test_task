import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserProfile

User = get_user_model()


class PhoneValidationMixin:

    @staticmethod
    def validate_phone(value):
        cleaned_value = re.sub(r'[^+\d]', '', value)

        if cleaned_value.startswith(('8', '7')):
            cleaned_value = '+7' + cleaned_value[1:]
        elif cleaned_value.startswith('+7'):
            cleaned_value = '+7' + cleaned_value[2:]
        else:
            raise serializers.ValidationError(
                'Корректный номер телефона должен начинаться на +7, 7 или 8')

        if not re.fullmatch(r'^\+7\d{10}$', cleaned_value):
            raise serializers.ValidationError(
                'Введите корректный номер телефона в формате +7XXXXXXXXXX, 7XXXXXXXXXX или 8XXXXXXXXXX')

        return cleaned_value


class UserPhoneSerializer(PhoneValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone']


class VerifyCodeSerializer(PhoneValidationMixin, serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.IntegerField(min_value=1000, max_value=9999)


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    own_invite_code = serializers.SerializerMethodField()
    foreign_invite_code = serializers.SerializerMethodField(read_only=True)
    invites = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'own_invite_code', 'foreign_invite_code', 'invites',
                  'is_verified']

    def get_phone(self, obj):
        return obj.user_profile.phone

    def get_own_invite_code(self, obj):
        return obj.user_profile.own_invite_code

    def get_foreign_invite_code(self, obj):
        try:
            return obj.user_profile.invited_by.user_profile.own_invite_code
        except AttributeError:
            return None

    def get_invites(self, obj):
        return list(
            obj.invited_users
            .values_list('phone', flat=True)
        )

    def get_is_verified(self, obj):
        return obj.user_profile.is_verified


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

    def validate_invite_code(self, value):
        if UserProfile.objects.filter(own_invite_code=value).exists():
            return value
        raise serializers.ValidationError(
            f'Invite код {value} не существует')
