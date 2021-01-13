from django.shortcuts import render
from creds.forms import (
    CreateUserForm, UserPassResetForm, UserLoginForm
)
from django.views import View
from django.contrib.auth.models import User


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
        user = User.objects.create_user(
            form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
        return render(request, 'creds/login.html', {'form': UserLoginForm()})


def login(request):
    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'creds/login.html', context)


def reset_password(request):
    form = UserPassResetForm()
    context = {'form': form}
    return render(request, 'creds/reset-password.html', context)
