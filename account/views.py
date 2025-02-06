import re
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "account/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':

        context = {"errors": []}

        username = request.POST.get('username')
        email = request.POST.get('email')
        password_1 = request.POST.get('password1')
        password_2 = request.POST.get('password2')

        if User.objects.get(username=username):
            context["errors"].append("username is already taken!")

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            context["errors"].append("please enter a valid email address!")

        elif User.objects.filter(email=email).exists():
            context["errors"].append("email is already taken!")

        if password_1 != password_2:
            context["errors"].append("passwords are not same!")

        if context["errors"]:
            return render(request, "account/register.html", context=context)
        else:
            user = User.objects.create_user(username=username, email=email, password=password_1)
            login(request, user)
            return redirect('home')

    return render(request, "account/register.html")
