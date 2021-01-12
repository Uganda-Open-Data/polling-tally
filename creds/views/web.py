from django.shortcuts import render
from creds.forms import (
    CreateUserForm, UserPassResetForm, UserLoginForm
)
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse
import logging

class UserSignUp(View):
    """
    View to handle user sign up
    """
    def get(self, request):
        context = {'form': CreateUserForm()}
        return render(request, 'creds/signup.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if not form.is_valid():
            context = {'form': CreateUserForm(), 'sign_up_errors': form.errors}
            return render(request, 'creds/signup.html', context)

        # create use if form is valid
        User.objects.create_user(
            form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password1'))
        return HttpResponse('User created.')


def login(request):
    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'creds/login.html', context)


def reset_password(request):
    form = UserPassResetForm()
    context = {'form': form}
    return render(request, 'creds/reset-password.html', context)
