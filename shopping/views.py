import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
from shopping.forms import RegisterForm, LoginForm, ProfileForm
from .models import User, Shop, Item
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def index(request):
    user_shops = []
    user_items = []
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_shops = Shop.objects.filter(owner=user)
        user_items = Item.objects.filter(owner=user)
    return render(request, "shopping/index.html",{
        "user_shops": user_shops,
        "user_items": user_items
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
            return HttpResponseRedirect(reverse("manage_shops"))
        except ValidationError:
            messages.error(request, "Please enter the valid text!")
            return HttpResponseRedirect(reverse("manage_shops"))
        messages.success(request, f"The shop {new_shop.shop_name} was successfully added!")
        return HttpResponseRedirect(reverse("index"))
    
    
# @login_required
# def add_item(request):
#     user = User.objects.get(id=request.user.id)
#     user_shops = Shop.objects.filter(owner=user)
#     user_items = Item.objects.filter(owner=user)
#     if request.method == "GET":
#         return render(request, "shopping/add_item.html", {
#             "user_shops": user_shops,
#             "user_items": user_items
#         })
#     else:
#         item_name = request.POST.get("item_name")
#         item_note = request.POST.get("item_note")
#         shop = request.POST.get("shop")
#         if not item_name or not shop:
#             raise ValidationError(message="Please enter the valid text!")
#         try: 
#             shop = Shop.objects.get(owner=user, shop_name=shop)
#             new_item = Item.objects.create(
#                 item_name = item_name,
#                 item_note = item_note,
#                 shop = shop,
#                 owner = user
#             )
#             new_item.save()
#         except IntegrityError:
#             messages.error(request, "Something went wrong. Try again later.")
#             return HttpResponseRedirect(reverse("add_item"))
#         except ValidationError:
#             messages.error(request, "Please enter the valid text!")
#             return HttpResponseRedirect(reverse("add_item"))
#         messages.success(request, f"The {new_item.item_name} item was successfully added!")
#         return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def add_item(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "GET":
        return JsonResponse({})
    
    else:
        data = json.loads(request.body)
        item_name = data.get("item_name")
        item_note = data.get("item_note")
        shop_id = data.get("shop_id")
        if not item_name or not shop_id:
            raise ValidationError(message="Please enter the valid text!")
        try:
            shop = Shop.objects.get(owner=user, id=shop_id)
            new_item = Item.objects.create(
                item_name = item_name,
                item_note = item_note,
                shop = shop,
                owner = user
            )
            new_item.save()
        except IntegrityError:
            return JsonResponse({
                "message": "Something went wrong. Try again later."
            })
        except ValidationError:
            return JsonResponse({
                "message": "Please enter the valid text!"
            })
        return JsonResponse({
            "message": f"The item { item_name } was successfully added!"
        })


@csrf_exempt
@login_required
def delete_item(request, name):
    user = User.objects.get(id=request.user.id)
    try:
        item = Item.objects.get(id=name, owner=user)
    except Item.DoesNotExist:
        return JsonResponse({
            "message": "It is not your item!"
        }) 
   
    if request.method == "DELETE":
        try:
            item.delete()
        except IntegrityError:
            return JsonResponse({
                "message": "Something went wrong. Try again later."
            })
        return JsonResponse({
            "message": f"Your { item.item_name } was successfully deleted!"
        })


@csrf_exempt
@login_required
def delete_shop(request, name):
        user = User.objects.get(id=request.user.id)
        try:
            shop = Shop.objects.get(owner=user, id=name)
        except Shop.DoesNotExist:
            return JsonResponse({
                "message": "It is not your shop!"
            })
            
        if request.method == "DELETE":
            try:
                shop.delete()
            except IntegrityError:
                return JsonResponse({
                    "message": "Something went wrong. Try again later."
                })
        return JsonResponse({
            "message": f"Your shop {shop.shop_name} was successfuly deleted!"
        })
                

# @login_required
# def delete_shop(request, name):
#     user = User.objects.get(id=request.user.id)
   
#     if request.method == "POST": 
#         try:
#             shop = Shop.objects.get(owner=user, id=name)
#             shop.delete()
#         except Shop.DoesNotExist:
#             messages.error(request, "It's not your shop!")
#             return HttpResponseRedirect(reverse('manage_shops'))
#         except IntegrityError:
#             messages.error(request, "Something went wrong. Try again later.")
#             return HttpResponseRedirect(reverse('manage_shops'))
#         messages.success(request, f"Your { shop.shop_name } shop was successfully deleted!")
#         return HttpResponseRedirect(reverse('manage_shops'))


@login_required
def manage_shops(request):
    user = User(id=request.user.id)
    user_shops = Shop.objects.filter(owner=user)
    if request.method == "GET":
        return render(request, "shopping/manage_shops.html", {
            "user_shops": user_shops
        })
    
    
@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "GET":
        return render(request, "shopping/profile.html", {
            "form": ProfileForm(initial={
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
        })
    else:
        form = ProfileForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            current_password = form.cleaned_data.get("current_password")
            new_password = form.cleaned_data.get("new_password")
            confirmation = form.cleaned_data.get("confirmation")
            
            if not check_password(current_password, user.password):
                messages.error(request, "The current password doesn't match.")
                return render(request, "shopping/profile.html", {
                    "form": form
                })
            
            if new_password:
                if new_password != confirmation:
                    messages.error(request, "The new password doesn't match confirmation.")
                    return render(request, "shopping/profile.html", {
                        "form": form
                    })
                else: 
                    user.set_password(new_password)
                    
            try:
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                update_session_auth_hash(request, user)
            except IntegrityError:
                messages.error(request, "Something went wrong. Try again later.")
                return render(request, "shopping/profile.html", {
                    "form": form
                })
            messages.success(request, f"Your profile was successfully updated!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "The form is not valid!")
            return render(request, "shopping/profile.html", {
                "form": form
            })
            
                
                