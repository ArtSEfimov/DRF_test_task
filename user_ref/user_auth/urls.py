from django.urls import path

from .views import AuthByPhoneView, VerifyByCodeView, UserInfoView

urlpatterns = [
    path('user-auth/', AuthByPhoneView.as_view(), name='user_auth'),
    path('user-validate/', VerifyByCodeView.as_view(), name='user_validate'),
    path('users/', UserInfoView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserInfoView.as_view(), name='user_detail'),

]
