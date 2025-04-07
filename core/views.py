from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model, login, logout as auth_logout, authenticate
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
User = get_user_model()


def index(request):
    return render(request, "index.html")


@login_required(login_url="signin")
def settings(request):
    return render(request, "setting.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 and password2 and password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "the username is taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, password=password1)
                Profile.objects.create(user=user, id_user=user.id)
                user_login = authenticate(username=username, password=password1)
                if user_login:
                    login(request, user_login)
                return redirect("settings")
        else:
            messages.info(request, "the passwords did not match")
            return redirect("signup")
    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_login = authenticate(username=username, password=password)
        if user_login:
            login(request, user_login)
            messages.success(request, "You have successfully logged in.")
            return redirect("index")
        else:
            messages.info(request, "ops something is wrong")
    return render(request, "signin.html")


def logout(request):
    auth_logout(request)
    return redirect("index")
