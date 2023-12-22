from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    
    path("add_shop", views.add_shop, name="add_shop"),
    path("add_item", views.add_item, name="add_item"),
    
    path("manage_shops", views.manage_shops, name="manage_shops"),
    
    path("delete_item/<str:name>", views.delete_item, name="delete_item"),
    path("delete_shop/<str:name>", views.delete_shop, name="delete_shop"),
    
    path("profile", views.profile, name="profile"),
]

# POST add_shop
# POST delete_shop
# GET shops_page