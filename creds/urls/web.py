from django.urls import path
from creds.views.web import UserLogin, recover_password, UserSignUp


urlpatterns = [
    path('', UserLogin.as_view(), name='login'),
    path('login', UserLogin.as_view(), name='login'),
    path('register', UserSignUp.as_view(), name='signup'),
    path('recover-password', recover_password, name="recover-password")
]
