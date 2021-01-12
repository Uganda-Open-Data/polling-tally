from django.urls import path
from creds.views.web import login, reset_password, UserSignUp


urlpatterns = [
    path('', login, name='login'),
    path('signup', UserSignUp.as_view(), name='signup'),
    path('reset-password', reset_password, name="reset-password")
]
