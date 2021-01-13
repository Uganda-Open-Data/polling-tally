from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
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

        user = User.objects.create_user(
            form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
        return render(request, 'creds/login.html', {'form': UserLoginForm()})


class UserLogin(View):
    def get(self, request):
        context = {'form': UserLoginForm()}
        return render(request, 'creds/login.html', context)

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username", "")
            password = form.cleaned_data.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('voting:dashboard')
        else:
            context = {'form': form, 'login_errors': form.errors}
            return render(request, 'creds/login.html', context)


def reset_password(request):
    form = UserPassResetForm()
    context = {'form': form}
    return render(request, 'creds/reset-password.html', context)
