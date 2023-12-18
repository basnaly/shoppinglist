from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from shopping.forms import RegisterForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.

def index(request):
    return render(request, "shopping/index.html",{})


def register(request):
    if request.method == "GET":
        return render(request, "shopping/register.html", {
            "form": RegisterForm
        })
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
            
            if password != confirmation:
                messages.error(request, "Password must match conformation.")
                return HttpResponseRedirect(reverse("register"))
                
            try:
                new_user = User.objects.create_user(
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    password = password
                )
                new_user.save()
            except IntegrityError:
                messages.error(request, "User already taken!")
                return HttpResponseRedirect(reverse("register"))
            
            login(request, new_user)
            messages.success(request, "The user was successfully saved!")
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form.errors)
            messages.error(request, "Some of the values are not valid!")
            return HttpResponseRedirect(reverse("register"))
                

def login_view(request):
    if request.method == "GET":
        return render(request, "shopping/login.html", {
            "form": LoginForm
        })
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, "Invalid username or password!")
                return render(request, "shopping/login.html", {
                    "form":form
                })
        else:
            messages.error(request, "The form is not valid!")
            return render(request, "shopping/login.html", {
                "form":form
            })



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))