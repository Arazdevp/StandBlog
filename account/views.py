import re
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, EditUserInfoForm


# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            login(request, User.objects.get(username=form.cleaned_data['username']))
            return redirect('home')

        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect("home")
    else:
        form = LoginForm()
    return render(request, "account/login.html", context={"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST.get('username'),
                                            email=request.POST.get('email'),
                                            password=request.POST.get('password1'))
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, "account/register.html", {"form": form})


def edit_user_info(request):
    if request.method == 'POST':
        form = EditUserInfoForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('edit_info')
    else:
        form = EditUserInfoForm(instance=request.user)
    return render(request, 'account/edit_info.html', {"form": form})