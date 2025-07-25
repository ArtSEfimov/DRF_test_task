from django.urls import path

from .views import AuthByPhoneView, VerifyByCodeView, UserInfoView, RevokeUserVerify, ActivateInviteCode

urlpatterns = [
    path('auth/', AuthByPhoneView.as_view(), name='user_auth'),
    path('verify/', VerifyByCodeView.as_view(), name='user_verify'),
    path('users/', UserInfoView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserInfoView.as_view(), name='user_detail'),
    path('users/<int:pk>/revoke/', RevokeUserVerify.as_view(), name='user_revoke'),
    path('users/<int:pk>/activate/', ActivateInviteCode.as_view(), name='user_activate'),

]