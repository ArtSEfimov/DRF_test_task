import random
import time
from string import digits, ascii_letters

from django.contrib.auth import get_user_model
from django.core.cache import cache as verify_codes_cache
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserPhoneSerializer, VerifyCodeSerializer, UserProfileSerializer

INVITE_CHARS = digits + ascii_letters

User = get_user_model()


class AuthByPhoneView(APIView):
    def post(self, request):
        serializer = UserPhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            verify_code = self.get_verify_code(phone)
            time.sleep(2)
            print(verify_code)  # SMS like
            message = f'Код отправлен на номер {phone}'
            user, created = User.objects.get_or_create(
                user_phone_query__phone=phone,
                defaults={'username': f'user_{phone}'}
            )
            if created:
                invite_code = self.generate_invite_code()
                UserProfile.objects.create(user=user, phone=phone, invite_code=invite_code)
                message += f"\nновый пользователь {f'user_{phone}'} создан"

            return Response({"message": message})

    @staticmethod
    def generate_verify_code():
        return random.randint(1000, 9999)

    def get_verify_code(self, phone):
        if (code := verify_codes_cache.get(phone)) is not None:
            return code

        generated_verify_code = self.generate_verify_code()
        verify_codes_cache.set(phone, generated_verify_code)
        return generated_verify_code

    @staticmethod
    def generate_invite_code():
        return ''.join(random.choices(INVITE_CHARS, k=6))


class VerifyByCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            user_verify_code = serializer.validated_data['code']
            cached_verify_code = verify_codes_cache.get(phone)
            if cached_verify_code is None or user_verify_code != cached_verify_code:
                return Response({'error': 'Код подтверждения некорректен или устарел.'},
                                status=status.HTTP_400_BAD_REQUEST)

            verify_codes_cache.delete(phone)
            return Response({'message': 'Верификация прошла успешно.'}, status=status.HTTP_200_OK)


class UserInfoView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
