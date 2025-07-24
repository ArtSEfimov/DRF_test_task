from django.urls import path

from .views import PhoneAuthView

urlpatterns = [
    path('user-auth/', PhoneAuthView.as_view(), name='user_auth'),
    path('user-validate/', PhoneAuthView.as_view(), name='user_validate')
]
