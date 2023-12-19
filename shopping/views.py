from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
from shopping.forms import RegisterForm, LoginForm
from .models import User, Shop
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    user_shops = []
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_shops = Shop.objects.filter(owner=user)
    return render(request, "shopping/index.html",{
        "user_shops": user_shops
    })


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
                return render(request, "shopping/register.html", {
                    "form": form
                })
                
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
                return render(request, "shopping/register.html", {
                    "form": form
                })
            
            login(request, new_user)
            messages.success(request, "The user was successfully saved!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Some of the values are not valid!")
            return render(request, "shopping/register.html", {
                "form": form,
            })
                

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


@login_required
def add_shop(request):
    user = User(id=request.user.id)
    user_shops = Shop.objects.filter(owner=user)
    if request.method == "POST":
        shop_name = request.POST.get("shop_name")
        # name="shop_name" from index.html form input
        try:
            if not shop_name:
                raise ValidationError(message="Please enter the valid text!")
            new_shop = Shop.objects.create(
                shop_name = shop_name,
                owner = user
            )
            new_shop.save()
        except IntegrityError:
            messages.error(request, "Something went wrong. Try again later.")
            return HttpResponseRedirect(reverse("index"))
        except ValidationError:
            messages.error(request, "Please enter the valid text!")
            return HttpResponseRedirect(reverse("index"))
        messages.success(request, f"The shop {new_shop.shop_name} was successfully added!")
        return HttpResponseRedirect(reverse("index"))
    