import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserProfile

User = get_user_model()


def phone_validator(value):
    cleaned_value = re.sub(r'[^+\d]', '', value)

    if cleaned_value.startswith('8') or cleaned_value.startswith('7'):
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


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone']

    @staticmethod
    def validate_phone(value):
        return phone_validator(value)


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator])
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
        try:
            return obj.user_profile.phone
        except AttributeError:
            return None

    def get_own_invite_code(self, obj):
        try:
            return obj.user_profile.own_invite_code
        except AttributeError:
            return None

    def get_foreign_invite_code(self, obj):
        try:
            return obj.user_profile.invited_by.user_profile.own_invite_code
        except AttributeError:
            return None

    def get_invites(self, obj):
        # user_invites_profiles = UserProfile.objects.filter(user__in=obj.invited_users.all())
        return UserPhoneSerializer(obj.invited_users.all(), many=True).data

    def get_is_verified(self, obj):
        try:
            return obj.user_profile.is_verified
        except AttributeError:
            return None
